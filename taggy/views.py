from django.shortcuts import render
from taggy.modules.users import User as User

# Create your views here.

def index(request):
    pageName = "index"
    user = 'null'
    sessionId = 'null'

    if(user != 'null' and sessionId != 'null'):
        context = {"pageName":pageName, "user":user, "sessionId":sessionId}
    else:
        context = {"pageName":pageName , "user": 'not an user', "sessionId": 'not a valid session id'}

    return render(request,"index.html",context)