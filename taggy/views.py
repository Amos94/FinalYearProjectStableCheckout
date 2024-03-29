from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.backends import django
from django.middleware import csrf
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from taggy.models import Document
from forms import CreateSet, UpdateSet, ChooseTag, DocumentForm, CreateDomain, EditDomain, CreateTag
from taggy.modules.Annotator import Annotator
from taggy.modules.HelperMethods import HelperMethods
from taggy.modules.Kappa.CohensKappa import CohensKappa
from taggy.modules.Kappa.PostKappaDetails import PostKappaDetails
from taggy.modules.Queries import Queries
from taggy.modules.actions.AnnotationAction import AnnotationAction
from taggy.modules.actions.SetAction import SetAction
from taggy.modules.actions.TagAction import TagAction
from taggy.modules.post.AdjudicatedPost import AdjudicatedPost
from taggy.modules.post.AnnotatedPost import AnnotatedPost
from taggy.modules.post.Post import Post
from taggy.modules.post.Set import Set



# Create your views here.
def index(request):
    pageName = "index"
    username = ''
    userId = ''
    adminRights = False

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user
        username = user.username
        userId = user.id
        adminRights = user.is_staff


    context = {"pageName":pageName , "user": user, "adminRights":adminRights}

    return render(request,"index.html",context)

def about(request):
    pageName = "About"

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    context = {"pageName":pageName}

    return render(request, "about.html", context)


def annotation(request):
    pageName = "Annotation"
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username
    context = {"pageName":pageName}

    return render(request, "annotation.html", context)


def adjudication(request):
    pageName = "Adjudication"
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username
    context = {"pageName":pageName}

    return render(request, "adjudication.html", context)

def setCreate(request):
    pageName = "Create Set"

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    sessionId = 'null'
    userid = 2
    qry = Queries()
    context = {"pageName": pageName, "sessionId": sessionId}
    if(request.method == 'POST'):
        #TO CHANGE THE USER WHEN THE USER ROLE IS READY
        form = CreateSet(request.POST)
        if(form.is_valid()):
            setname = form.cleaned_data['setname']
            setdescr = form.cleaned_data['setdescr']
            result = qry.insertSet(setname, setdescr, userid,1)

            if(result == 1):
                # #JUST ADDED NOW
                # setId = 0 #must initialize with the id of the newest set created.
                # results = []
                # qryObject = Queries()
                # #NOW ASSIGN POSTS TO SET.(50 new posts/ set, maybe?)
                # results = qryObject.getPosts()
                # for result in results:
                #     if(result[3] != 'INITIAL'):
                #         #TO CREATE QUERY TO ADD POST IN SET
                #         qryObject.addPostInSet(setId)
                #         qryObject.updatePostState(result[0], 'SELECTED')

                return HttpResponseRedirect('/success/')
            else:
                return HttpResponseRedirect('/fail/')


    else:
        form = CreateSet()


    return render(request, "create_set.html", {'form':form})

def editSet(request, setid=-1):
    pageName = 'Edit Set'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    userType = "ADMIN_TYPE"
    userId = 6
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
        for result in results:
            print('NAME SETMETA: ' + results[1])
        setname = results[1]
        qry.updateSet(setid, request.POST.get('updateset'))
        results = qry.getSet(setid)

        postCase = 1
    else:

        if (request.method == 'POST'):
            # TO CHANGE THE USER WHEN THE USER ROLE IS READY
            form = UpdateSet(request.POST)
            if (form.is_valid()):
                textarea = form.cleaned_data['updateset']
                result = qry.getSet(setid)

                return HttpResponseRedirect('/set/edit/'+str(setid))
        else:
            form = UpdateSet()

        results = qry.getSetMeta(setid)

        setname = results[1]
        results = qry.getSet(setid)
        updateset = ""
        for result in results:
            updateset = updateset + str(result[0]) + "\n"

        context = {'pageName': pageName, 'setid': setid, 'results': results, 'postCase': postCase,'updateset': updateset, 'form':form}



    context = {'pageName': pageName, 'setid': setid, 'results':results, 'postCase':postCase}
    return render(request, "edit_set.html", context)

def editSetAdd(request, setid = -1):
    pageName = 'Edit Set'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    userType = "admin"
    userId = 6
    error = False
    errorMsg = ''
    topicIds = []
    forums = []
    qryObject = Queries()
    try:
        if(request.GET['s']):
            setid = int(request.GET['s'])
        else:
            setid = -1
    except:
        pass

    if(setid!=-1):
        forums = qryObject.getForums()
        for forum in forums:
            topicIds = qryObject.getTopic(forum[0])
    else:
        error = True
        errorMsg = 'Set id was not valid'



    context = {'pageName':pageName, 'topicIds':topicIds, 'setid':setid, 'error':error, 'errorMsg':errorMsg}
    return render(request, 'edit_set_add.html', context)

