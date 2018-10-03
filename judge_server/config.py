default_max_cpu_time = 3000
default_max_real_time = 5000
default_max_memory = 128 * 1024
default_max_output_size = 10000
default_max_stack = 32 * 1024 * 1024

lang_config = {
    "c" : {
        "src_file" : "c/main.c",
        "compile" : "gcc c/main.c -o {src_file}",
        "exe_path" : "c/main",
        "args" : "",
        "rule" : "c_cpp"
        },
    "cpp" : {
        "src_file" : "cpp/main.cpp",
        "compile" : "g++ cpp/main.cpp -o {src_file}",
        "exe_path" : "cpp/main",
        "args" : "",
        "rule" : "c_cpp"
        },
    "cs" : {
        "src_file" : "cs/main.cs",
        "compile" : "mcs {src_file}",
        "exe_path" : "/usr/bin/mono",
        "args" : "cs/main.exe",
        "rule" : None
        },
    "java" : {
        "src_file" : "jav/Main.java",
        "compile" : "/usr/bin/javac {src_file}",
        "exe_path" : "/usr/bin/java",
        "args" : "-cp jav -XX:MaxRAM={max_memory}k -Djava.security.manager -Dfile.encoding=UTF-8 -Djava.security.policy==policy/java_policy -Djava.awt.headless=true Main",
        "rule" : None,
        "max_memory" : -1,
        "memory_limit_check_only" : 1
        },
    "py2" : {
        "src_file" : "py2/main.py",
        "compile" : "/usr/bin/python -m py_compile {src_file}",
        "exe_path" : "/usr/bin/python",
        "args" : "py2/main.pyc",
        "rule" : "general"
        },
    "py3" : {
        "src_file" : "py3/main.py",
        "compile" : "/usr/bin/python3 -m py_compile {src_file}",
        "exe_path" : "/usr/bin/python3",
        "args" : "py3/__pycache__/main.cpython-36.pyc",
        "rule" : "general"
        }
}

def get_max_cpu_time(max_cpu_time, cfg):
    if max_cpu_time == None:
        return default_max_cpu_time
    return max_cpu_time
    
def get_max_memory(max_memory, cfg):
    if cfg["max_memory"] != None:
        return cfg["max_memory"]
    if max_memory == None:
        return default_max_memory
    return max_memory

def get_memory_limit_check_only(cfg):
    if cfg["memory_limit_check_only"] != None:
        return cfg["memory_limit_check_only"]
    return 0
