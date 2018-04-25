from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json

#from .models import Room

# @login_required
def chat_main(request):
	#rooms = Room.objects.order_by("title")
	#context = {"rooms":rooms,}
	context = {}
	return render(request, 'dmlchat/chat_index.html', context)


def chat_room(request, room_name):
	context = 	{
        		'room_name_json': mark_safe(json.dumps(room_name))
    			}
	return render(request, 'dmlchat/room.html', context )


# def chat_test(request):
	# pass
