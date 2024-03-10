import sys
import warnings

from argparse import ArgumentParser
from cgitb import handler

import pymongo
import json

from flask import Flask, request, abort, json
from linebot import LineBotApi, LineBotSdkDeprecatedIn30
from linebot.v3 import (
    WebhookHandler
)

from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage, PushMessageRequest
)


class MessageDto:
    def __init__(self, **kwargs):
        self.user_name = kwargs.get("user_name")
        self.user_id = kwargs.get("user_id")
        self.message_text = kwargs.get("message_text")

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(**dict_obj)


app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = 'bd46caef29e861da397adb5479804435'
channel_access_token = '/a32rgsFiJA1tE//4g6iwCmlXZ53gH4ItGy969YMlBMQdMDnlssyOx4OzoZNLrMKED9hbt5doBhyHF54nulxVQC/fH3hprToFzSPSfNKlNeFzByDQsuNBHZagIOD7DPQEPzFNqKbWl8GSzgC/ZQpEAdB04t89/1O/w1cDnyilFU='
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)  # handler

configuration = Configuration(  # line_bot_api
    access_token=channel_access_token
)

# mongodb connection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["message"]
mycol = mydb["line_message"]


def upload(messagedto):
    print("write to mongoDB")
    mycol.insert_one(messagedto)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        profile = line_bot_api.get_profile(user_id=event.source.user_id)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )
        message_dto = MessageDto.from_dict({'user_name': profile.display_name,
                                            'user_id': profile.user_id,
                                            'message_text': event.message.text})

        upload(message_dto.to_dict())


@app.route('/get_message', methods=['GET', 'POST'])  # get list of message from user
def getuser():
    query2 = mycol.aggregate(
        [
            {'$group': {
                "_id": "$user_name",
                "message_text": {'$addToSet': '$message_text'}
            }}
        ]
    )
    list_query = list(query2)
    return json.dumps(list_query, ensure_ascii=False).encode('utf8')


@app.route('/send', methods=['POST'])  # sending message to line
def send():
    user_id = request.args.get("user_id")
    message = request.args.get("message")
    with ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = MessagingApi(api_client)
        push_message_request = PushMessageRequest(
            to=user_id,
            messages=[TextMessage(text=message)],
        )
        try:
            api_instance.push_message(push_message_request)
            return {"user_id": user_id, "text": message}
        except Exception as e:
            print("Exception when calling MessagingApi->push_message: %s\n" % e)
            return "error"


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    warnings.filterwarnings("ignore", category=LineBotSdkDeprecatedIn30)

    app.run(debug=options.debug, port=options.port)
