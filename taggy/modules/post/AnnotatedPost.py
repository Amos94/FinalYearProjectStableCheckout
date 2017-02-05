from taggy.modules.post.Post import Post
#import MySQLdb
from django.db import connection

from taggy.modules.sentence.AnnotatedSentence import AnnotatedSentence

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
    lookup = None

    """
    * Annotator Object
    *
    * @var Annotator
    """
    annotator = None

    """
    * Annotator Object
    *
    * @var Annotator
    """
    annotator_states = []

    """
    * comments for this post indexed by Annotator ID
    *
    * @var array
    """
    comments = []

    """
    * Constructor of AnnotatedPost object
    *
    * @param Queries $qryObject the DB Queries object
    * @param int $pID id of Post
    """
    def __init__(self, queryObject, postId = -1, annotator):

        self.lookup = TagLookUpTable(queryObject)
        self.annotator = annotator

        # Get current PostState and Comment
        postAnnotation = self.execQuery(queryObject.getPostAnnotation(postId, annotator.getId()))
        self.annotator_states[annotator.getId()] = postAnnotation['postAnnotatorState']
        self.comments[annotator.getId()] = postAnnotation['comment']

        Post.__init__(queryObject, postId)



    """
    * addSentence()
    *
    * adds a sentence to the post's collection of sentences.  Assumes that sentences
    * are added in display order.  No sorting is done prior to display.
    *
    * @return void
    """
    def addSentence(self, qryObject, args):
        self.sentences.append(AnnotatedSentence( qryObject, self.lookup, self.annotator, args ))


    def render_table_header(self):
        print("<tr><th width='5%'></th><th width='65%'>sentence</th><th width='30%'>tags</th></tr>")

    """
    * render_finalize_button()
    *
    * renders HTML for appropriated finalize button
    *
    """
    def render_finalize_button(self, qryObject):

        if(self.annotator_states[self.annotator.id] == 'DONE' or self.annotator_states[self.annotator.id] == 'ADJUDICATED'):
            finalizeHiddenCls = "initiallyHidden"
            unfinalizeHiddenCls = ""
        else:
            finalizeHiddenCls = ""
            unfinalizeHiddenCls = "initiallyHidden"

        if(self.postState == 'ADJUDICATED'):
            finalizedDisabledCls = "finalizedDisabled"
        else:
            finalizedDisabledCls = "finalizedEnabled"

        print( "<div id='finalize' class='postBtn finalizePostBtn "+
          finalizeHiddenCls+" "+
          +finalizedDisabledCls+"'>FINALIZE</div>\n")

        print("<div id='unfinalize' class='postBtn finalizePostBtn "+
          unfinalizeHiddenCls+" "+
          finalizedDisabledCls+"'>--DONE--</div>\n")

    """
    * render_posts_annotation()
    *
    * renders HTML for populated Comment section for this post and a particular annotator
    *
    * @param Queries $qryObject a DB Queries object
    * @return void
    """
    def render_posts_annotation(self, qryObject):
        print("<div id='annotatorsCommentContainer'>\n")
        print("<i>")
        print("Comments:")
        print("</i>\n")
        print("<textarea id='annotatorsComment'>\n")
        print( self.comments[self.annotator.id])
        print("</textarea>\n")
        print("<div id='annotatorsCommentSave' class='postBtn saveCommentsBtn '>SAVE COMMENTS</div>")
        print("</div>\n")
        print("<p></p>\n")

    """
    * render_available_tags()
    *
    * renders HTML available tags for is this post
    *
    * @return void
    """
    def render_available_tags(self):
        self.lookup.render()

    """
    MYSQL QUERY EXECUTER CLASS
    """
    def execQuery(self, qry):
        # execution of the query 'qry'
        with connection.cursor() as cursor:
            cursor.execute(qry)
            # fetching all data of the query 'qry'
            qryResult = cursor.fetchall()
        return qryResult