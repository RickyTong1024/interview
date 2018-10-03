import tornado.ioloop
import tornado.web
import json
import config

class ping_handler(tornado.web.RequestHandler):
    def get(self):
        self.write('pong')
        self.finish()

class judge_handler(tornado.web.RequestHandler):
    def post(self):
        case_in = []
        case_out = []
        for i in range(10):
            tcase_in = self.get_argument("case_in%d" % (i))
            tcase_out = self.get_argument("case_out%d" % (i))
            if tcase_in != None and tcase_out != None:
                case_in.append(tcase_in)
                case_out.append(tcase_out)
        src = self.get_argument("src")
        max_cpu_time = self.get_argument("max_cpu_time")
        max_memory = self.get_argument("max_memory")
        lang = self.get_argument("lang")
        
        cfg = config.lang_config[lang]
        if cfg == None:
            self.send_result(5, 0, 0)
            return
        
        with open(cfg["src_file"], "w", encoding="utf-8") as f:
            f.write(src)

        compile_command = cfg["compile"]
        compile_command = compile_command.format(src_file=cfg["src_file"])
        if os.system(compile_command):
            self.send_result(-2, 0, 0)
            return

        args = cfg["args"].format(max_memory=max_memory).split(" ")

        max_cpu_time = 0
        max_memory = 0
        for i in range(len(case_in)):
            with open("1.in", "w") as f:
                f.write(case_in[i])
            run_result = _judger.run(max_cpu_time=config.get_max_cpu_time(max_cpu_time, cfg),
                                 max_real_time=config.default_max_real_time,
                                 max_memory=config.get_max_memory(max_memory, cfg),
                                 max_stack=config.default_max_stack,
                                 max_output_size=config.default_max_output_size,
                                 max_process_number=_judger.UNLIMITED,
                                 exe_path=cfg["exe_path"],
                                 input_path="1.in",
                                 output_path="1.out",
                                 error_path="1.error",
                                 args=args,
                                 env=[],
                                 log_path="judger.log",
                                 seccomp_rule_name=cfg["rule"],
                                 uid=0,
                                 gid=0,
                                 memory_limit_check_only=config.get_memory_limit_check_only(cfg))
            max_cpu_time = max_cpu_time + run_result["cpu_time"]
            if run_result["memory"] > max_memory:
                max_memory = run_result["memory"]
            if run_result["result"] == _judger.RESULT_SUCCESS:
                with open("1.out", "r", encoding="utf-8") as f:
                    content = f.read()
                    if content != case_out[i]:
                        self.send_result(-1, max_cpu_time, max_memory)
                        return
            else:
                self.send_result(run_result["result"], max_cpu_time, max_memory)
                return
        self.send_result(0, max_cpu_time, max_memory)

    def send_result(self, res, cpu, memory):
        result = {"result" : res, "cpu" : cpu, "memory" : memory}
        result = json.dump(result)                         
        self.write(result)
        self.finish()                         

application = tornado.web.Application([
    (r"/ping", ping_handler),
    (r"/judge", judge_handler),
])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
