from taggy.modules import Queries
from taggy.modules.post.AnnotatedPost import AnnotatedPost

"""
 * AdjusdicatedPost Class
 *
 * represents an Adjudicated Post in the bcforumdb
 *
 * @package default
"""

class AdjudicatedPost(AnnotatedPost):

    """
    * Other Annotators
    """
    others = []

    """
    * Constructor of AdjudicatedPost object
    *
    * @param Queries $qryObject the DB Queries object
    * @param int $pID id of Post
    """
    def __init__(self, qryObject, postId, annotator):

        qryObject = Queries



        if(postId < 0):
            raise Exception("PostId "+postId+" is not valid!")

        #  Get all Annotators that have annotated this post
        # retrieve sentences for Post from DB
        results = qryObject.Queries.getAnnotatorsProgressByPost(postId)

        for r in results:
            if(r['annotatorId'] != annotator.id):
                self.others.append(Annotator( qryObject, r['annotatorId'] ))
                postAnnotation = qryObject.Queries.getPostAnnotation(postId, r['annotatorId'])
                self.annotatorStates[r['annotatorId']] = ""+postAnnotation['postAnnotatorState']
                self.comments[r['annotatorId']] = ""+postAnnotation['comment']


        AnnotatedPost.__init__(qryObject, postId, annotator)




        self.comments[self.annotator.id] = '[' + self.annotator.username +':'+self.comments[self.annotator.id] + ']'

        for a in self.others:
            self.comments[self.annotator.id] = '[' + a.username + ':' + self.comments[a.id] + ']'


    """
    * addSentence()
    *
    * adds a sentence to the post's collection of sentences.  Assumes that sentences
    * are added in display order.  No sorting is done prior to display.
    *
    """
