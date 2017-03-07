from taggy.modules.Annotator import Annotator
from taggy.modules.Queries import Queries
from taggy.modules.post.Post import Post
#import MySQLdb
from django.db import connection
from taggy.modules.tag.TagLookUpTable import TagLook
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
    def __init__(self, postId = -1, annotator=None):
        Post.__init__(self, int(postId))

        """

        :type annotator: Annotator
        """
        queryObject = Queries()
        self.lookup = TagLook()
        self.annotator = annotator


        # Get current PostState and Comment

        postAnnotation = queryObject.getPostAnnotation(postId, annotator.id)
        print(postAnnotation)
        for r in postAnnotation:
            self.annotator_states.insert(self.annotator.id , r[3])  #postAnnotatorState
            self.comments.insert(self.annotator.id , r[0])  #comment





    """
    * addSentence()
    *
    * adds a sentence to the post's collection of sentences.  Assumes that sentences
    * are added in display order.  No sorting is done prior to display.
    *
    * @return void
    """
    def addSentences(self, args):
        a = AnnotatedSentence(self.lookup, self.annotator, args)
        self.sentences.append(a)


    def render_table_header(self):
        toReturn = ''
        toReturn += "<tr><th width='5%'></th><th width='65%'>sentence</th><th width='30%'>tags</th></tr>"
        return toReturn

    """
    * render_finalize_button()
    *
    * renders HTML for appropriated finalize button
    *
    """
    def render_finalize_button(self):
        qryObject = Queries()
        toReturn = ''
        #annotator_states[self.annotator.id]
        if(self.annotator_states[0] == 'DONE' or self.annotator_states[0] == 'ADJUDICATED'):
            finalizeHiddenCls = "initiallyHidden"
            unfinalizeHiddenCls = ""
        else:
            finalizeHiddenCls = ""
            unfinalizeHiddenCls = "initiallyHidden"

        if(self.postState == 'ADJUDICATED'):
            finalizedDisabledCls = "finalizedDisabled"
        else:
            finalizedDisabledCls = "finalizedEnabled"

        toReturn += "<div id='finalize' class='postBtn finalizePostBtn "+finalizeHiddenCls+" "+finalizedDisabledCls+"'>FINALIZE</div><br/>"

        toReturn += "<div id='unfinalize' class='postBtn finalizePostBtn "+unfinalizeHiddenCls+" "+finalizedDisabledCls+"'>--DONE--</div><br>"
        return toReturn

    """
    * render_posts_annotation()
    *
    * renders HTML for populated Comment section for this post and a particular annotator
    *
    * @param Queries $qryObject a DB Queries object
    * @return void
    """
    def render_posts_annotation(self):
        qryObject = Queries()
        toReturn = ''
        toReturn +="<div id='annotatorsCommentContainer'><br>"
        toReturn +="<i>"
        toReturn +="Comments:"
        toReturn +="</i><br>"
        toReturn +="<textarea id='annotatorsComment'><br>"
        toReturn += self.comments[0]#self.annotator.id
        toReturn +="</textarea><br>"
        toReturn +="<div id='annotatorsCommentSave' class='postBtn saveCommentsBtn '>SAVE COMMENTS</div>"
        toReturn +="</div><br>"
        toReturn +="<p></p><br>"
        return toReturn

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