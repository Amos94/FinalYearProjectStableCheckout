import Taggy.modules.Queries as Queries


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