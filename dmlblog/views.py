from django.shortcuts import render

def post_list(request):
    return render(request, 'dmlblog/post_list.html', {})