def editSetTopic(request, setid = -1, topicid = -1, forumid = -1):
    pageName = 'Edit Set'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    error = False
    userType = "admin"
    userId = 6
    errorMsg = ''
    userType = 'admin'
    results = []
    topics = []
    qryObject = Queries()

    try:
        if(request.GET['s']):
            setid = int(request.GET['s'])
        else:
            setid = -1
    except:
        pass

    try:
        if(request.GET['t']):
            topicid= int(request.GET['t'])
        else:
            topicid = -1
    except:
        pass

    try:
        if(request.GET['f']):
            forumid= int(request.GET['f'])
        else:
            forumid = -1
    except:
        pass

    if(setid != -1 and topicid != -1 and userType == 'admin'):
        #add topic to set - ADD JUST POSTS THAT HAS THE postState = INITIAL
        posts = qryObject.getPosts(forumid, topicid, 'INITIAL')
        #iterate and add each post to the set
        for post in posts:

            result = qryObject.addPostInSet(setid, post[0])
            # print(result)
            if(result != 1):
                error = True
                errorMsg = 'Could not update the database'
            # print (post[0])
            # change the state of the post from INITIAL to SELECTED
            result = qryObject.updatePostState(post[0],'PARSED')
            # print('TO UPDATE updatePostState')
            # print(result)
            if (result):
                error = True
                errorMsg = 'Could not update the database'



    else:
        if(userType != 'admin'):
            error = True
            errorMsg = 'You have no access to this action, due to you are not an admin.'
        elif(setid == -1):
            error = True
            errorMsg = 'The set id is not valid.'
        else:
            error = True
            errorMsg = 'The topic id is not valid.'

    context = {'pageName':pageName, 'setid':setid, 'error':error, 'errorMsg':errorMsg}
    return render(request, 'edit_set_add_topic.html', context)

def deleteSet(request, setid=-1):
    pageName = 'Delete Set'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    userType = "ADMIN_TYPE"
    userId = 6
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
        #print(result)

        if (result == 1):
            return HttpResponseRedirect('/success/')
        else:
            return HttpResponseRedirect('/fail/')


    context = {'pageName': pageName, 'setid': setid, 'results': results, 'postCase': postCase}
    return render(request, "delete_set.html", context)


def assignSet(request):
    #print("Assign Set method")
    pageName = 'Assign Set'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    qry = Queries()
    helper = HelperMethods()
    annotators_divs = []

    results = qry.getSets()
    annotators = helper.annotators_lookup()
    annotatorsSets = []

    for result in results:
        annotatorsSets = qry.getAnnotatorsSets(result[0])
        #print annotatorsSets

        for a in annotatorsSets:
            annotators_divs.append({'result':result[0], 'div':qry.getAnnotatorName(a[0])})

    context = {'pageName': pageName, "results":results, "annotators":annotators, "annotatorsSets_divs":annotators_divs}
    return render(request, "assign_set.html", context)

def assignSetAdd(request, setid=-1):
    pageName = 'Assign Set'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    userType = "admin"
    userId = 6
    error = False
    errorMsg = ''
    h = HelperMethods()
    annotators = []

    try:
        if(request.GET['s']):
            setid = int(request.GET['s'])
        else:
            setid = -1
    except:
        pass

    if(setid!=-1):
        annotators = h.annotators_lookup()
    else:
        error = True
        errorMsg = 'Set id was not valid'

    context={'pageName':pageName, 'annotators':annotators, 'setid':setid}
    return render(request,'assign_set_add.html', context)

def assignSetAnnotator(request, setid=-1, annotatorid=-1):
    pageName = 'Assign Set'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    error = False
    userType = "admin"
    userId = 6
    errorMsg = ''
    results = []
    topics = []
    qryObject = Queries()

    try:
        if (request.GET['s']):
            setid = int(request.GET['s'])
        else:
            setid = -1
    except:
        pass

    try:
        if (request.GET['a']):
            annotatorid = int(request.GET['a'])
        else:
            annotatorid = -1
    except:
        pass

    if (setid != -1 and annotatorid != -1 and userType == 'admin'):
        # assign annotator to set
        result = qryObject.insertAnnotatorsSets(annotatorid, setid)
        if(result != 1):
            error = True
            errorMsg = 'The annotator assignment task was unsuccessfull.'

    else:
        if (userType != 'admin'):
            error = True
            errorMsg = 'You have no access to this action, due to you are not an admin.'
        elif (setid == -1):
            error = True
            errorMsg = 'The set id is not valid.'
        else:
            error = True
            errorMsg = 'The annotator id is not valid.'

    context = {'pageName': pageName, 'setid': setid, 'error': error, 'errorMsg': errorMsg}
    return render(request, 'assign_set_annotator.html', context)

