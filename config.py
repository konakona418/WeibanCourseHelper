from configparser import *


class Conf:
    # Common
    DEBUG = True
    IGNORE_FINISHED_TASKS = False
    MAX_TASK_NUM = 8
    DEBUG_PRINT_MAX_LEN = 65535
    LEARN_TIMEOUT = 16

    # Network Service
    JQUERY_VER = "3.4.1"
    MY_CAPTCHA = "ba95ef14-d7dd-4d7b-8ec5-189d33b3a6d8"
    CAPTCHA_CRACK_MAX_ITER = 256

    # Cryptography
    KEY_SZ = 128
    KEY: bytes = "wbs512".encode("utf-8").ljust(KEY_SZ // 8, b"\x00")
    IV = b""

    def parse_conf(self):
        conf: ConfigParser = ConfigParser()
        conf.read("./config.ini")

        if conf.has_section("Common"):
            self.DEBUG = conf.getboolean("Common", "debug")
            self.IGNORE_FINISHED_TASKS = conf.getboolean("Common", "ignore_finished_tasks")
            self.MAX_TASK_NUM = conf.getint("Common", "max_task_num")
            self.DEBUG_PRINT_MAX_LEN = conf.getint("Common", "debug_print_max_len")
            self.LEARN_TIMEOUT = conf.getfloat("Common", "learn_timeout")

        if conf.has_section("Network"):
            self.JQUERY_VER = conf.get("Network", "jquery_ver")
            self.MY_CAPTCHA = conf.get("Network", "my_captcha")
            self.CAPTCHA_CRACK_MAX_ITER = conf.get("Network", "captcha_crack_max_iter")

        return self


config_instance: Conf = Conf().parse_conf()
