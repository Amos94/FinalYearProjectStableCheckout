from django.shortcuts import render
from Taggy.modules.users import User as User

# Create your views here.

def index(request):

    pageName = "Index"
    user = 'null'
    sessionId = 'null'


    if(user != 'null' and sessionId != 'null'):
        context = {"pageName":pageName, "user":user, "sessionId":sessionId}
    else:
        context = {"pageName": pageName, "user": user, "sessionId": sessionId}

    return render(request, 'index.html', context)