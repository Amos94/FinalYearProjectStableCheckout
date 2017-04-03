import RAKE

from taggy.modules.Queries import Queries


class KeyWordsExtractor:

    sentenceId = -1
    sentence = ""
    """
    Constructor
    :param: sentence - int
    """
    def __init__(self, sentenceId):

        self.sentenceId = sentenceId
        qry = Queries()
        s=''

        sentences = qry.getSentence(self.sentenceId)
        for s in sentences:
            self.sentence = s[2]
        self.getKeyWords()


    """
    getKeyWords
    returns an array with the keywords found in the sentence.
    """
    def getKeyWords(self):
        Rake = RAKE.Rake('C:\\Users\\amosn\\Desktop\\python-rake-master\\stoplists\\SmartStoplist.txt')
        return Rake.run(self.sentence)


text = KeyWordsExtractor(2595971)
print(text.getKeyWords())