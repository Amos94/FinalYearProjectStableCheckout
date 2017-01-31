from rake_nltk import Rake
class KeyWordsExtractor:

    sentence = ""
    """
    Constructor
    :param: sentence - string
    """
    def __init__(self, sentence):
        self.sentence = sentence

    """
    getKeyWords
    returns an array with the keywords found in the sentence.
    """
    def getKeyWords(self):
        extractor = Rake()
        print(self.sentence)
        return extractor.extract_keywords_from_sentences(self.sentence)


text = KeyWordsExtractor("Cancer. Power to extend it in other creative ways, if I see fit later, without having to implement everything myself.")
print(text.getKeyWords())