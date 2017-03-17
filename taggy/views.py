from django.http import HttpResponseRedirect
from django.shortcuts import render

from forms import CreateSet, UpdateSet
from taggy.modules.Annotator import Annotator
from taggy.modules.HelperMethods import HelperMethods
from taggy.modules.Kappa.ChosenKappa import ChosenKappa
from taggy.modules.Kappa.PostKappaDetails import PostKappaDetails
from taggy.modules.Queries import Queries
from taggy.modules.post.AdjudicatedPost import AdjudicatedPost
from taggy.modules.post.AnnotatedPost import AnnotatedPost
from taggy.modules.post.Post import Post
from taggy.modules.post.Set import Set


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
        for result in results:
            print('NAME SETMETA: ' + results[1])
        setname = results[1]
        qry.updateSet(setid, request.POST.get('updateset'))
        results = qry.getSet(setid)

        postCase = 1
    else:
        results = qry.getSetMeta(setid)
        for result in results:
            print('NAME SETMETA: ' + results[1])
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
            annsts.insert(qryObject.getPostAnnotatorsAndStates(result[0]))

    context = {'pageName': pageName, 'results':results, 'annsts':annsts, "setid":setId, "i":i, 'adjudicationFlag':adjudicationFlag}
    return render(request, "adjudicate_set.html", context)



def tagPost(request, postId=None, setId=None, adjudicationFlag=''):

    pageName = 'Tag Post'
    pageTitle = ''
    userType = 'admin_test'
    userId = 7
    a_set = None
    a_post = None
    qryObject = Queries()
    helper = HelperMethods()


    if (request.GET['setId'] != None):
        setId = request.GET['setId']
    else:
        setId = str(-1)

    set = Set(int(setId))

    if (request.GET['postId'] != None):
        postId = request.GET['postId']
    else:
        postId = str(-1)

    if (request.GET['adjudicationFlag'] == 'true'):
        adjudicationFlag = 'true'
    else:
        adjudicationFlag = 'false'

    if(setId == '-1'):
        a_set = set.get_set(int(setId), userId)
        if(a_set != None):
            if(postId != '-1'):
                postId = a_set.firstPostID()
                print('POST ID: '+ str(postId))
        else:
            a_set = None


    if(userId != None):
        annotator = Annotator(qryObject, userId)
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


    dnt = helper.display_nav_tagpost(a_set, a_post, adjudicationFlag)

    postTableRnd = a_post.render_as_table()

    a = a_post.render_finalize_button()
    b = a_post.render_posts_annotation()
    c = a_post.render_available_tags()

    context = {'pageName': pageName, "setid":setId, "postid":postId, 'pageTitle':pageTitle, 'display_nav_tagpost':dnt, 'postTableRnd':postTableRnd, 'a':a, 'b':b, 'c':c}
    return render(request, "tag_post.html", context)


def reviewSet(request, setId=None):
    pageName = 'Review set'
    userType = 'admin_test'
    userId = 7
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


def reviewParse(request, setId=None, postId=None):
    pageName = 'Review set'
    userType = 'admin'
    userId = 7
    user = 'amos'
    a_set = None
    a_post = None
    set = None
    prevPostId = None
    qryObject = Queries()
    results = []
    parseTools = ['nltk-v0.9.9', 'opennlp-v1.4.3', 'manually' ]


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
                if(request.Post['review'] == 'accept'):
                    status = qryObject.updateParseTool(postId, '', 'PARSED')
                    parseHtml += "<font color=#009900>" + request.Post['review'] + "</font>"
                else:
                    status = qryObject.updateParseTool(postId, request.POST['review'], 'REPARSE')
                    parseHtml += "<font color=#990000>reparse using: " + request.Post['review'] + "</font>"
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
                parseHtml += "<td valign=top align=left>"+str(result[2])+"</td>"#sentence
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
                parseHtml += "<td align=left bgcolor=#aaffaa>"+result['postState']+"</td>"
            else:
                parseHtml += "<td align=left><font color=#cc0000>"+result[0]+"</font></td>"

            parseHtml += "</tr>"
            parseHtml += "<tr class='info'>"
            parseHtml += "<td align=right><i>last reviewed:</i></td>"
            parseHtml += "<td align=left>"
            #result[1] = 'reviewed'
            if ( result[1] == '' ):
                parseHtml += "not reviewed yet</td>"
            else:
                parseHtml += result[1]+"</td>"

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
                parseHtml += "<form action=\"reviewparse.php?"+"\" method=\"post\">"
                parseHtml += "<input type=\"hidden\" name=\"userid\" value=\""+ userId+"\"/>"
                parseHtml += "<input type=\"hidden\" name=\"username\" value=\""+user+"\"/>"
                parseHtml += "<input type=\"hidden\" name=\"usertype\" value=\""+userType+"\"/>"
                parseHtml += "<input type=\"hidden\" name=\"setid\" value=\""+setId+"\"/>"
                parseHtml += "<input type=\"hidden\" name=\"postid\" value=\""+postId+"\"/>"
                parseHtml += "<font color=#0000ff><b>Is the post parsed okay?</b></font>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
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

