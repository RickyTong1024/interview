from django.shortcuts import render, redirect
from django.http import HttpResponse
from interview.models import *
import os, shutil
import random
import zipfile
from django.conf import settings

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
        return render(request, 'templates/problem_update.html', {'problem_id' : _problem_id,
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
    
def problem_list(request):
    return HttpResponse("problem_list")

def problem(request):
    if request.method == 'GET':
        _problem_id = request.GET.get('problem_id', None)
        pm = problem_model.objects.get(id=_problem_id)
        return render(request, 'templates/problem.html', {'problem' : pm})


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

def problem_submit(request):
    if request.method == 'POST':
        _problem_id = request.POST.get('problem_id', None)
        _lang = request.POST.get('lang', None)
        _code = request.POST.get('code', None)
        
        return HttpResponse("problem_submit")
