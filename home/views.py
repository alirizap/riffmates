from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def credits(request):
    content = "Nicky\nAlireza"
    return HttpResponse(content, content_type="text/plain")

def about(request):
    content = """
        <h1>About Page</h1>
        <p>A website for musicians!</p>
    """
    return HttpResponse(content, content_type="text/html")

def info(request):
    content = {'version': '0.0.1'}
    return JsonResponse(content)

def news(request):
    data = {
        "news": [
            "RiffMates now has a new page",
            "RiffMates has its first web page",
        ]
    }

    return render(request, "news2.html", data)
