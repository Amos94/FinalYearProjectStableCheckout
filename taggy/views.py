from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import resolve
from django.utils.six.moves.urllib.parse import urlparse
from forms import CreateSet, UpdateSet
from taggy.modules.Queries import Queries
from taggy.modules.users import User as User
from taggy.modules.HelperMethods import HelperMethods

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

def setCreate(request):
    pageName = "Create Set"
    sessionId = 'null'
    userid = 0
    qry = Queries()
    context = {"pageName": pageName, "sessionId": sessionId}
    if(request.method == 'POST'):
        #TO CHANGE THE USER WHEN THE USER ROLE IS READY
        form = CreateSet(request.POST)
        if(form.is_valid()):
            setname = form.cleaned_data['setname']
            setdescr = form.cleaned_data['setdescr']
            result = qry.insertSet(setname, setdescr, userid)

            if(result == 1):
                return HttpResponseRedirect('/success/')
            else:
                return HttpResponseRedirect('/fail/')


    else:
        form = CreateSet()


    return render(request, "create_set.html", {'form':form})

def editSet(request, setid=-1):
    pageName = 'Edit Set'
    userType = "ADMIN_TYPE"
    userId = 1
    postCase = 0

    qry = Queries()

    if(request.method == 'GET'):

        if(request.get_full_path() != '/set/edit/'):
            path = request.get_full_path()
            setid = path.split('/set/edit/')[1]
            setid = setid.rstrip('/')

    if(setid == -1):
        if(userType == "ADMIN_TYPE"):
            results = qry.getSets()
        else:
            results = qry.getSetsByCreator(userId)
    elif(request.POST.get('updateset')):
        results = qry.getSetMeta(setid)
        setname = results[1]
        qry.updateSet(setid, request.POST.get('updateset'))
        results = qry.getSet(setid)

        postCase = 1
    else:
        results = qry.getSetMeta(setid)
        setname = results[1]
        results = qry.getSet(setid)
        updateset = ""
        for result in results:
            updateset = updateset + str(result[0]) + "\n"

        context = {'pageName': pageName, 'setid': setid, 'results': results, 'postCase': postCase,'updateset': updateset}

        if (request.method == 'POST'):
            # TO CHANGE THE USER WHEN THE USER ROLE IS READY
            form = UpdateSet(request.POST)
            if (form.is_valid()):
                textarea = form.cleaned_data['updateset']
                print(textarea)
                result = qry.getSet(setid)

                if (result == 1):
                    return HttpResponseRedirect('/success/')
                else:
                    return HttpResponseRedirect('/fail/')


        else:
            form = UpdateSet()

    context = {'pageName': pageName, 'setid': setid, 'results':results, 'postCase':postCase}
    return render(request, "edit_set.html", context)


def deleteSet(request, setid=-1):
    pageName = 'Delete Set'
    userType = "ADMIN_TYPE"
    userId = 1
    postCase = 0

    qry = Queries()

    if (request.method == 'GET' or request.method == 'POST'):

        if (request.get_full_path() != '/set/delete/'):
            path = request.get_full_path()
            setid = path.split('/set/delete/')[1]
            setid = setid.rstrip('/')

    if (setid == -1):
        if (userType == "ADMIN_TYPE"):
            results = qry.getSets()
        else:
            results = qry.getSetsByCreator(userId)
    else:
        results = qry.getSetMeta(setid)
        setname = results[1]

    if (request.method == 'POST'):
        # TO CHANGE THE USER WHEN THE USER ROLE IS READY

        result = qry.deleteSet(setid)
        print(result)

        if (result == 1):
            return HttpResponseRedirect('/success/')
        else:
            return HttpResponseRedirect('/fail/')


    context = {'pageName': pageName, 'setid': setid, 'results': results, 'postCase': postCase}
    return render(request, "delete_set.html", context)


def assignSet(request):
    print("Assign Set method")
    pageName = 'Assign Set'

    qry = Queries()
    helper = HelperMethods()
    annotators_divs = []

    results = qry.getSets()
    annotators = helper.annotators_lookup()
    annotatorsSets = []

    for result in results:
        annotatorsSets = qry.getAnnotatorsSets(result[0])

        for a in annotatorsSets:
            print(str(a[1]) + " SI "+ str(result[0]))
            if(a[1] == results[0]):
                print('TRUE')
                annotators_divs.append(helper.annotatorssets_divs(annotators,result[0]))
                print(annotators_divs)
                print('TRUE')

    context = {'pageName': pageName, "results":results, "annotators":annotators, "annotatorsSets_divs":annotators_divs}
    return render(request, "assign_set.html", context)


def successPage(request):
    pageName = "Success"
    context = {'pageName': pageName}

    return render(request, "success.html", context)

def failPage(request):
    pageName = "FAIL"
    context = {'pageName': pageName}


    return render(request, "fail.html", context)