def browseSet(request, setId=None, postId=None):
    pageName = 'Browse'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    userType = 'admin'
    userId = 0
    dbname = 'perseus'
    qryObject = Queries()
    results = []

    try:
        if(int(request.GET['s']) != None):
            setId = int(request.GET['s'])
        else:
            setId = -1
    except:
        pass

    try:
        if (int(request.GET['p']) != None):
            postId = int(request.GET['p'])
        else:
            postId = -1
    except:
        pass

    if(str(setId) == 'None'):
        setId = -1

    if(not postId):
        postId = -1

    h = HelperMethods()
    rAnnotationProgress = []

    if(setId == -1):
        if(userType == 'admin'):
            results = qryObject.getSets()
            for result in results:
                rAnnotationProgress.append(h.renderAnnotationProgress(result[0]))
        else:
            results = qryObject.getSetsByCreator(userId)
            for result in results:
                rAnnotationProgress.append(h.renderAnnotationProgress(result[0]))
    elif(postId == -1):
        results = qryObject.getPostsInSet(setId)
    else:
        results = qryObject.getSentences(postId)

    rAnnotationProgress.reverse()


    context = {'pageName': pageName, 'dbName':dbname, "results": results, 'setId':setId, 'postId': postId, 'rAnnotationProgress':rAnnotationProgress}
    return render(request, "browse_set.html", context)




def tagSet(request, setId=None):

    pageName = 'Tag Set'


    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    userType = 'admin'
    userId = 6
    i=0
    qryObject = Queries()
    results = []
    annsts = []

    adjudicationFlag = 'false'
    if(userType=='admin' or userType=='adjud'):
        adjudicationFlag = 'true'

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


    context = {'pageName': pageName, 'results':results, 'annsts':annsts, "setid":setId, "i":i,'adjudicationFlag':adjudicationFlag}
    return render(request, "tag_set.html", context)


def adjudicateSet(request, setId=None):

    pageName = 'Adjudicate Set'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    userType = 'admin'
    userId = 0
    i=0
    qryObject = Queries()
    results = []
    annsts = []
    adjudicationFlag = 'false'

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
            #print(result[0])
            annsts.insert(qryObject.getPostAnnotatorsAndStates(result[0]))

    context = {'pageName': pageName, 'results':results, 'annsts':annsts, "setid":setId, "i":i, 'adjudicationFlag':adjudicationFlag}
    return render(request, "adjudicate_set.html", context)


@csrf_exempt
def tagPost(request, postId=None, setId=None, adjudicationFlag=''):

    pageName = 'Tag Post'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    pageTitle = ''
    userType = 'annotator'
    userId = 7
    a_set = None
    a_post = None
    qryObject = Queries()
    helper = HelperMethods()

    try:
        if (request.GET['setId'] != None):
            setId = request.GET['setId']
        else:
            setId = str(-1)
    except:
        pass

    if(setId != None):
        set = Set(int(setId))
    else:
        setid = '-1'

    try:
        if (request.GET['postId'] != None):
            postId = request.GET['postId']
        else:
            postId = str(-1)
    except:
        pass
    if(postId == None):
        postId = '-1'

    try:
        if (request.GET['adjudicationFlag'] == 'true'):
            adjudicationFlag = 'true'
        else:
            adjudicationFlag = 'false'
    except:
        pass
    if(adjudicationFlag == None):
        adjudicationFlag == 'false'

    if(setId == '-1'):
        a_set = set.get_set(int(setId), userId)
        if(a_set != None):
            if(postId != '-1'):
                postId = a_set.firstPostID()
                #print('POST ID: '+ str(postId))
        else:
            a_set = None


    if(userId != None):
        annotator = Annotator(userId)
        if(annotator.canAdjudicate() and adjudicationFlag == 'true'):
            a_post = AdjudicatedPost(int(postId), annotator)
        else:
            a_post = AnnotatedPost(int(postId), annotator)
    else:
        a_post = Post(int(postId))


    if(adjudicationFlag == 'true'):
        pageTitle = 'ADJUDICATE POST: '+postId+ ' '
    else:
        pageTitle = 'TAG POST: '+postId+' '

    annotatorsOfSet = []
    assigned = True
    if(annotator.canAdjudicate() == True):
        assigned = True
    try:
        annotators = qryObject.getAnnotatorsSets(setid)
        for a in annotators:
            if(annotator.id == a[0]):
                assigned = True
    except:
        pass


    if request.method == 'POST':
        #print('worked')
        return HttpResponseRedirect('/thanks/')

    dnt = helper.display_nav_tagpost(a_set, a_post, adjudicationFlag)
    postTableHeader = a_post.render_table_header()
    postTableRnd = a_post.render_as_table(adjudicationFlag, annotator.id)

    a = a_post.render_finalize_button()
    b = a_post.render_posts_annotation()
    c = a_post.render_available_tags()

    context = {'pageName': pageName, "assigned":assigned ,"setid":setId, "postid":postId, 'pageTitle':pageTitle, 'display_nav_tagpost':dnt, 'postTableHeader':postTableHeader,'postTableRnd':postTableRnd, 'a':a, 'b':b, 'c':c}
    return render(request, "tag_post.html", context)

