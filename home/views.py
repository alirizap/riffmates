from django.http import HttpResponse


def credits(request):
    content = "Nicky\nAlireza"
    return HttpResponse(content, content_type="text/plain")

def about(request):
    content = """
        <h1>About Page</h1>
        <p>A website for musicians!</p>
    """
    return HttpResponse(content, content_type="text/html")
