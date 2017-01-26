from taggy.modules.post.Post import Post
#import MySQLdb
from django.db import connection


"""
* AnnotatedPost Class
*
* represents an Annotated Post in the bcforumdb
*
* @package default
"""
class AnnotatedPost(Post):
    """
    * a TagLookupTable to utilize in displaying tags for this Post
    *
    * @var TagLookupTable
    """
    __lookup = None

    """
    * Annotator Object
    *
    * @var Annotator
    """
    __annotator = None

    """
    * Annotator Object
    *
    * @var Annotator
    """
    __annotator_states = []

    """
    * comments for this post indexed by Annotator ID
    *
    * @var array
    """
    __comments = []

    """
    * Constructor of AnnotatedPost object
    *
    * @param Queries $qryObject the DB Queries object
    * @param int $pID id of Post
    """
    def __init__(self, queryObject, postId = -1, annotator):

        self.__lookup = TagLookUpTable(queryObject)
        self.__annotator = annotator

        # Get current PostState and Comment
        postAnnotation = self.execQuery(queryObject.getPostAnnotation(postId, annotator.getId()))
        self.__annotator_states[annotator.getId()] = postAnnotation['postAnnotatorState']
        self.__comments[annotator.getId()] = postAnnotation['comment']

        Post.__init__(queryObject, postId)


    def execQuery(self, qry):
        # execution of the query 'qry'
        with connection.cursor() as cursor:
            cursor.execute(qry)
            # fetching all data of the query 'qry'
            qryResult = cursor.fetchall()
        return qryResult