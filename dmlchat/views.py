from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room

@login_required
def chat_main(request):
	rooms = Room.objects.order_by("title")
	context = {"rooms":rooms,}
	return render(request, 'user_list.html', context)


def chat_test(request):
	pass
