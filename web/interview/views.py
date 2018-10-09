from django.shortcuts import render, redirect
from django.http import HttpResponse
from interview.models import *
import os, shutil,json
import random
import zipfile
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from interview.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def login(request):
    if request.method == "POST":
        form = LoginForm(request=request,data=request.POST)
        if form.is_valid():
            return redirect('/')
    else:
        form = LoginForm()
        if request.user.is_authenticated:
            return redirect('/')

    return render(request, 'templates/login.html',
                  {'page':'Login',
                   'form':form})

def logout(request):
    django_logout(request)
    return redirect('/')

@login_required(login_url="/login/")
def index(request):
    request.session.set_expiry(10800)
    return render(request, 'templates/index.html',
                  {"page":'Examinations',
                   "user":request.user})

def rand_str(length=32):
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    ss = ""
    for i in range(length):
        ss = ss + s[random.randint(0, len(s) - 1)]
    return ss

def process_zip(zip_file, pid):
    test_case_dir = os.path.join(settings.TEST_CASE_DIR, str(pid))
    if not os.path.exists(test_case_dir):
        os.mkdir(test_case_dir)
    if zipfile.is_zipfile(zip_file):
        zf = zipfile.ZipFile(zip_file, "r")
        zf.extractall(test_case_dir)
        zf.close()
    test_case = os.path.join(test_case_dir, 'case.zip')
    shutil.copy(zip_file, test_case)
    
def problem_update(request):
    if request.method == 'GET':
        _problem_id = request.GET.get('problem_id', None)
        if _problem_id:
            pm = problem_model.objects.get(id=_problem_id) 
        else:
            pm = problem_model()
        difs = difficulty_model.objects.all()
        tags = tag_model.objects.all()
        langs = language_model.objects.all()
        pm_tags = []
        for tag in pm.tags.all():
            pm_tags.append(tag.id)
        pm_langs = []
        for lang in pm.languages.all():
            pm_langs.append(lang.id)
        return render(request, 'templates/problem_update.html',
                      {'page':'Problem Update',
                       'problem_id' : _problem_id,
                       'problem' : pm,
                       'problem_tags' : pm_tags,
                       'problem_languages' : pm_langs,
                       'difficulties' : difs,
                       'tags' : tags,
                       'languages' : langs})

    else:
        _problem_id = request.POST.get('problem_id', None)
        _title = request.POST.get('title', None)
        _description = request.POST.get('description', None)
        _time_limit = request.POST.get('time_limit', None)
        _memory_limit = request.POST.get('memory_limit', None)
        _difficulty = request.POST.get('difficulty', None)
        _tags = request.POST.getlist('tags')
        _tag_add = request.POST.get('tag_add', None)
        _languages = request.POST.getlist('languages')
        _can_exam = request.POST.getlist('can_exam')
        if _problem_id:
            pm = problem_model.objects.get(id=_problem_id)
        else:
            pm = problem_model()
        pm.tags.clear()
        pm.languages.clear()
        # add new tags
        _tag_add = _tag_add.split('|')
        if _tag_add[0] != '':
            for tag in _tag_add:
                try:
                    t = tag_model.objects.get(name=tag)
                except:
                    t = tag_model.objects.create(name=tag)
                pm.tags.add(t)

        # update problem
        pm.title = _title
        pm.description = _description
        pm.time_limit = _time_limit
        pm.memory_limit = _memory_limit
        pm.difficulty = difficulty_model.objects.get(id=_difficulty)
        for tag in _tags:
            pm.tags.add(tag_model.objects.get(id=tag))
        for language in _languages:
            pm.languages.add(language_model.objects.get(id=language))
        pm.can_exam = len(_can_exam) != 0
        pm.save()

        #update file
        inf = request.FILES.get("inputfile", None)
        if inf:
            tmp_dir = os.path.join(settings.TEST_CASE_DIR, "tmp")
            if not os.path.exists(tmp_dir):
                os.makedirs(tmp_dir)
            zip_file = os.path.join(tmp_dir, rand_str() + ".zip")
            with open(zip_file, "wb") as f:
                for chunk in inf:
                    f.write(chunk)
            process_zip(zip_file, pm.id)
            os.remove(zip_file)

        return redirect('/problem_list')

