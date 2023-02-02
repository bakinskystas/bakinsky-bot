import vk_api
import utils
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll, VkBotMessageEvent
from vk_api.longpoll import VkLongPoll, VkEventType
from dbconfig import User
from config import *

class MyLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print(e)

class Bot:
    def __init__(self):
        self.vk_session = vk_api.VkApi(token)
        self.longpoll = MyLongPoll(self.vk_session, 218106561)
    def run (self):        
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.object.message
                user_id = msg['from_id']
                user = utils.get_user_by_id(user_id)
                mess = msg['text']
                fwd = self.vk_session.method('messages.getByConversationMessageId', {'conversation_message_ids': msg['conversation_message_id'],'peer_id': msg['peer_id']})['items'][0]
                if 'reply_message' in fwd:
                    fwd = fwd['reply_message']
                else:
                    fwd = None

                if user.admin >= 1:
                    if fwd:
                        if mess == 'warn':
                            user_id = msg['from_id']
                            fwd_user = utils.get_user_by_id(fwd['from_id'])
                            fwd_user.warns += int(1)
                            fwd_user.save()
                            user_name = self.vk_session.method('users.get', {'user_id': fwd_user.vk_id})[0]['first_name']
                            self.vk_session.method('messages.send', {'chat_id': msg['peer_id']-2000000000, 'message': f'{user_name}, вам выдано предупреждение!\nВсего предупреждений: {fwd_user.warns}/3', 'random_id': 0})
                            if fwd_user.warns >= int(3):
                                self.vk_session.method('messages.removeChatUser', {'user_id': fwd_user.vk_id, 'chat_id': msg['peer_id']-2000000000})
                                fwd_user.warns -= int(3)
                                fwd_user.save()
                        elif mess == 'unwarn':
                            if(fwd_user.warns != int(0)):
                                fwd_user = utils.get_user_by_id(fwd['from_id'])
                                fwd_user.warns -= int(1)
                                fwd_user.save()
                                user_name = self.vk_session.method('users.get', {'user_id': fwd_user.vk_id})[0]['first_name']
                                self.vk_session.method('messages.send', {'chat_id': msg['peer_id']-2000000000, 'message': f'{user_name}, вам снято одно предпреждение!\nВсего предупреждений: {fwd_user.warns}/3', 'random_id': 0})
                            else:
                                user_name = self.vk_session.method('users.get', {'user_id': fwd_user.vk_id})[0]['first_name']
                                self.vk_session.method('messages.send', {'chat_id': msg['peer_id']-2000000000, 'message': f'{user_name}, у вас не варнов', 'random_id': 0})
                        elif mess == 'warns':
                            fwd_user = utils.get_user_by_id(fwd['from_id'])
                            user_name = self.vk_session.method('users.get', {'user_id': fwd_user.vk_id})[0]['first_name']
                            self.vk_session.method('messages.send', {'chat_id': msg['peer_id']-2000000000, 'message': f'У пользователя {user_name} - {fwd_user.warns}/3 предупреждений', 'random_id': 0})
                if user.admin >= int(2):
                    if fwd:
                        if mess == 'kick':
                            self.vk_session.method('messages.removeChatUser', {'user_id': fwd['from_id'], 'chat_id': msg['peer_id']-2000000000})
                            fwd_user = utils.get_user_by_id(fwd['from_id'])
                            if(fwd_user.warns != int(0)):
                                fwd_user.warns -= int(3)
                                fwd_user.save()
                if user.admin >= int(3):
                      if fwd:
                        if mess == 'admin':
                            fwd_user = utils.get_user_by_id(fwd['from_id'])
                            fwd_user.admin += int(1)
                            fwd_user.save()
                            user_name = self.vk_session.method('users.get', {'user_id': fwd_user.vk_id})[0]['first_name']
                            self.vk_session.method('messages.send', {'chat_id': msg['peer_id']-2000000000, 'message': f'{user_name}, вам добавлен один уровень админки', 'random_id': 0})
                        elif mess == 'unadmin':
                            fwd_user = utils.get_user_by_id(fwd['from_id'])
                            fwd_user.admin -= int(1)
                            fwd_user.save()
                            user_name = self.vk_session.method('users.get', {'user_id': fwd_user.vk_id})[0]['first_name']
                            self.vk_session.method('messages.send', {'chat_id': msg['peer_id']-2000000000, 'message': f'{user_name}, вам снят один уровень админки', 'random_id': 0})
                        elif mess == 'admins':
                            fwd_user = utils.get_user_by_id(fwd['from_id'])
                            user_name = self.vk_session.method('users.get', {'user_id': fwd_user.vk_id})[0]['first_name']
                            self.vk_session.method('messages.send', {'chat_id': msg['peer_id']-2000000000, 'message': f'У {user_name} - {fwd_user.admin} уровень админки', 'random_id': 0})

if __name__ == '__main__':
    Bot().run()