@csrf_exempt
def tagUpdateDb(request):
    pageName = 'TAG POST'


    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    variables = []
    array = []
    qryObject = Queries()
    error = False
    errorMsg = ''
    try:
        variables = request.POST.getlist('taskOption')
        #print variables
    except:
        error = True
        errorMsg = 'The request is not valid'
        pass

    # 0 = TAGID, 1 = ANNOTATORID, 2 = POSTID, 3 = SENTENCEID
    for variable in variables:
        array.append(variable.split())


    try:
        #annotate the sentence
        for a in array:
            qryObject.insertSentenceTag(a[3], a[0], a[2], a[1])
        pass
    except:
        error = True
        errorMsg = 'Could not update the database'
        pass

    context = {'error':error, 'errorMsg':errorMsg, 'pageName':pageName}
    return render(request,'tag_post_update.html',context)


def deletePostTags(request, annotatorid=-1, postid=-1, sentenceid=-1):
    pageName = 'EDIT POST TAGS'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    qryObject = Queries()
    sentence = []
    sentenceTags = []
    tags = []
    tags2 = []
    allTags = []
    toRemove = []
    error = False
    errorMsg = ''


    try:
        postid = request.GET['post']
        annotatorid = request.GET['annotator']
        sentenceid = request.GET['sentence']

    except:
        error = True
        errorMsg = 'Invalid link.'
        pass


    try:
        sentence = qryObject.getSentence(sentenceid)
        sentenceTags = qryObject.getSentenceTags(postid, sentenceid, annotatorid)
        allTags = qryObject.getTagAndPOR()
        for s in sentenceTags:
            tags.append(qryObject.getTag(s[2]))
            tags2.append(qryObject.getTag(s[2]))
        tags.reverse()
        tags2.reverse()

        # for i in allTags:
        #     for j in tags:
        #         a = i[0]
        #         b = j[0]
        #
        #         if(a == b[0]):
        #             toRemove.append(a)
        #
        # for remove in toRemove:
        #     print(remove)
        #     allTags.pop(remove)



    except:
        error = True
        errorMsg = 'Could talk to database.'
        pass

    context = {'error':error, 'errorMsg':errorMsg, 'pageName':pageName, 'sentence':sentence, 'sentenceTags':sentenceTags, 'allTags':allTags, 'tags2':tags2, 'tags':tags, 'annotatorid':annotatorid,'postid':postid, 'sentenceid':sentenceid}
    return render(request,'post_update_tag.html',context)



def tagDeleteDb(request, sentenceid=-1, tagid=-1, postid=-1, annotatorid=-1):
    pageName = 'Delete TAGS'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    qryObject = Queries()
    error = False
    errorMsg = ''
    result = []


    try:
        tagid = request.GET['tag']
        postid = request.GET['post']
        annotatorid = request.GET['annotator']
        sentenceid = request.GET['sentence']

    except:
        error = True
        errorMsg = 'Invalid link.'
        pass


    try:
        result = qryObject.deleteSentenceTag(sentenceid,tagid,postid,annotatorid)
    except:
        error = True
        errorMsg = 'Could talk to database.'
        pass

    context = {'error':error, 'errorMsg':errorMsg, 'pageName':pageName}
    return render(request,'delete_post_tag.html',context)

#test



@csrf_exempt
def reviewSet(request, setId=None):
    pageName = 'Review set'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    userType = 'admin_test'
    userId = 1
    qryObject = Queries()
    results = []

    if (request.GET['s'] != None):
        setId = request.GET['s']
    else:
        setId = str(-1)

    if(setId == '-1'):
        results = qryObject.getSets()
    else:
        results = qryObject.getPostsInSet(setId)

    context = {'pageName':pageName, 'setid':setId, 'results':results}
    return render(request, "review_set.html", context)

