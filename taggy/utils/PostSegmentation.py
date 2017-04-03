import taggy.modules.post.Post
from taggy.modules.Queries import Queries
import nltk
from django.db import connection
class PostSegmentation:


    qryObject = None
    postId = 0
    sentences = []

    def __init__(self,postId):
        """

        :type qryObject: Queries
        """
        #nltk.download()
        self.qryObject = Queries()
        self.postId = postId
        self.postSegmentation()

    #returns an array of sentences
    def postSegmentation(self):
        self.getPostString()
        text = nltk.corpus.gutenberg.raw('C:\\Users\\Amos Madalin Neculau\\Desktop\\FinalYearProject2\\taggy\\utils\\post.txt')
        self.sentences = nltk.sent_tokenize(text)
        return self.sentences

    def getPostString(self):
        post = self.qryObject.getPostContent(self.postId)
        sentence = ''

        for p in post:
            sentence = p[0]

        with open("C:\\Users\\Amos Madalin Neculau\\Desktop\\FinalYearProject2\\taggy\\utils\\post.txt", "w") as postFile:
            postFile.write(sentence)

        return sentence


    #insert sentences into DB
    #TO BE ADDED PARAGRAPH IN POST
    def insertSentence(self):
        postInParagraph = 1
        sentenceInParagraph = 0
        for i in self.sentences:

            if("<br />" in i):
                postInParagraph = postInParagraph + 1
                sentenceInParagraph = 1
            else:
                sentenceInParagraph = sentenceInParagraph + 1
            with connection.cursor() as cursor:
                qry = "INSERT INTO taggy_sentences (postId, sentence, paragraphInPost, sentenceInParagraph) VALUES("+str(self.postId) + ",'" + i.replace("'","\\'") + "'," + str(postInParagraph) + "," + str(sentenceInParagraph)+")"
                cursor.execute(qry)

a = PostSegmentation(14)
print(a.postSegmentation())