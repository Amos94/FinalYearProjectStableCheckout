import taggy.modules.Queries as Queries


class Post():

    __postId = 0
    __postError = 0
    __forumId = 0
    __topicId = 0
    __sentences = []

    def __init__(self, qryObject, postId = -1):

        qryObject = Queries()

        if(postId < 0):
            results = qryObject.getPostAtRandom()

        else:
            results = qryObject.getPost(postId)

        if(results.count != 1):
            self.__postId = postId
            self.__postError = 'PostID ' + postId + ' does not exist or is not ready to be annotated.'

        else:
            rows = results.fetchall()

            for row in rows:
                self.__postId = row['postID']
                self.__forumId = row['forumID']
                self.__topicId = row['topicID']
                self.__postState = row['postState']

            results = qryObject.getSentences(self.__postId)
            rows = results.fetchall()

            for row in rows:
                self.addSentence(qryObject, row)

            self.__postError = None




    def getPostId(self):
        return self.__postId

    def getPostError(self):
        return self.__postError

    def getForumId(self):
        return self.__forumId

    def getTopicId(self):
        return self.__topicId

    def getSentences(self):
        return self.__sentences

    def addSentence(self, qryObkect, args):
        self.__sentences.append(args)

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