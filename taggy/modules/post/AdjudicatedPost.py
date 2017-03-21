from taggy.modules.Annotator import Annotator
from taggy.modules.Queries import Queries
from taggy.modules.post.AnnotatedPost import AnnotatedPost
from taggy.modules.sentence.AdjudicatedSentence import AdjudicatedSentence

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
    annotatorStates = []
    comments = []

    """
    * Constructor of AdjudicatedPost object
    *
    * @param Queries $qryObject the DB Queries object
    * @param int $pID id of Post
    """
    def __init__(self, postId, annotator):
        # self.others = []
        # self.annotatorStates = []
        # self.comments = []

        qryObject = Queries()

        if(int(postId) < 0):
            raise Exception("PostId "+postId+" is not valid!")

        #  Get all Annotators that have annotated this post
        # retrieve sentences for Post from DB
        results = qryObject.getAnnotatorsProgressByPost(postId)

        self.annotatorStates = [None]*100
        self.comments = [None]*100

        for r in results:
            if(int(r[0]) != annotator.id):
                i = int(r[0])
                self.others.append(Annotator( r[0] ))
                postAnnotation = qryObject.getPostAnnotation(postId, r[0])
                self.annotatorStates[i] = postAnnotation[3]
                self.comments[i] = postAnnotation[1]



        AnnotatedPost.__init__(self, postId, annotator)




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
    def addSentence(self, args):
        qryObject = Queries()
        self.sentences.append(AdjudicatedSentence(
                                                    self.annotatorStates[self.annotator.id],
                                                    self.lookup,
                                                    self.annotator,
                                                    self.others,
                                                    args)
                              )



    def render_table_header(self):
        toReturn = ''
        toReturn += "<tr><th width='5%'></th><th width='65%'>sentence</th>"
        for a in self.others:
            toReturn += "<th class='"+self.annotatorStates[a.id] +"'>tags ("+a.username+")</th>"
        toReturn += "<th class='"+ self.annotatorStates[self.annotator.id] +"'>tags (adjudicated)</th>"
        toReturn += "</tr>"
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
        if((self.annotatorStates[self.annotator.id] == 'DONE') or (self.annotatorStates[self.annotator.id] == 'ADJUDICATED')):
            finalizeHiddenCls = "initiallyHidden"
            unfinalizeHiddenCls = ""
        else:
            finalizeHiddenCls = ""
            unfinalizeHiddenCls = "initiallyHidden"

        if(self.postState == 'ADJUDICATED'):
            finalizedDisabledCls = "finalizedDisabled"
        else:
            finalizedDisabledCls = "finalizedEnabled"
        unfinalizedDisabledCls=''

        toReturn += "<div id='finalize' class='postBtn finalizePostBtn adjudicatorPostBtn btn-primary "+finalizeHiddenCls+" "+finalizedDisabledCls+"'>FINALIZE</div><br>"
        toReturn += "<div id='unfinalize' class='postBtn finalizePostBtn adjudicatorPostBtn btn-primary "+unfinalizeHiddenCls+" "+unfinalizedDisabledCls+"'>--DONE--</div><br>"
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
        toReturn += "<b><span id='othersCommentsLabel'>Other Annotators Comments: <span id='othersCommentsDisplay'>show/hide</span></span></b>"
        toReturn += "<div id='othersComments'><br>"
        toReturn += "<table><br>"

        for a in self.others:
            toReturn += "<tr>"
            toReturn += "<td class='"+ self.annotatorStates[a.id] +"'>"+a.username+"</td>"

            if(self.comments[a.id]):
                toReturn += "<td>" + self.comments[a.id] + "</td>"
            else:
                toReturn += "<td><i>no comments</i></td>"

            toReturn += "</tr><br>"

        toReturn += "</table><br>"
        toReturn += "</div><br>"
        return toReturn