@csrf_exempt
def reviewParse(request, setId=None, postId=None):
    pageName = 'Review set'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    userType = 'admin'
    userId = 7
    user = 'amos'
    a_set = None
    a_post = None
    set = None
    prevPostId = None
    qryObject = Queries()
    results = []
    parseTools = ['NLTK parser']


    if(userType == 'admin'):
        if (request.GET['s'] != None):
            setId = request.GET['s']
        elif(request.POST['s'] != None):
            setId = request.POST['s']
        else:
            setId = '-1'

        set = Set(int(setId))

        if(request.GET['p'] != None):
            postId = request.GET['p']
        elif(request.POST['p'] != None):
            postId = request.POST['p']
        else:
            postId = '-1'

        a_set = set.get_set(setId, userId)
        prevPostId = a_set.getPrevPostId(int(postId))

        #PARSE REVIEW POST METHOD
        parseHtml = ''

        if(request.method == 'POST'):
            if(request.POST['review']):
                parseHtml += "<br /><i>processing review</i><br /><br />"
                parseHtml +="&nbsp;&nbsp; post " + postId + " in set " + setId + ": &nbsp; [ "
                if(request.POST['review'] == 'accept'):
                    status = qryObject.updateParseTool(postId, '', 'PARSED')
                    parseHtml += "<font color=#009900>" + request.POST['review'] + "</font>"
                else:
                    status = qryObject.updateParseTool(postId, request.POST['review'], 'REPARSE')
                    parseHtml += "<font color=#990000>reparse using: " + request.POST['review'] + "</font>"
                parseHtml += " ]<br /><br />"
                parseHtml += "<i>database has been updated.</i><br />"
        else:
            parseHtml = ''
            parseHtml += "<br/><b>results of most recent parse:</b><br />"
            parseHtml += "<i>sentences found in post "+postId+" in set "+setId+":</i><br />"

            results = qryObject.getSentences( postId )

            parseHtml += "<div class='scrollHalfList'>"
            parseHtml += "<table class='table table-striped table-hover table-condensed'>"
            parseHtml += "<tr><th>sentenceID</th><th>paragraphInPost</th><th>sentenceInParagraph</th><th>sentence</th></tr>"
            for result in results:
                parseHtml += "<tr>"
                parseHtml += "<td valign=top align=right>"+str(result[1])+"</td>"#sentenceID
                parseHtml += "<td valign=top align=center>"+str(result[3])+"</td>"#paragraphInPost
                parseHtml += "<td valign=top align=center>"+str(result[4])+"</td>"#sentenceInParagraph
                parseHtml += "<td valign=top align=left>"+result[2]+"</td>"#sentence
                parseHtml += "</tr>"
            parseHtml += "</table>"
            parseHtml += "</div>"

            parseHtml += "<b>information about this post:</b><br />"
            results = qryObject.getPostParseInfo( postId )
            result = results[0]

            parseHtml += "<table class='table text-center'>"
            parseHtml += "<tr class='info'>"
            parseHtml += "<td align=right><i>post state: </i></td>"
            #result[0] = 'postState'
            if (( result[0] == 'INITIAL' ) or ( result[0] == 'SELECTED' ) or ( result[0] == 'REPARSE' )):
                parseHtml += "<td align=left bgcolor=#aaffaa>"+str(result[0])+"</td>"
            else:
                parseHtml += "<td align=left><font color=#cc0000>"+str(result[0])+"</font></td>"

            parseHtml += "</tr>"
            parseHtml += "<tr class='info'>"
            parseHtml += "<td align=right><i>last reviewed:</i></td>"
            parseHtml += "<td align=left>"
            #result[1] = 'reviewed'
            if ( result[1] == '' ):
                parseHtml += "not reviewed yet</td>"
            else:
                parseHtml += str(result[1])+"</td>"

            parseHtml += "</tr>"
            #result[5] = 'parseTool'
            if ( result[5] ):
                parseHtml += "<tr class='info'>"
                parseHtml += "<td align=right><i>parse tool:</i></td>"
                parseHtml += "<td align=left>"+result[5]+"</td>"
                parseHtml += "</tr>"

            parseHtml += "<tr class='info'>"
            parseHtml += "<td align=right><i>parse version:</i></td>"
            #result[] = 'parseVersion'
            parseHtml += "<td align=left>"+ str(result[4])+"</td>"
            parseHtml += "</tr>"
            parseHtml += "<tr class='info'>"
            parseHtml += "<td align=right><i>last parsed:</i></td>"
            # result[] = 'parsed'
            parseHtml += "<td align=left>"+ result[2]+"</td>"
            parseHtml += "</tr>"
            parseHtml += "<tr class='info'>"
            parseHtml += "<td align=right><i>parse history:</td>"
            #result[] = 'parseHistory'
            parseHtml += "<td align=left>"+ result[3]+"</td>"
            parseHtml += "</tr>"
            parseHtml += "</table>"
            parseHtml += "<p>"
            #result[0] = poststate
            if (( result[0] == 'INITIAL' ) or ( result[0] == 'SELECTED' ) or ( result[0] == 'REPARSE' )):
                parseHtml += "<form action=\"/review/parse/?s="+str(setId)+"&p="+str(postId)+"\" method='POST'>"

                parseHtml += "<input type=\"hidden\" name=\"userid\" value=\""+ str(userId)+"\"/>"
                parseHtml += "<input type=\"hidden\" name=\"username\" value=\""+user+"\"/>"
                parseHtml += "<input type=\"hidden\" name=\"usertype\" value=\""+userType+"\"/>"
                parseHtml += "<input type=\"hidden\" name=\"setid\" value=\""+str(setId)+"\"/>"
                parseHtml += "<input type=\"hidden\" name=\"postid\" value=\""+str(postId)+"\"/>"
                parseHtml += "<b>Is the post parsed okay?</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                parseHtml += "<select name=\"review\">"
                parseHtml += "<option value=\"accept\">Yes! Accept the parse </option>"

                for p in parseTools:
                    # result[0] = poststate
                    # result[5] = parsetool
                    if(result[0] == 'REPARSE' and result[5] == p):
                        parseHtml += "<option value=\"" + p + "\" selected=\"selected\">No! Reparse using: "+ p +"</option>"
                    else:
                        parseHtml += "<option value=\"" + p + "\">No! Reparse using: "+ p +"</option>"
                parseHtml += "</select>"
                parseHtml += "<input type=\"submit\" name=\"submit\" />"
                parseHtml += "</form>"

    context = {'pageName': pageName, 'setid':setId, 'postid':postId, 'parseHtml': parseHtml}

    return render(request, 'review_parse.html', context)