def deal_page(obj, page):
    paginator = Paginator(obj, 25)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    start_page_tab = contacts.number - 2
    end_page_tab = contacts.number + 2

    if start_page_tab < 1:
        start_page_tab = 1
        end_page_tab = 5

    if end_page_tab > paginator.num_pages:
        start_page_tab = paginator.num_pages - 4
        end_page_tab = paginator.num_pages

    if start_page_tab < 1:
        start_page_tab = 1

    page_list = []
    for i in range(start_page_tab, end_page_tab + 1):
        page_list.append(i)

    return contacts, page_list

@login_required(login_url="/login/")  
def problem_list(request):
    request.session.set_expiry(10800)
    if request.method == 'GET':
        _page = request.GET.get('page', 1)
        pms = problem_model.objects.all()
        contacts, page_list = deal_page(pms, _page)
        return render(request, 'templates/problem_list.html',
                          {'user' : request.user,
                           'contacts': contacts,
                           'page_list' : page_list})

@login_required(login_url="/login/")
def problem(request):
    request.session.set_expiry(10800)
    if request.method == 'GET':
        _problem_id = request.GET.get('problem_id', None)
        pm = problem_model.objects.get(id=_problem_id)
        return render(request, 'templates/problem.html',
                      {'user' : request.user,
                       'problem' : pm})


def problem_language(request):
    if request.method == 'POST':
        _problem_id = request.POST.get('problem_id', None)
        print(_problem_id)
        _lang = request.POST.get('lang', None)
        pm = problem_model.objects.get(id=_problem_id)
        test_case_dir = os.path.join(settings.TEST_CASE_DIR, str(pm.id))
        cnf = os.path.join(test_case_dir, _lang)
        with open(cnf, "r") as f:
            c = f.read()
        return HttpResponse(c)

def get_submission_json(sm):
    res = {}
    if sm == None:  
        res["id"] = -1
        res["state"] = -1
        res["res"] = 5
        res["cpu"] = 0
        res["memory"] = 0
    else:
        res["id"] = sm.id
        res["state"] = sm.state
        res["res"] = sm.res
        res["cpu"] = sm.cpu
        res["memory"] = sm.memory
    return json.dumps(res)

@login_required(login_url="/login/")
def problem_submit(request):
    request.session.set_expiry(10800)
    if request.method == 'POST':
        _user_id = request.user.id
        _problem_id = request.POST.get('problem_id', None)
        _examination_sub_id = request.POST.get('examination_sub_id', 0)
        _lang = request.POST.get('lang', None)
        _code = request.POST.get('code', None)

        if not _problem_id or not _lang or not _lang or not _code:
            sm = None
        else:
            sm = submission_model.objects.create(user_id = _user_id,
                                                 problem_id=_problem_id,
                                                 examination_sub_id=_examination_sub_id,
                                                 language=_lang,
                                                 code=_code,
                                                 state=0)        
        return HttpResponse(get_submission_json(sm))

@login_required(login_url="/login/")
def problem_view_submit(request):
    request.session.set_expiry(10800)
    if request.method == 'POST':
        _submission_id = request.POST.get('submission_id', None)
        sm = submission_model.objects.filter(id=_submission_id).first()
        return HttpResponse(get_submission_json(sm))

@login_required(login_url="/login/")  
def assignment(request):
    request.session.set_expiry(10800)
    if not request.user.is_staff:
        return redirect('/')
    return HttpResponse("assignment")

@login_required(login_url="/login/")  
def create_account(request):
    request.session.set_expiry(10800)
    if not request.user.is_staff:
        return redirect('/')
    return HttpResponse("create_account")

@login_required(login_url="/login/")  
def create_examination(request):
    request.session.set_expiry(10800)
    if not request.user.is_staff:
        return redirect('/')
    return HttpResponse("create_examination")
