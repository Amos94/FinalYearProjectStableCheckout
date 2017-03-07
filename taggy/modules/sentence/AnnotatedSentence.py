from taggy.modules.Queries import Queries
from taggy.modules.Annotator import Annotator
from taggy.modules.sentence.Sentence import Sentence

def AnnotatedSentence(Sentence):

    lookup = None
    annotator = None
    """
    * array of tagIds as integers associated with this Sentence (differs based upon annotator)
    *
    """
    tags = []




    """
    * Constructor of Sentence Object
    *
    """
    def __init__(self, lookup, annotator, args=None):

        """

        :type annotator: Annotator
        """
        qryObject = Queries()
        self.lookup = lookup
        self.annotator = annotator

        Sentence.__init__(self, args)

        self.tags[annotator.id] = self.retrieve_tags(annotator)



    """
    * populates the tagIds array for a particular post and annotator (is post id necessary in query?)
    *
    * @param Queries $qryObject the DB Queries object
    * @param int $annotatorID id for annotator
    * @return void
    """
    def retrieve_tags(self, a):
        qryObject = Queries()

        results = qryObject.getSentenceTags(self.postId, self.sentenceId, a.id)

        t = []

        for row in results:
            t.append(self.lookup.tag(row['tagID']))

        return t



    """
    * renders <td> columns for tags
    *
    * @return void
    """
    def render_tag_columns(self):
        toReturn = ''
        toReturn += "<td class='tagsSentence'>"

        for t in self.tags[self.annotator.id]:
            t.render_as_div()

        toReturn = "</td>"
        return toReturn