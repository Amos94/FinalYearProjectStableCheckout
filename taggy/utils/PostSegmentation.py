import taggy.modules.post.Post
from taggy.modules.Queries import Queries
import nltk
from django.db import connection
class PostSegmentation:


    qryObject = None
    postId = 0
    sentences = []

    def __init__(self, qryObject,postId):
        """

        :type qryObject: Queries
        """
        self.qryObject = qryObject
        self.postId = postId

    #returns an array of sentences
    def postSegmentation(self, postString):
        text = nltk.corpus.gutenberg.raw(postString)
        self.sentences = nltk.sent_tokenize(text)
        return self.sentences

    #insert sentences into DB
    #TO BE ADDED PARAGRAPH IN POST
    def insertSentence(self, postId):
        for i in self.sentences:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO taggy_sentences VALUES("+postId + ',' + self.sentences[i] + ',' + "[TO BE ADDED PARAGRAPH IN POST]" + ',' + i+")")