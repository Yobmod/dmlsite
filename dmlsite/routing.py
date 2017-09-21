from channels.routing import route
from dmlchat.consumers import ws_connect, ws_message, ws_disconnect#, http_consumer


channel_routing = [
	#route("http.request", http_consumer),
	route('websocket.connect', ws_connect),
	route('websocket.connect', ws_message),
	route('websocket.disconnect', ws_disconnect),

]
