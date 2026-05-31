from django.http import HttpResponse, JsonResponse


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
