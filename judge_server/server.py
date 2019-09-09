import tornado.ioloop
import tornado.web
import json
import config
import os
import _judger

class ping_handler(tornado.web.RequestHandler):
    def get(self):
        self.write('pong')
        self.finish()

class judge_handler(tornado.web.RequestHandler):
    def post(self):
        try:
            case_in = []
            case_out = []
            for i in range(10):
                tcase_in = self.get_argument("case_in%d" % (i), None)
                tcase_out = self.get_argument("case_out%d" % (i), None)
                if tcase_in != None and tcase_out != None:
                    case_in.append(tcase_in)
                    case_out.append(tcase_out)
            src = self.get_argument("src", None)
            max_cpu_time = self.get_argument("max_cpu_time", None)
            max_cpu_time = int(max_cpu_time)
            max_memory = self.get_argument("max_memory", None)
            max_memory = int(max_memory)
            lang = self.get_argument("lang", None)

            if not lang in config.lang_config.keys():
                self.send_result(5, 0, 0)
                return
            cfg = config.lang_config[lang]

            input_path = os.path.join(config.default_dir, "1.in")
            output_path = os.path.join(config.default_dir, "1.out")
            error_path = os.path.join(config.default_dir, "1.error")
            log_path = os.path.join(config.default_dir, "judger.log")
            src_file = cfg["src_file"].format(ddir=config.default_dir)
            exe_path = cfg["exe_path"].format(ddir=config.default_dir)
            compile_cmd = cfg["compile_cmd"].format(src_file=src_file, exe_path=exe_path)
            args = cfg["args"].format(ddir=config.default_dir, max_memory=max_memory).split(" ")
            if args[0] == '':
                args = []
            print(input_path, output_path, error_path, log_path, src_file, exe_path)
            with open(src_file, "w", encoding="utf-8") as f:
                f.write(src)
            if os.system(compile_cmd):
                self.send_result(-2, 0, 0)
                return

            m_cpu_time = 0
            m_memory = 0
            max_cpu_time = config.get_max_cpu_time(max_cpu_time, cfg)
            max_memory = config.get_max_memory(max_memory, cfg)
            print(max_cpu_time)
            print(max_memory)
            for i in range(len(case_in)):
                with open(input_path, "w") as f:
                    f.write(case_in[i])

                run_result = _judger.run(max_cpu_time=max_cpu_time,
                                     max_real_time=config.default_max_real_time,
                                     max_memory=max_memory,
                                     max_stack=config.default_max_stack,
                                     max_output_size=config.default_max_output_size,
                                     max_process_number=200,
                                     exe_path=exe_path,
                                     input_path=input_path,
                                     output_path=output_path,
                                     error_path=error_path,
                                     args=args,
                                     env=[],
                                     log_path=log_path,
                                     seccomp_rule_name=cfg["rule"],
                                     uid=0,
                                     gid=0,
                                     memory_limit_check_only=config.get_memory_limit_check_only(cfg))

                m_cpu_time = m_cpu_time + run_result["cpu_time"]
                if run_result["memory"] > m_memory:
                    m_memory = run_result["memory"]
                if run_result["result"] == _judger.RESULT_SUCCESS:
                    if m_cpu_time > max_cpu_time:
                        self.send_result(1, m_cpu_time, m_memory)
                        return
                    if m_memory > max_memory and max_memory != -1:
                        self.send_result(3, m_cpu_time, m_memory)
                        return
                    with open(output_path, "r") as f:
                        content = f.read()
                        content = config.compare_output(content)
                        if content != case_out[i]:
                            self.send_result(-1, m_cpu_time, m_memory)
                            return
                else:
                    self.send_result(run_result["result"], m_cpu_time, m_memory)
                    return
                    
            self.send_result(0, m_cpu_time, m_memory)
        except Exception as e:
            print(e)
            self.send_result(5, 0, 0)

    def send_result(self, res, cpu, memory):
        result = {"result" : res, "cpu" : cpu, "memory" : memory}
        result = json.dumps(result)                         
        self.write(result)
        self.finish()                         

application = tornado.web.Application([
    (r"/ping", ping_handler),
    (r"/judge", judge_handler),
])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
