import json
import traceback
import tornado.web

from common.logger import logger


# from conf.config import DEBUG


class BaseRequestHandler(tornado.web.RequestHandler):

    # def __init__(self, application, request, **kwargs):
    #     super().__init__(application, request, **kwargs)
    #     self._operator_name = 'No_Login'

    def write_error(self, status_code, **kwargs):
        """
        改写原功能
        :param status_code:
        :param kwargs:
        :return:
        """
        # if not DEBUG:
        try:
            if status_code >= 500:
                # subject = "【prod】灵刻实业汽车零配件信息查询机器人-报警提醒"
                exc_info = kwargs.get('exc_info')
                msg = "".join(traceback.format_exception(*exc_info))
                logger.error(msg)
                # logger.info(msg)
                # pool = self.__class__.TASK_POOL
                # pool.submit(send_log, subject, msg)
        except Exception:
            msg = traceback.format_exc()
            logger.warning(msg)
        super().write_error(status_code, **kwargs)

    def set_default_headers(self):
        """
        跨域
        :return:
        """
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    # def _request_summary(self):
    #     """自定义日志记录内容"""
    #     return "%s %s %s(%s@%s)" % (self.request.method, self.request.uri, self.request.body.decode(),
    #                                 self._operator_name, self.request.remote_ip)
    def get_current_user(self):
        self.current_user = self.get_secure_cookie("userid", max_age_days=1)
        # print(f"current_user: {self.current_user}")
        if isinstance(self.current_user, bytes):
            return self.current_user.decode()
        return self.current_user

    async def proxy_real_request(self, status_code, resp):
        if status_code == 200:
            return self.write(resp)
        else:
            self.set_status(status_code)
            if isinstance(resp, dict):
                return self.finish(resp)
            else:
                if resp:
                    return self.finish({"msg": resp})
                else:
                    return self.finish({"msg": "unknown error."})


class QueryBlock(BaseRequestHandler):
    """询问单元 数据源 url"""

    NLG_ENTER_REPLACE = '\\n'

    def make_response(self, slots: list, nlg: str):
        """
        构造接口响应
        :param slots: 词槽值动态数据, 可作为快捷回复
        :param nlg: 机器人提问的文本, 文本内`\n`无法识别需要转换
        :return:
        """
        content = nlg.replace('\n', self.NLG_ENTER_REPLACE)
        content = json.dumps({"Content": content}, ensure_ascii=False)
        return {
            "nlg": content,
            "results": slots
        }


class APIBlock(BaseRequestHandler):
    """接口单元"""

    def make_response(self, slots: list, nlg_list=None):
        """
        构造接口响应
        :param slots: 返回给词槽的值列表
        :return:
        """
        key_res = slots
        # pattern = {i: i for i in slots}
        if not nlg_list:
            nlg_list = []
        return {
            "nlg_list": nlg_list,
            "key_res": key_res,
            "pattern": {},
        }


class AdvancedAPIBlock(BaseRequestHandler):
    """高级接口单元"""

    def make_response(self, slots: dict, *args, error_no=0, responses=None, **kwargs):
        """
        构造接口响应
        :param slots: 返回给词槽的值字典
        :return:
        """
        res_num = len(slots)
        slots = [
            {
                "name": name, "value": value
            } for name, value in slots.items()
        ]
        return {
            "error_no": error_no,
            "slots": slots,
            "responses": responses if responses else []
        }


class QueryBlockCase(QueryBlock):
    """询问单元 数据源 URL"""

    async def get(self, *args, **kwargs):
        response = self.make_response(['1', '2', '3'], '你好啊')
        return self.write(response)


class APIBlockCase(APIBlock):
    """接口单元"""

    async def get(self, *args, **kwargs):
        response = self.make_response(['true'])
        return self.write(response)


class AdvancedAPIBlockCase(AdvancedAPIBlock):
    """高级接口单元"""

    async def get(self, *args, **kwargs):
        slots = {
            "slot1": "value1",
            "slot2": "value2",
        }
        response = self.make_response(slots)
        return self.write(response)
