from django.http import HttpResponse


def credits(request):
    content = "Nicky\nAlireza"
    return HttpResponse(content, content_type="text/plain")

