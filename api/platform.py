import json
import copy

from api import BaseRequestHandler
from common.logger import logger
from common.async_db import get_mongo_db
from conf.config import mongo_uri, mongo_db


class WebhookHandler(BaseRequestHandler):
    """
    吾来平台消息路由
    """

    async def post(self, *args, **kwargs):
        # mongo
        mongo_collection = "webhook_record"
        m_db = get_mongo_db(mongo_uri, mongo_db)
        m_col = m_db[mongo_collection]

        data = json.loads(self.request.body)

        if data.get("bot_response"):
            version = "v1"
        else:
            version = "v2"

        data["version"] = version
        data["scene"] = "request"
        await m_col.insert_one(data)

        # 消息路由处理，v1
        if version == "v1":
            suggested_response = data['bot_response']['suggested_response']

            resp = {
                "suggested_response": suggested_response
            }
        else:
            is_dispatch = data["is_dispatch"]
            suggested_response = data['suggested_response']
            extra = data["extra"]
            resp = {
                "is_dispatch": is_dispatch,
                "suggested_response": suggested_response,
                "extra": extra
            }
        resp["version"] = version
        resp["scene"] = "response"
        await m_col.insert_one(resp)

        return self.write(resp)
