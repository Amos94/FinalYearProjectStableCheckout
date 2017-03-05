from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import resolve
from django.utils.six.moves.urllib.parse import urlparse
from forms import CreateSet, UpdateSet
from taggy.modules.Annotator import Annotator
from taggy.modules.Queries import Queries
from taggy.modules.post.AdjudicatedPost import AdjudicatedPost
from taggy.modules.post.AnnotatedPost import AnnotatedPost
from taggy.modules.post.Post import Post
from taggy.modules.users import User as User
from taggy.modules.HelperMethods import HelperMethods
from taggy.modules.post import Set as Set

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
            annotators_divs.append({'result':result[0], 'div':helper.annotatorssets_divs(annotators,result[0])})

    context = {'pageName': pageName, "results":results, "annotators":annotators, "annotatorsSets_divs":annotators_divs}
    return render(request, "assign_set.html", context)



def browseSet(request, setId=None, postId=None):
    pageName = 'Browse'
    userType = 'admin'
    userId = 0
    dbname = 'perseus'
    qryObject = Queries()
    Results = []

    print(int(request.GET['s']))
    print(int(request.GET['p']))

    if(int(request.GET['s']) != None):
        setId = int(request.GET['s'])
    else:
        setId = -1


    if (int(request.GET['p']) != None):
        setId = int(request.GET['p'])
    else:
        setId = -1

    if(setId == -1):
        if(userType == 'admin'):
            results = qryObject.getSets()
        else:
            results = qryObject.getSetsByCreator(userId)
    elif(postId == -1):
        results = qryObject.getPostsInSet(setId)
    else:
        results = qryObject.getSentences(postId)

    context = {'pageName': pageName, "results": results}
    return render(request, "browse_set.html", context)




def tagSet(request, setId=None):

    pageName = 'Tag Set'
    userType = 'admin'
    userId = 6
    i=0
    qryObject = Queries()
    results = []
    annsts = []


    if(request.GET['s'] != None):
        setId = request.GET['s']
    else:
        setId = str(-1)

    if(setId == str(-1)):
        if(userType == 'admin'):
            results = qryObject.getSets()
        else:
            results = qryObject.getSetsByAnnotatorId(userId)
    else:
        results = qryObject.getPostsInSet(setId)
        for result in results:
            annsts.append(qryObject.getPostAnnotatorsAndStates(result[0]))


    context = {'pageName': pageName, 'results':results, 'annsts':annsts, "setid":setId, "i":i}
    return render(request, "tag_set.html", context)


def adjudicateSet(request, setId=None):

    pageName = 'Adjudicate Set'
    userType = 'admin'
    userId = 0
    i=0
    qryObject = Queries()
    results = []
    annsts = []

    if (request.GET['s'] != None):
        setId = request.GET['s']
    else:
        setId = str(-1)

    if(setId == -1):
        if(userType == 'admin'):
            results = qryObject.getSets()
        else:
            results = qryObject.getSetsByAnnotatorId(userId)
    else:
        results = qryObject.getPostsInSet(setId)
        for result in results:
            annsts.insert(qryObject.getPostAnnotatorsAndStates(result[0]))

    context = {'pageName': pageName, 'results':results, 'annsts':annsts, "setid":setId, "i":i}
    return render(request, "adjudicate_set.html", context)



def tagPost(request, postId=None, setId=None, adjudicationFlag=''):

    pageName = 'Tag Post'
    pageTitle = ''
    userType = 'admin'
    userId = 0
    set = Set()
    qryObject = Queries()

    if (request.GET['setId'] != None):
        setId = request.GET['setId']
    else:
        setId = str(-1)

    if (request.GET['postId'] != None):
        postId = request.GET['postId']
    else:
        postId = str(-1)

    if (request.GET['adjudicationFlag'] == 'true'):
        adjudicationFlag = 'true'
    else:
        postId = 'false'

    if(setId == '-1'):
        a_set = set.get_set(setId, userId)
        if(a_set != None):
            if(postId != '-1'):
                postId = a_set.firstPostId()
        else:
            a_set = None


    if(userId != None):
        annotator = Annotator(qryObject, userId)
        if(annotator.canAdjudicate() and adjudicationFlag == 'true'):
            a_post = AdjudicatedPost(qryObject, postId, annotator)
        else:
            a_post = AnnotatedPost(qryObject, postId, annotator)
    else:
        a_post = Post(qryObject, postId)

    if(adjudicationFlag == 'true'):
        pageTitle = 'ADJUDICATE POST: '+postId+ ' '
    else:
        pageTitle = 'TAG POST: '+postId+' '

    #TO BE ADDED
    display_nav_tagpost(a_set, a_post, adjudicationFlag)




    context = {'pageName': pageName, "setid":setId, "postid":postId, 'pageTitle':pageTitle}
    return render(request, "tag_post.html", context)

def successPage(request):
    pageName = "Success"
    context = {'pageName': pageName}

    return render(request, "success.html", context)

def failPage(request):
    pageName = "FAIL"
    context = {'pageName': pageName}


    return render(request, "fail.html", context)