@csrf_exempt
def postKappaDetails(request):
    pageName = "Post Kappa Details"

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    q = Queries()

    a_set = None
    annotator = None
    a_post = None
    a = []
    b = []
    obj1 = []
    obj2 = []
    pkd = PostKappaDetails()
    errorMsg = ''
    k = CohensKappa()

    try:
        if(request.GET['s']):
            s = Set(request.GET['s'])
            a_set = s.get_set(request.GET['s'], request.GET['p'])

            if(request.GET['p']):
                postId = a_set.firstPostID()
        else:
            a_set = None

        if(not request.GET['p']):
            raise Exception('No PostID available.', 'No PostID available.')

        if(request.GET['a']):
            annotator = Annotator(request.GET['a'])

            if(annotator.canAdjudicate() and request.GET['adjudicateFlag'] == 'true'):
                a_post = AdjudicatedPost(request.GET['p'],annotator)
            else:
                a_post = AnnotatedPost(request.GET['p'], annotator)
        else:
            a_post = Post(request.GET['p'])
        if(a_post.postError()):
            errorMsg += "'<p style='color:red'><i>" + str(a_post.postError()) + "</i><p>"
    except:
        errorMsg += "ERROR"

    page_title = "Post "+request.GET['p']

    query = "SELECT P.annotatorId, username FROM taggy_posts_annotators P INNER JOIN taggy_annotators A ON P.annotatorId = A.annotatorId WHERE postId = "+request.GET['p']+" AND usertype = 'annotator';"
    a = q.getData(query)

    #if(len(a) != 2):
        #print("The annotators number !=2. Number of annotators: " + str(len(a)))
    obj1 = a[0]
    annotator1 = obj1[0]
    name1 = obj1[1]

    obj2 = a[1]
    annotator2 = obj2[0]
    name2 = obj2[1]

    query = "SELECT COUNT(DISTINCT S1.sentenceId) FROM taggy_sentences_tags S1 INNER JOIN (SELECT sentenceId FROM taggy_sentences_tags WHERE annotatorId = "+str(annotator2)+" AND postId = "+request.GET['p']+") S2 ON S1.sentenceId = S2.sentenceId WHERE S1.annotatorId = "+str(annotator1)+" AND postId = "+request.GET['p']+";"
    b = q.getData(query)
    ts = b[0]
    totalSentences = ts[0]


    query = "SELECT DISTINCT tagName FROM taggy_tags"
    tags = q.getData(query)
    sum = 0
    sum2 = 0
    count = 0
    table = "<br />"
    for tag in tags:
        tagIDs = tag[0]

        results = k.countsByPost(annotator1, annotator2, tags, request.GET['p'])
        neither = totalSentences - (results[0] + results[1] + results[2])
        ck = k.chosenKappa(results[0], results[1], results[2], neither)
        if(results[0] > 0 or results[1] > 0 or results[2] > 0):
            sum2 = sum2 + ck
            count = count + 1
        sum += ck
        table += "<b>Cohen's Kappa for "+tag[0]
        table += " : "+str(ck)+"</b><br /><br /><table border='1'><tr><td colspan='2' rowspan='2'></td><th colspan='2'>"+name1
        table += "</th></tr><tr><th width='75'>Tag "+tag[0]
        table += "</th><th width='75'>&not Tag "+tag[0]
        table += "</th></tr><tr><th rowspan='2'>"+name2
        table += "</th><th align='right'>Tag "+tag[0]
        table += "</th><td align='right'>"+str(results[2])
        table += "</td><td align='right'>"+str(results[1])
        table += "</td></tr><tr><th align='right'>&not Tag "+tag[0]
        table += "</th><td align='right'>"+str(results[0])
        table += "</td><td align='right'>"+str(neither)
        table += "</td></tr></table><br /><br />"
    average = sum / 11
    average2 = 0
    if(count != 0):
        average2 = sum2 / count

    nav_tagpost = pkd.display_nav_tagpost(a_set, a_post, request.GET['adjudicateFlag'])

    context = {'pageName':pageName, 'pageTitle':page_title, 'average':average, 'average2':average2, 'table':table, 'nav_tagpost':nav_tagpost}
    return render(request, 'postKappaDetails.html', context)

@csrf_exempt
def tagAction(request):

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    ta = TagAction()
    annotatorId = 0#annotator who is making the action
    array = []#POST args
    if(request.method == 'POST'):

        array.insert('action',request.POST['action'])
        array.insert('sentenceId', request.POST['sentenceId'])
        array.insert('tagId', request.POST['tagId'])
        array.insert('postId', request.POST['postId'])

        if(request.POST['action'] == 'INSERT'):
            ta.insertSentenceTagToDb(annotatorId, array)
        elif(request.POST['action'] == 'DELETE'):
            ta.detleteSentenceTagFromDb(annotatorId, array)
    context = {}
    return render(request, 'tag_action.html', context)


