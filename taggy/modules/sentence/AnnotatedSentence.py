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
    def __init__(self, qryObject, lookup, annotator, args):

        """

        :type annotator: Annotator
        """
        self.lookup = lookup
        self.annotator = annotator

        Sentence.__init__(args)

        self.tags[annotator.id] = self.retrieve_tags(qryObject, annotator)



    """
    * populates the tagIds array for a particular post and annotator (is post id necessary in query?)
    *
    * @param Queries $qryObject the DB Queries object
    * @param int $annotatorID id for annotator
    * @return void
    """
    def retrieve_tags(self, qryObject, a):

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
        print("<td class='tagsSentence'>")

        for(t in self.tags[self.annotator.id]):
            t.render_as_div()

        print("</td>")
