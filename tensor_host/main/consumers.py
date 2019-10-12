from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class CaptureLogging(WebsocketConsumer):
    """ Establishes the broadcast websocket for the entire application"""
    def connect(self):
        """ Join layer group """
        async_to_sync(self.channel_layer.group_add)('broadcast', self.channel_name)
        self.accept()
        print("Connecting")

    def disconnect(self, code):
        """ Leave layer group """
        async_to_sync(self.channel_layer.group_discard)('broadcast', self.channel_name)
        print("Disconnecting")

    def logging_event(self, event):
        """ Publish group message to client """
        self.send(text_data=event['data'])
        print("Event")
