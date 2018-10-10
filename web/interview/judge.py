from interview.models import *
from django.conf import settings
import os
import urllib
import httplib2
import hashlib
import json

def compare_output(s):
    output_md5 = hashlib.md5(s.encode("utf-8")).hexdigest()
    return output_md5

def judge():
    sm = submission_model.objects.filter(state__lte=1).order_by('id').first()
    if sm:
        sm.state = 1
        sm.save()

        test_data = {
            'src' : sm.code,
            'lang' : sm.language,
            }
        test_case_dir = os.path.join(settings.TEST_CASE_DIR, str(sm.problem_id))
        info_file = os.path.join(test_case_dir, 'info')
        with open(info_file, "r") as f:
            content = f.readline()
            num = int(content)
        for i in range(num):
            j = i + 1
            in_file = os.path.join(test_case_dir, str(j) + '.in')
            with open(in_file, "r") as f:
                content_in = f.read()
            out_file = os.path.join(test_case_dir, str(j) + '.out')
            with open(out_file, "r") as f:
                content_out = f.read()
                content_out = compare_output(content_out)
            test_data['case_in' + str(i)] = content_in
            test_data['case_out' + str(i)] = content_out

        body = urllib.parse.urlencode (test_data)
        conn = httplib2.Http("")
        resp, content = conn.request(settings.JUDGE_SERVER + "judge", "POST", body, headers={'Content-Type': 'application/x-www-form-urlencoded'}) 
        content = json.loads(content)

        sm.state = 2
        sm.res = content['result']
        sm.cpu = content['cpu']
        sm.memory = content['memory']
        sm.save()

        problem = problem_model.objects.filter(id=sm.problem_id).first()
        if problem:
            problem.add_submission_number()
            if sm.res == 0:
                problem.add_ac_number()       
        examination_sub = examination_sub_model.objects.filter(id=sm.examination_sub_id).first()
        if examination_sub:
            examination_sub.submissions.add(sm)
            if examination_sub.result != 0 and sm.res == 0:
                examination_sub.result = 0
            examination_sub.save()
