from django.shortcuts import render


def anonymousRedirect(request):
    return render(request, "AnonymousAlert.html")
