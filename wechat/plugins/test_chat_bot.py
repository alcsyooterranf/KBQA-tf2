from classes import Message
from monitor.plugin.on import on_command
from modules import chitchat_bot, medical_bot, classifier
from utils.json_utils import dump_user_dialogue_context, load_user_dialogue_context
import re

# priority 为优先级，数值越低优先级越高，block 是否阻断消息继续传递，默认 True，为 False 时还需继续传递至下一层事件处理
chatbot = on_command("开始问诊", priority=3, block=True)


@chatbot.handle()
async def handle_first_message(message: Message):
    data = message.data
    message = data['msg']
    print("message = ", message)
    user = data['from_wxid']
    print("user:{}, message:{}".format(user, message))
    await chatbot.pause("你好，我是您的智能问诊机器人，很开心为您服务！")


@chatbot.handle()
async def handle_message(message: Message):
    data = message.data
    message = data['msg']
    user = data['from_wxid']
    print("user:{}, message:{}".format(user, message))
    # 判断用户意图是否属于闲聊类，相当于第一层意图过滤
    user_intent = classifier(message)
    print("user_intent:", user_intent)
    if user_intent == "goodbye":
        reply = chitchat_bot(user_intent)
        await chatbot.finish(reply)
    elif user_intent in ["greet", "deny", "isbot"]:
        reply = chitchat_bot(user_intent)
    elif user_intent == "accept":
        reply = load_user_dialogue_context(user)
        reply = reply.get("choice_answer")
        print("01-accept:", reply)
    # diagnosis
    else:
        reply = medical_bot(message, user)
        if reply["slot_values"]:
            dump_user_dialogue_context(user, reply)
        reply = reply.get("replay_answer")
    print("reply:", reply)
    replys = split_by_number_of_words(reply, 70)
    for reply in replys:
        await chatbot.reject(reply)
    # await chatbot.reject()


def split_by_number_of_words(s, n):
    pieces = s.split()
    return [" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n)]
