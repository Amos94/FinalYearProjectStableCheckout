import taggy.modules.post.Post
from taggy.modules.Queries import Queries
class SentenceSegmentation:


    qryObject = None
    sentenceId = 0

    def __init__(self, qryObject,sentenceId):
        """

        :type qryObject: Queries
        """
        self.qryObject = qryObject
        self.sentenceId = sentenceId

    def sentenceSegmentation(self):
        sentence = self.qryObject.getSentence(self.sentenceId)
        s = sentence[0]

        #add case for punctuation!!!
        words = s.split(' ')

        return words