@csrf_exempt
def annotationAction(request):

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    array = []
    annotatorId = 0  # annotator who is making the action
    aa = AnnotationAction()
    array.insert('postId', request.POST['postId'])
    array.insert('comment', request.POST['comment'])
    array.insert('state', request.POST['state'])


    aa.updateAnnotatorsTable(array, annotatorId)

    return request


@csrf_exempt
def setAction(request):

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    array = []
    annotatorId = 0
    sa = SetAction()

    array.insert('setId', request.POST['setId'])
    array.insert('action', request.POST['action'])

    sa.action(annotatorId, array)

    return request

def list(request):

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'list.html',
        {'documents': documents, 'form': form}
)



def domainCreate(request):
    pageName = "Create domain"

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    sessionId = 'null'
    userid = 2
    qry = Queries()
    context = {"pageName": pageName, "sessionId": sessionId}
    if(request.method == 'POST'):
        #TO CHANGE THE USER WHEN THE USER ROLE IS READY
        form = CreateDomain(request.POST)
        if(form.is_valid()):
            domainName = form.cleaned_data['domainname']

            result = qry.insertDomain(domainName)

            if(result == 1):
                return HttpResponseRedirect('/success/')
            else:
                return HttpResponseRedirect('/fail/')


    else:
        form = CreateDomain()


    return render(request, "create_domain.html", {'form':form})


def domainEdit(request, domainId=-1):
    pageName = "Edit domain"

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    qryObject = Queries()
    results = []
    postCase = 0

    try:
        if(request.method == "GET"):
            domainId = request.GET['id']
        else:
            domainId = -1
    except:
        pass

    if(domainId == -1):
        results = qryObject.getDomainsMeta()

    else:
        results = qryObject.getDomainById(domainId)



    context = {'pageName':pageName, 'results':results, 'postCase':postCase, 'domainId':domainId}
    return render(request, "edit_domain.html", context)



def editDomainName(request, domainId = -1):
    pageName = 'Edit Set'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    userType = "admin"
    userId = 6
    results = []
    qryObject = Queries()

    try:
        if(request.GET['id']):
            domainId = int(request.GET['id'])
        else:
            domainId = -1
    except:
        pass

    if (request.method == 'POST'):
        # TO CHANGE THE USER WHEN THE USER ROLE IS READY
        form = EditDomain(request.POST)
        if (form.is_valid()):
            domainName = form.cleaned_data['domainname']

            result = qryObject.editDomainName(domainId, domainName)

            if (result == 1):
                return HttpResponseRedirect('/success/')
            else:
                return HttpResponseRedirect('/fail/')


    else:
        form = EditDomain()


    context = {'pageName':pageName, 'form': form, 'domainId':domainId}

    return render(request, 'edit_domain_name.html', context)


def assignDomain(request):

    pageName = 'Assign Domain'


    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    qry = Queries()
    helper = HelperMethods()
    annotators_divs = []

    results = qry.getDomainsMeta()
    annotators = helper.annotators_lookup()
    annotatorsSets = []

    for result in results:
        annotatorsSets = qry.getAnnotatorsDomains(result[0])

        for a in annotatorsSets:
            annotators_divs.append({'result':result[0], 'div':qry.getAnnotatorName(a[1])})

    context = {'pageName': pageName, "results":results, "annotators":annotators, "annotatorsSets_divs":annotators_divs}
    return render(request, "assign_domain.html", context)



def assignDomainAdd(request, domainId=-1):
    pageName = 'Assign Set'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    userType = "admin"
    userId = 6
    error = False
    errorMsg = ''
    h = HelperMethods()
    annotators = []

    try:
        if(request.GET['id']):
            domainId = int(request.GET['id'])
        else:
            domainId = -1
    except:
        pass

    if(domainId!=-1):
        annotators = h.annotators_lookup()
    else:
        error = True
        errorMsg = 'Set id was not valid'

    context={'pageName':pageName, 'annotators':annotators, 'domainId':domainId}
    return render(request,'assign_domain_add.html', context)


def assignDomainAnnotator(request, domainId = -1, annotatorid = -1):
    pageName = 'Assign Set'

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    error = False
    userType = "admin"
    userId = 6
    errorMsg = ''
    results = []
    topics = []
    qryObject = Queries()

    try:
        if (request.GET['id']):
            domainId = int(request.GET['id'])
        else:
            domainId = -1
    except:
        pass

    try:
        if (request.GET['a']):
            annotatorid = int(request.GET['a'])
        else:
            annotatorid = -1
    except:
        pass

    if (domainId != -1 and annotatorid != -1 and userType == 'admin'):
        # assign annotator to set
        result = qryObject.assignAnnotatorToDomain(annotatorid, domainId)

        if(result != 1):
            error = True
            errorMsg = 'The annotator assignment task was unsuccessfull.'

    else:
        if (userType != 'admin'):
            error = True
            errorMsg = 'You have no access to this action, due to you are not an admin.'
        elif (domainId == -1):
            error = True
            errorMsg = 'The domain id is not valid.'
        else:
            error = True
            errorMsg = 'The annotator id is not valid.'

    context = {'pageName': pageName, 'domainId': domainId, 'error': error, 'errorMsg': errorMsg}
    return render(request, 'assign_domain_annotator.html', context)



