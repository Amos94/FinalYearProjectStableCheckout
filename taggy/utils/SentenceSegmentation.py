import taggy.modules.post.Post
from taggy.modules.Queries import Queries
class SentenceSegmentation:


    qryObject = None
    sentenceId = 0
    words = []

    def __init__(self,sentenceId):
        """
        :type qryObject: Queries
        """
        self.qryObject = Queries()
        self.sentenceId = sentenceId
        self.words = self.sentenceSegmentation()

    def sentenceSegmentation(self):
        sentences = self.qryObject.getSentence(self.sentenceId)
        for sentence in sentences:
            s = sentence[2]

        #add case for punctuation!!!
        words = s.split(' ')

        return words

a = SentenceSegmentation(2595971)
print(a.sentenceSegmentation())