import taggy.modules.Queries as Queries


class Post():

    postId = 0
    postError = 0
    forumId = 0
    topicId = 0
    sentences = []

    def __init__(self, postId = -1):

        qryObject = Queries()

        if(postId < 0):
            results = qryObject.getPostAtRandom()

        else:
            results = qryObject.getPost(postId)

        if(results.count != 1):
            self.postId = postId
            self.postError = 'PostID ' + postId + ' does not exist or is not ready to be annotated.'

        else:
            rows = results.fetchall()

            for row in rows:
                self.postId = row['postID']
                self.forumId = row['forumID']
                self.topicId = row['topicID']
                self.postState = row['postState']

            results = qryObject.getSentences(self.postId)
            rows = results.fetchall()

            for row in rows:
                self.addSentence(qryObject, row)

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

    def addSentence(self, qryObkect, args):
        self.sentences.append(args)

    """
    * render_headline()
    *
    * renders HTML for a verbose description of the post
    *
    * @return void
    """
    def renderHeadline(self):
        print("<i>post "+self.getPostId()+" in topic "+self.getTopicId()+" in forum "+self.getForumId()+":</i><br />")

    def render_metadata(self):
        print("<table>")
        print("<tr><th>post id</th><th>topic id</th><th>forum id</th><th>creator</th><th>creationDate</th></tr>")
        print("<tr>")
        print("<td>"+self.getPostId()+"</td>")
        print("<td>"+self.getTopicId()+"</td>")
        print("<td>"+self.getForumId()+"</td>")
        print("</tr>")
        print("</table>")

    def render_table_header(self):
        print("<tr><th width='5%'></th><th width='95%'>sentence</th></tr>")

    """
    * render_as_table()
    *
    * renders an HTML Table for all of the sentences and tags for this post
    *
    * @return void
    """
    def render_as_table(self):
        print("<p>")
        print("<div id='post'>\n")
        print("<table id='p"+self.getPostId()+"' class='postTbl' width='100%' cellspacing=5>")

        self.render_table_header()

        for s in self.getSentences():
            print(s.render_as_row()+"\n")

        print("</table>")
        print("</div> <!-- div#post -->\n")