import urllib
import httplib2
import hashlib

def compare_output(s):
    output_md5 = hashlib.md5(s.encode("utf-8")).hexdigest()
    return output_md5
    
content = ""
with open("../judge/test/py3/main.py", "r") as f:
    content = f.read()
                    
test_data = {
    'src' : content,
    'case_in0' : '1 2',
    'case_out0' : compare_output('3\n'),
    'lang' : 'py3'
    }
body = urllib.parse.urlencode (test_data)
conn = httplib2.Http("")
resp, content = conn.request("http://47.99.138.90:8080/judge", "POST", body, headers={'Content-Type': 'application/x-www-form-urlencoded'}) 
print(content)
