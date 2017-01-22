class Sentence():
    """
    * id of containing post
    *
    * @var int
    """
    __postId = 0

    """
    * id of sentence
    *
    * @var int
    """
    __sentenceID = 0

    """
    * display ready text of sentence
    *
    * @var string
    """
    __sentence = ""

    """
    * number of paragraph which sentence belongs to (count starts with 1)
    *
    * @var int
    """
    __paragraphInPost = 0

    """
    * number of sentence within paragraph (count starts with 1)
    *
    * @var int
    """
    __sentenceInParagraph = 0


    def __init__(self, postId, sentenceId, sentence, paragraphInPost, sentenceInParagraph):
        self.__postId = postId
        self.__sentenceID = sentenceId
        self.__sentence = sentence
        self.__paragraphInPost = paragraphInPost
        self.__sentenceInParagraph = sentenceInParagraph

    def getPostId(self):
        return self.__postId

    def getSentenceId(self):
        return self.__sentenceID

    def getSentence(self):
        return self.__sentence

    def getParagraphInPost(self):
        return self.__paragraphInPost

    def getSentenceInParagraph(self):
        return self.__sentenceInParagraph