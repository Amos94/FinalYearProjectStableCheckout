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
    def AdjudicatedSentence(self, annotatorState, lookup, annotator, others, args ):
        qryObject = Queries()
        AnnotatedSentence.__init__(lookup, annotator, args)
        self.others = others
        """
        If Adjudicator has no tags for this sentence, create a Union of Tags from all current Annotators
        """
        union_tags = False

        if((len(self.tags[annotator.id]) == 0 and annotatorState != 'DONE')):
            union_tags = True
        #Retrieve tags for the other Annotators
        for a in self.others:
            self.tags[a.id] = self.retrieve_tags(qryObject, a)
            if(union_tags):#Assemble the union of the other Annotator's Tags
                self.tags[annotator.id] = dict(self.tags[annotator.id], **self.tags[a.id])

        #remove dups from this Adjudicator's tag set
        self.tags[annotator.id] = list(set(self.tags[annotator.id]))

        #Initialize Adjudicator's tag set in the DB if necessary
        if (union_tags):
            for t in self.tags[self.annotator.id]:
                results = qryObject.insertSentenceTag(self.sentenceId, t.tagId, self.postId, annotator.id )
            # update the post's this Adjudicator's tag count
            results = qryObject.updatePostAnnotation( self.postId, annotator.id  )


    """
    * populates the tagIds array for a particular post and annotator (is post id necessary in query?)
    *
    * @param Queries $qryObject the DB Queries object
    * @param int $annotatorID id for annotator
    * @return void
    """
    def retrieve_tags(self, qryObject, annotator):

        results = qryObject.getSentenceTags( self.postId, self.sentenceId, annotator.id )
        t = []

        for row in results:
            t.append(self.lookup.tag(row['tagID']) )

        return t


    #renders <td> columns for tags
    def render_tag_columns(self):
        toReturn = ''
        for a in self.others:

            toReturn += "<td>"

            for t in self.tags[a.id]:
                t.render_as_div( False,  False)

            toReturn +="</td>"

        toReturn +="<td class='tagsSentence'>"

        for t in self.tags[self.annotator.id]:
            t.render_as_div(False)

        toReturn +="</td>"
        return toReturn