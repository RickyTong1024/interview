import hashlib

default_max_cpu_time = 3000
default_max_real_time = 5000
default_max_memory = 128 * 1024
default_max_output_size = 10000
default_max_stack = 32 * 1024 * 1024

default_dir = "../execute"

lang_config = {
    "c" : {
        "src_file" : "{ddir}/c/main.c",
        "exe_path" : "{ddir}/c/main",
        "compile_cmd" : "gcc {src_file} -o {exe_path}",
        "args" : "",
        "rule" : "c_cpp"
        },
    "cpp" : {
        "src_file" : "{ddir}/cpp/main.cpp",
        "exe_path" : "{ddir}/cpp/main",
        "compile_cmd" : "g++ -std=c++11 {src_file} -o {exe_path}",
        "args" : "",
        "rule" : "c_cpp"
        },
    "cs" : {
        "src_file" : "{ddir}/cs/main.cs",
        "exe_path" : "/usr/bin/mono",
        "compile_cmd" : "mcs {src_file}",
        "args" : "{ddir}/cs/main.exe",
        "rule" : None,
        "max_memory" : -1,
        "memory_limit_check_only" : 1
        },
    "jav" : {
        "src_file" : "{ddir}/jav/Main.java",
        "exe_path" : "/usr/bin/java",
        "compile_cmd" : "/usr/bin/javac {src_file}",
        "args" : "-cp {ddir}/jav -XX:MaxRAM={max_memory}k -Djava.security.manager -Dfile.encoding=UTF-8 -Djava.security.policy==execute/policy/java_policy -Djava.awt.headless=true Main",
        "rule" : None,
        "max_memory" : -1,
        "memory_limit_check_only" : 1
        },
    "py2" : {
        "src_file" : "{ddir}/py2/main.py",
        "exe_path" : "/usr/bin/python",
        "compile_cmd" : "/usr/bin/python -m py_compile {src_file}",
        "args" : "{ddir}/py2/main.pyc",
        "rule" : "general"
        },
    "py3" : {
        "src_file" : "{ddir}/py3/main.py",
        "exe_path" : "/usr/bin/python3",
        "compile_cmd" : "/usr/bin/python3 -m py_compile {src_file}",
        "args" : "{ddir}/py3/__pycache__/main.cpython-36.pyc",
        "rule" : "general"
        }
}

def get_max_cpu_time(max_cpu_time, cfg):
    if max_cpu_time == None:
        return default_max_cpu_time
    return max_cpu_time
    
def get_max_memory(max_memory, cfg):
    if "max_memory" in cfg.keys():
        if cfg["max_memory"] == -1:
            return -1
        return cfg["max_memory"] * 1024
    if max_memory == None:
        return default_max_memory * 1024
    return max_memory * 1024

def get_memory_limit_check_only(cfg):
    if "memory_limit_check_only" in cfg.keys():
        return cfg["memory_limit_check_only"]
    return 0

def compare_output(s):
    output_md5 = hashlib.md5(s.encode("utf-8")).hexdigest()
    return output_md5