def postKappaDetails(request):
    pageName = "Post Kappa Details"
    q = Queries()
    s = Set()
    a_set = None
    annotator = None
    a_post = None
    a = []
    b = []
    obj1 = []
    obj2 = []
    pkd = PostKappaDetails()
    errorMsg = ''
    k = ChosenKappa()

    try:
        if(request.GET['s']):
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

    query = "SELECT P.annotatorID, username FROM taggy_posts_annotators P INNER JOIN annotators A ON P.annotatorID = A.annotatorID WHERE postID = "+request.GET['p']+" AND usertype = 'annotator';"
    a = q.getData(query)
    if(len(a) == 2):
        obj1 = a[0]
        annotator1 = obj1[0]
        name1 = obj1[1]

        obj2 = a[1]
        annotator2 = obj2[0]
        name2 = obj2[1]

    query = "SELECT COUNT(DISTINCT S1.sentenceID) FROM taggy_sentences_tags S1 INNER JOIN (SELECT sentenceID FROM taggy_sentences_tags WHERE annotatorID = "+str(annotator2)+" AND postID = "+request.GET['p']+") S2 ON S1.sentenceID = S2.sentenceID WHERE S1.annotatorID = "+str(annotator1)+" AND postID = "+request.GET['p']+";"
    b = q.getData(query)
    totalSentences = b[0]

    query = "SELECT DISTINCT tagName FROM tags"
    tags = q.getData(query)
    sum = 0
    sum2 = 0
    count = 0
    table = "<br />"
    for tag in tags:
        tagIDs = tag[0]
        results = k.countsByPost(annotator1, annotator2, tagIDs, request.GET['p'])
        neither = k.totalSentences - (results[0] + results[1] + results[2])
        ck = k.cohensKappa(results[0], results[1], results[2], neither)
        if(results[0] > 0 or results[1] > 0 or results[2] > 0):
            sum2 += ck
            count += 1
        sum += ck
        table += "<b>Cohen's Kappa for "+tag[0]
        table += " : "+ck+"</b><br /><br /><table border='1'><tr><td colspan='2' rowspan='2'></td><th colspan='2'>"+name1
        table += "</th></tr><tr><th width='75'>Tag "+tag[0]
        table += "</th><th width='75'>&not Tag "+tag[0]
        table += "</th></tr><tr><th rowspan='2'>"+name2
        table += "</th><th align='right'>Tag "+tag[0]
        table += "</th><td align='right'>"+results[2]
        table += "</td><td align='right'>"+results[1]
        table += "</td></tr><tr><th align='right'>&not Tag "+tag[0]
        table += "</th><td align='right'>"+results[0]
        table += "</td><td align='right'>"+neither
        table += "</td></tr></table><br /><br />"
    average = sum / 11
    average2 = sum2 / count

    nav_tagpost = pkd.display_nav_tagpost(a_set, a_post, request.GET['adjudicateFlag'])

    context = {'pageName':pageName, 'pageTitle':page_title, 'average':average, 'average2':average2, 'table':table, 'nav_tagpost':nav_tagpost}
    return render(request, 'postKappaDetails.html', context)

def successPage(request):
    pageName = "Success"
    context = {'pageName': pageName}

    return render(request, "success.html", context)

def failPage(request):
    pageName = "FAIL"
    context = {'pageName': pageName}


    return render(request, "fail.html", context)