import _judger
import sys
import os

def do_c():
    if os.system("gcc c/main.c -o c/main"):
        print("compile error")
        exit(1)

    ret = _judger.run(max_cpu_time=1000,
                      max_real_time=2000,
                      max_memory=128 * 1024 * 1024,
                      max_process_number=200,
                      max_output_size=10000,
                      max_stack=32 * 1024 * 1024,
                      exe_path="c/main",
                      input_path="1.in",
                      output_path="c/1.out",
                      error_path="c/1.error",
                      args=[],
                      env=[],
                      log_path="c/judger.log",
                      seccomp_rule_name="c_cpp",
                      uid=0,
                      gid=0)
    print(ret)

def do_cpp():
    if os.system("g++ cpp/main.cpp -o cpp/main"):
        print("compile error")
        exit(1)

    ret = _judger.run(max_cpu_time=1000,
                      max_real_time=2000,
                      max_memory=128 * 1024 * 1024,
                      max_process_number=200,
                      max_output_size=10000,
                      max_stack=32 * 1024 * 1024,
                      exe_path="cpp/main",
                      input_path="1.in",
                      output_path="cpp/1.out",
                      error_path="cpp/1.error",
                      args=[],
                      env=[],
                      log_path="cpp/judger.log",
                      seccomp_rule_name="c_cpp",
                      uid=0,
                      gid=0)
    print(ret)

def do_cpp():
    if os.system("g++ cpp/main.cpp -o cpp/main"):
        print("compile error")
        exit(1)

    ret = _judger.run(max_cpu_time=1000,
                      max_real_time=2000,
                      max_memory=128 * 1024 * 1024,
                      max_process_number=200,
                      max_output_size=10000,
                      max_stack=32 * 1024 * 1024,
                      exe_path="cpp/main",
                      input_path="1.in",
                      output_path="cpp/1.out",
                      error_path="cpp/1.error",
                      args=[],
                      env=[],
                      log_path="cpp/judger.log",
                      seccomp_rule_name="c_cpp",
                      uid=0,
                      gid=0)
    print(ret)

def do_cs():
    if os.system("mcs cs/main.cs"):
        print("compile error")
        exit(1)

    ret = _judger.run(max_cpu_time=1000,
                      max_real_time=2000,
                      max_memory=128 * 1024 * 1024,
                      max_process_number=200,
                      max_output_size=10000,
                      max_stack=32 * 1024 * 1024,
                      exe_path="/usr/bin/mono",
                      input_path="1.in",
                      output_path="cs/1.out",
                      error_path="cs/1.error",
                      args=["cs/main.exe"],
                      env=[],
                      log_path="cs/judger.log",
                      seccomp_rule_name=None,
                      uid=0,
                      gid=0)
    print(ret)
    
def do_java():
    if os.system("/usr/bin/javac jav/Main.java"):
        print("compile error")
        exit(1)

    ret = _judger.run(max_cpu_time=1000,
                      max_real_time=2000,
                      max_memory=-1,
                      max_process_number=200,
                      max_output_size=10000,
                      max_stack=32 * 1024 * 1024,
                      memory_limit_check_only=1,
                      exe_path="/usr/bin/java",
                      input_path="1.in",
                      output_path="jav/1.out",
                      error_path="jav/1.error",
                      args=["-cp", "jav", "-XX:MaxRAM=131072k", "-Djava.security.manager", "-Dfile.encoding=UTF-8", "-Djava.security.policy==/etc/java_policy", "-Djava.awt.headless=true", "Main"],
                      env=[],
                      log_path="jav/judger.log",
                      seccomp_rule_name=None,
                      uid=0,
                      gid=0)
    print(ret)

def do_py2():
    if os.system("/usr/bin/python -m py_compile py2/main.py"):
        print("compile error")
        exit(1)

    ret = _judger.run(max_cpu_time=1000,
                      max_real_time=2000,
                      max_memory=128 * 1024 * 1024,
                      max_process_number=200,
                      max_output_size=10000,
                      max_stack=32 * 1024 * 1024,
                      exe_path="/usr/bin/python",
                      input_path="1.in",
                      output_path="py2/1.out",
                      error_path="py2/1.error",
                      args=["py2/main.pyc"],
                      env=[],
                      log_path="py2/judger.log",
                      seccomp_rule_name="general",
                      uid=0,
                      gid=0)
    print(ret)

def do_py3():
    if os.system("/usr/bin/python3 -m py_compile py3/main.py"):
        print("compile error")
        exit(1)

    ret = _judger.run(max_cpu_time=1000,
                      max_real_time=2000,
                      max_memory=128 * 1024 * 1024,
                      max_process_number=200,
                      max_output_size=10000,
                      max_stack=32 * 1024 * 1024,
                      exe_path="/usr/bin/python3",
                      input_path="1.in",
                      output_path="py3/1.out",
                      error_path="py3/1.error",
                      args=["py3/__pycache__/main.cpython-36.pyc"],
                      env=[],
                      log_path="py3/judger.log",
                      seccomp_rule_name="general",
                      uid=0,
                      gid=0)
    print(ret)

if __name__ == '__main__':
    l = len(sys.argv)
    if l >= 2:
        cmd = sys.argv[1]
        if cmd == 'c':
            do_c()
        elif cmd == 'cpp':
            do_cpp()
        elif cmd == 'cs':
            do_cs()
        elif cmd == 'java':
            do_java()
        elif cmd == 'py2':
            do_py2()
        elif cmd == 'py3':
            do_py3()
