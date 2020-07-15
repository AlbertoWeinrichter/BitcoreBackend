from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from slugify import slugify


class WebsocketConsumer(JsonWebsocketConsumer):

    def connect(self):
        async_to_sync(self.accept())
        async_to_sync(self.send_json({
            'type': 'welcome',
            'data': 'Socket connection started with backend',
        }))

        # create a channel group for this user based on username
        query_string = self.scope.get('query_string').decode("utf-8")
        params = {
            s.split('=')[0]: s.split('=')[1] for s in query_string.split('&')
        }
        username = slugify(params.get('username'))
        async_to_sync(self.channel_layer.group_add)(username, self.channel_name)

    def disconnect(self, username):
        pass
        # TODO: how to close old channels? is it even needed?
        # async_to_sync(self.channel_layer.group_discard)(slugify(username), self.channel_name)

    def message(self, event):
        self.send_json(event)
