import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
import subprocess
from subprocess import PIPE, Popen
#https://www.youtube.com/watch?v=F4nwRQPXD8w

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'tester_message',
                'tester' : 'WebSocket establish',
            }
        )

    async def tester_message(self, event):
        tester = event['tester']
        print ("{} \n".format(tester))

        await self.send(text_data=json.dumps({
            'tester' : tester,
        }))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print ("Recieve by user {}".format(message))
        sms = message.split(',')
        #https://www.programmersought.com/article/31502607463/
        p = Popen(
            ["/usr/bin/python","/Users/kenny/Documents/tool_dir/test/python-smpplib/runner2.py", 
                "{}".format(sms[0]), 
                "{}".format(sms[1]), 
                "{}".format(sms[2]), 
                "{}".format(sms[3]),
                "{}".format(sms[4]),  
                "{}".format(sms[5])], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                encoding="gbk", universal_newlines=True
                )
        output, errors = p.communicate()
        output2 = []
        try:
                 output1 = output.split(',')
                #  print ("kdddd {}".format(output1))
        except:
            pass


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chatroom_message',
                'message' : output,
            }
        )
        
    async def chatroom_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message' : message,
        }))