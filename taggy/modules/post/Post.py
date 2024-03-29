from taggy.modules.Queries import Queries
from taggy.modules.sentence.Sentence import Sentence


class Post():

    postId = 0
    postError = ''
    forumId = 0
    topicId = 0
    sentences = []
    postState = ''

    def __init__(self, postId = -1):

        qryObject = Queries()

        if(postId < 0):
            results = qryObject.getPostAtRandom()

        else:
            results = qryObject.getPost(postId)

        if(results == None):
            self.postId = postId
            self.postError = 'PostID ' + str(postId) + ' does not exist or is not ready to be annotated.'

        else:


            for row in results:
                self.postId = row[0]#['postID']
                self.forumId = row[1]#['forumID']
                self.topicId = row[2]#['topicID']
                self.postState = row[5]#['postState']

            results = qryObject.getSentences(self.postId)


            for row in results:
                self.addSentence(row[2])

            self.postError = None




    def getPostId(self):
        return self.postId

    def getPostError(self):
        return self.postError

    def getForumId(self):
        return self.forumId

    def getTopicId(self):
        return self.topicId

    def getSentences(self):
        return self.sentences

    def addSentence(self, args):
        self.sentences.append(args)

    def getPostState(self):
        return self.postState

    """
    * render_headline()
    *
    * renders HTML for a verbose description of the post
    *
    * @return void
    """
    def renderHeadline(self):
        toReturn = ''
        toReturn += "<i>post "+self.getPostId()+" in topic "+self.getTopicId()+" in forum "+self.getForumId()+":</i><br />"
        return toReturn

    def render_metadata(self):
        toReturn = ''
        toReturn +="<table class='table table-striped table-hover table-condensed'>"
        toReturn +="<tr><th>Post id</th><th>Topic id</th><th>Forum id</th><th>creator</th><th>CreationDate</th></tr>"
        toReturn +="<tr>"
        toReturn +="<td>"+self.getPostId()+"</td>"
        toReturn +="<td>"+self.getTopicId()+"</td>"
        toReturn +="<td>"+self.getForumId()+"</td>"
        toReturn +="</tr>"
        toReturn +="</table>"
        return toReturn

    def render_table_header(self):
        toReturn = ''
        toReturn +="<tr><th>#</th><th>Sentence</th><th>Tag - Provide/ Request</th></tr>"
        return toReturn

    """
    * render_as_table()
    *
    * renders an HTML Table for all of the sentences and tags for this post
    *
    * @return void
    """
    def render_as_table(self, adjudicationFlag, annotatorId):
        toReturn = ''
        toReturn +="<p>"
        toReturn +="<div id='post'>"
        toReturn +="<table id='p"+str(self.getPostId())+"' class='postTbl table table-striped table-hover table-condensed' width='100%'>"

        toReturn += self.render_table_header()

        qryObject = Queries()
        results = qryObject.getSentences(self.postId)
        for s in results:
            a = Sentence(s[0], s[1], s[2], s[3], s[4])
            toReturn += a.render_as_row(self.getPostId(),s[1],annotatorId, adjudicationFlag)

        toReturn +="</table>"
        toReturn +="</div> <!-- div#post -->"
        return toReturn