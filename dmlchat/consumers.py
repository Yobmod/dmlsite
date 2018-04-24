"""from django.http import HttpResponse.

# from channels.handler import AsgiHandlee
# def http_consumer(message):
# 	# Make standard HTTP response - access ASGI path attribute directly
# 	response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
Encode that response into message format (ASGI)
for chunk in AsgiHandler.encode_response(response):
message.reply_channel.send(chunk)
"""
from channels import Group
from channels.auth import channel_session_user_from_http


@channel_session_user_from_http
def ws_connect(message):
	message.reply_channel.send({"accept": True})
	message.channel_session['rooms'] = []
	Group('chat').add(message.reply_channel)


def ws_message(message):
	Group("chat").send({
			"text": "[user] %s" % message.content['text'],
			# "text": f"[user] {message.content['text']}"
	})

def ws_disconnect(message):
	Group('chat').discard(message.reply_channel)
