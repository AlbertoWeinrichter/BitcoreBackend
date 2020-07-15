from channels.routing import route

channel_routing = [
    route("websocket.connect", "API.notifications.channels.consumers.ws_add"),
    route("websocket.receive", "API.notifications.channels.consumers.ws_message"),
    route("websocket.disconnect", "API.notifications.channels.consumers.ws_disconnect"),
]
