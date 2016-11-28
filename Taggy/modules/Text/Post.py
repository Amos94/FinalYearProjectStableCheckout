class Post():

    __postId = 0
    __postError = 0
    __forumId = 0
    __topicId = 0
    __sentences = []

    def __init__(self, postId, postError, forumId, topicId, sentences):

        self.__postId = postId
        self.__postError = postError
        self.__forumId = forumId
        self.__topicId = topicId
        self.__sentences = sentences

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

    def addSentence(self, sentence):
        self.__sentences.append(sentence)