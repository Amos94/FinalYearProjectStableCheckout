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

    """
    * Constructor of AdjudicatedPost object
    *
    * @param Queries $qryObject the DB Queries object
    * @param int $pID id of Post
    """
    def __init__(self, postId, annotator):

        qryObject = Queries()

        if(postId < 0):
            raise Exception("PostId "+postId+" is not valid!")

        #  Get all Annotators that have annotated this post
        # retrieve sentences for Post from DB
        results = qryObject.getAnnotatorsProgressByPost(postId)

        for r in results:
            if(r['annotatorId'] != annotator.id):
                self.others.append(Annotator( qryObject, r['annotatorId'] ))
                postAnnotation = qryObject.Queries.getPostAnnotation(postId, r['annotatorId'])
                self.annotatorStates[r['annotatorId']] = ""+postAnnotation['postAnnotatorState']
                self.comments[r['annotatorId']] = ""+postAnnotation['comment']


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

        toReturn += "<div id='finalize' class='postBtn finalizePostBtn adjudicatorPostBtn "+finalizeHiddenCls+" "+finalizedDisabledCls+"'>FINALIZE</div><br>"
        toReturn += "<div id='unfinalize' class='postBtn finalizePostBtn adjudicatorPostBtn "+unfinalizeHiddenCls+" "+unfinalizedDisabledCls+"'>--DONE--</div><br>"
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
        self.render_posts_annotation()
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