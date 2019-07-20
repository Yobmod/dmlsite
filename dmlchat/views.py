from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json

from .models import Room

from typing import Any, Dict


@login_required
def chat_main(request: HttpRequest) -> HttpResponse:
    """Main page of chats. Give list of avaiable rooms or allow user to create new room"""
    rooms = Room.objects.order_by("title")
    context: Dict[str, Any] = {"rooms": rooms, }
    return render(request, "dmlchat/chat_index.html", context)


def chat_room(request: HttpRequest, room_name: str) -> HttpResponse:
    context = {"room_name_json": mark_safe(json.dumps(room_name))}
    return render(request, "dmlchat/room.html", context)


# def chat_test(request):
# pass
