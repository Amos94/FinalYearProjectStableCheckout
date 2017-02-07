from django.shortcuts import render
from taggy.modules.users import User as User

# Create your views here.

def index(request):
    pageName = "index"
    user = 'null'
    sessionId = 'null'

    if(user != 'null' and sessionId != 'null'):
        context = {"pageName":pageName, "sessionId":sessionId}
    else:
        context = {"pageName":pageName , "sessionId": 'not a valid session id'}

    return render(request,"index.html",context)

def about(request):
    pageName = "About"

    context = {"pageName":pageName}

    return render(request, "about.html", context)


def annotation(request):
    pageName = "Annotation"

    context = {"pageName":pageName}

    return render(request, "annotation.html", context)


def adjudication(request):
    pageName = "Adjudication"

    context = {"pageName":pageName}

    return render(request, "adjudication.html", context)