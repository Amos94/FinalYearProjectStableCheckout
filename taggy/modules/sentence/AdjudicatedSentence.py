from taggy.modules.Queries import Queries
from taggy.modules.sentence.Sentence import Sentence
from taggy.modules.sentence.AnnotatedSentence import AnnotatedSentence

def AdjudicatedSentence(AnnotatedSentence):


    """

    :param AnnotatedSentence:
    :return:
    """

    """
    * other Annotators
    *
    """
    others = []

    """
    * Constructor of AdjudicatedSentence Object
    *
    """
    def AdjudicatedSentence(self, qryObject, annotatorState, lookup, annotator, others, args ):

        AnnotatedSentence.__init__(qryObject, lookup, annotator, args)
        self.others = others

        union_tags = False