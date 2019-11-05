import json
import copy

from api import BaseRequestHandler
from common.logger import logger


class WebhookHandler(BaseRequestHandler):
    """
    吾来平台消息路由
    """

    async def post(self, *args, **kwargs):
        data = json.loads(self.request.body)

        # extra字段转化成json记录
        logger.warning(f"data: {data}")
        extra_str = data['msg_body']["extra"]
        # data_dp = copy.deepcopy(data)
        try:
            extra = json.loads(extra_str) if extra_str else {}
            tag = extra.get("qudao") + "_" + extra.get("time")
        except json.JSONDecodeError:
            tag = "通用"
            extra = {}
            logger.warning(f"extra格式有误: {extra_str}")
        # data_dp["msg_body"]["extra"] = extra

        logger.warning("==========================webhook=====================================")
        # 消息路由处理，v1
        suggested_response = data['bot_response']['suggested_response']
        for one in suggested_response:
            if one["is_send"] is True:
                groups = one["group"]
                for index, group in enumerate(groups):
                    # if group.get("group_name") == tag:
                    if index == 0:
                        one["response"] = group["response"]

        resp = {
            "suggested_response": suggested_response
        }
        logger.warning(f"resp: {resp}")

        return self.write(resp)