def createTag(request, tagpor='N/A', domainid=-1):
    pageName = "Create TAG"

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    sessionId = 'null'
    userid = 2
    results = []
    tags = []
    domainName = ''
    qry = Queries()

    try:
        if(request.method == 'GET'):
            domainid = request.GET['id']
        else:
            domainid = -1
        #PROVIDE OR REQUEST APPLING JUST TO PERSUS
        if(domainid == 1):
            tagpor = request.GET['por']
        else:
            tagpor = 'N/A'
    except:
        pass

    if(domainid == -1):
        results = qry.getDomainsMeta()
    else:
        results = qry.getDomainById(domainid)
        tags = qry.getTagsForDomain(domainid)
        for result in results:
            domainName = result[1]



    context = {"pageName": pageName, 'results':results, 'tags':tags, 'domainId':domainid, 'tagpor':tagpor, 'domainName':domainName}

    return render(request, "create_tag.html", context)


def createTagAdd(request, tagpor='N/A', tagdomain=-1):
    pageName = "Create TAG"

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    sessionId = 'null'
    userid = 2
    qry = Queries()

    try:
        if(request.method == 'GET'):
            tagdomain = request.GET['id']
        else:
            tagdomain = -1
        #PROVIDE OR REQUEST APPLING JUST TO PERSUS
        if(tagdomain == '1'):
            tagpor = request.GET['por']
        else:
            tagpor = 'N/A'
    except:
        pass


    if (request.method == 'POST'):
        # TO CHANGE THE USER WHEN THE USER ROLE IS READY
        try:
            if (request.method == 'POST'):
                tagdomain = request.GET['id']
            else:
                tagdomain = -1
            # PROVIDE OR REQUEST APPLING JUST TO PERSUS
            if (tagdomain == '1'):
                tagpor = request.GET['por']
            else:
                tagpor = 'N/A'
        except:
            pass
        form = CreateTag(request.POST)
        if (form.is_valid()):
            tagname = form.cleaned_data['tagname']
            tagdescr = form.cleaned_data['tagdescr']
            result = qry.createTag(tagname, tagdescr, tagpor, tagdomain)

            if (result == 1):

                return HttpResponseRedirect('/success/')
            else:
                return HttpResponseRedirect('/fail/')


    else:
        form = CreateTag()

    context = {"pageName": pageName, "form": form, 'domainId':tagdomain, 'por':tagpor}

    return render(request, "create_tag_add.html", context)


def deleteTag(request, tagpor='N/A', domainid=-1):
    pageName = "Delete TAG"

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    sessionId = 'null'
    userid = 2
    results = []
    tags = []
    domainName = ''
    qry = Queries()

    try:
        if(request.method == 'GET'):
            domainid = request.GET['id']
        else:
            domainid = -1
        #PROVIDE OR REQUEST APPLING JUST TO PERSUS
        if(domainid == 1):
            tagpor = request.GET['por']
        else:
            tagpor = 'N/A'
    except:
        pass

    if(domainid == -1):
        results = qry.getDomainsMeta()
    else:
        results = qry.getDomainById(domainid)
        tags = qry.getTagsForDomain(domainid)
        for result in results:
            domainName = result[1]



    context = {"pageName": pageName, 'results':results, 'tags':tags, 'domainId':domainid, 'tagpor':tagpor, 'domainName':domainName}

    return render(request, "delete_tag.html", context)



def deleteTagAction(request, tagId=-1):
    pageName = "Delete TAG"

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    sessionId = 'null'
    userid = 2
    error = False
    errorMsg = ''
    results = []
    qry = Queries()

    try:
        if(request.method == 'GET'):
            tagId = request.GET['id']
        else:
            tagId = -1
    except:
        pass

    if(tagId == -1):
        error = True
        errorMsg = 'INVALID TAG ID'
    else:
        results = qry.deleteTag(tagId)



    context = {"pageName": pageName, 'results':results, 'error':error, 'errorMsg':errorMsg}

    return render(request, "delete_tag_action.html", context)



def importJson(request):
    pageName = "Import JSON"
    user = None
    qryObject = Queries()
    results = []

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user


    results = qryObject.getJSONDocumentsMeta()

    context = {'pageName':pageName, 'user':user, 'results':results}

    return render(request, 'import_json.html', context)



def parseJson(request, id=-1):
    pageName = "Parse JSON"
    user = None
    qryObject = Queries()
    results = []

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user




    context = {'pageName':pageName, 'user':user}

    return render(request, 'parse_json.html', context)



def successPage(request):
    pageName = "Success"

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    context = {'pageName': pageName}

    return render(request, "success.html", context)

def failPage(request):
    pageName = "FAIL"

    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    else:
        #GETUSERID
        user = request.user.username

    context = {'pageName': pageName}


    return render(request, "fail.html", context)