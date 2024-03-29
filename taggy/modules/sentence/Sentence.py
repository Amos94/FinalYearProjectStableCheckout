from django.views.decorators.csrf import csrf_exempt

from taggy.modules.Annotator import Annotator
from taggy.modules.Queries import Queries


class Sentence():
    """
    * id of containing post
    *
    * @var int
    """
    postId = 0

    """
    * id of sentence
    *
    * @var int
    """
    sentenceID = 0

    """
    * display ready text of sentence
    *
    * @var string
    """
    sentence = ""

    """
    * number of paragraph which sentence belongs to (count starts with 1)
    *
    * @var int
    """
    paragraphInPost = 0

    """
    * number of sentence within paragraph (count starts with 1)
    *
    * @var int
    """
    sentenceInParagraph = 0


    def __init__(self, postId, sentenceId, sentence, paragraphInPost, sentenceInParagraph):
        self.postId = postId
        self.sentenceID = sentenceId
        self.sentence = sentence
        self.paragraphInPost = paragraphInPost
        self.sentenceInParagraph = sentenceInParagraph

    def getPostId(self):
        return self.postId

    def getSentenceId(self):
        return self.sentenceID

    def getSentence(self):
        return self.sentence

    def getParagraphInPost(self):
        return self.paragraphInPost

    def getSentenceInParagraph(self):
        return self.sentenceInParagraph



    """
    * renders the sentence as an HTML table row (i.e. a <tr>)
    *
    * @param array $tagLookup a tag lookup table, an associated array of Tag objects
    * indexed by their tag id
    * @return void
    """

    @csrf_exempt
    def render_as_row(self, postId, sentenceId, annotatorId, adjudicationFlag):

        toReturn = ''
        toReturn += '<tr id="s'+ str(self.sentenceID) +'" class="sentenceRow">'
        toReturn += '<td align="right" valign="middle">'+str(self.paragraphInPost)+"-"+str(self.sentenceInParagraph)+'</td>'
        toReturn += '<td align="left" valign="middle">'+self.sentence+'</td>'

        toReturn += '<td align="left" valign="middle">'+self.render_tag_columns(postId, sentenceId, annotatorId, adjudicationFlag)+'</td>'

        toReturn += "</tr>"
        return toReturn
    #if is Annotated, show the tag
    #else, make annotation possible
    @csrf_exempt
    def render_tag_columns(self, postId, sententenceId,annotatorId, adjudicationFlag):
        qryObject = Queries()
        toReturn = ''
        results = []
        annotator = Annotator(annotatorId)

        #doesn't matter if it is setted to true by GET, if annotator cannot adjudicate, then adjudicationFlag = false
        if(not annotator.canAdjudicate()):
            adjudicationFlag = 'false'

        if(annotator.canAdjudicate() and adjudicationFlag == 'true'):
            #SEE TAGS FROM ALL USERS THAT ANNOTATED THAT SENTENCE
                annotators = qryObject.getAnnotatorsForPost(postId)
                for annotator in annotators:
                    results = qryObject.getSentenceTags(postId, sententenceId, annotator[0])
                    for result in results:
                        tags = qryObject.getTag(str(result[2]))
                        for tag in tags:
                            toReturn += tag[1] + " - " + tag[3] + "<br />"
        elif(annotator.canAdjudicate()and adjudicationFlag == 'false'):
            # an adjudicator can annotate as well
            # make a form
            #annotate
            #ETC.

            results = []
            results = qryObject.getTagAndPOR()
            toReturn += '<center>'
            toReturn += '<form action="/tag/update-db/" method="post">\n'
            toReturn += '<select multiple class="form-control text-center" name="taskOption">'
            for result in results:
                if (result[2] == 'P'):
                    #TAGID, ANNOTATORID, POSTID, SENTENCEID
                    toReturn += '<option selected="selected" value="' + "" +str(result[0]) + " "+str(annotatorId) + " "+str(postId)+" "+str(sententenceId)+'">' + str(result[1]) + " & " + 'PROVIDE' + "</option>"
                elif (result[2] == 'R'):
                    toReturn += '<option selected="selected" value="' + "" +str(result[0]) + " "+str(annotatorId) + " "+str(postId)+" "+str(sententenceId)+'">' + str(result[1]) + " & " + 'REQUEST' + "</option>"
                else:
                    toReturn += '<option selected="selected" value="' + "" +str(result[0]) + " "+str(annotatorId) + " "+str(postId)+" "+str(sententenceId)+'">' + str(result[1]) +  "</option>"
            toReturn += '</select>'

            toReturn += '<input class="btn btn-primary" type="submit" value="Submit" />'
            toReturn += '</form>'
            toReturn += '</center>'

        else:
            #if already annotated by current user(that cannot adjudicate), show the tag assigned
            annotators = []
            annotators = qryObject.getAnnotatorsForPost(postId)

            sentenceIsAnnotatedByUser = True
            afs = []
            afs = qryObject.getSentenceAnnotator(sententenceId, annotatorId)

            if(not afs):
                sentenceIsAnnotatedByUser = False

            tof = False
            for annotator in annotators:
                if(annotator[0] == annotatorId and sentenceIsAnnotatedByUser):
                    tof = True

            if(tof):
                results = qryObject.getSentenceTags(postId, sententenceId, annotatorId)
                for result in results:
                    tags = qryObject.getTag(str(result[2]))
                    for tag in tags:
                        if(tag[4] == 1):
                            toReturn += tag[1] + "-" + tag[3] + "<br />"
                        else:
                            toReturn += tag[1] + "<br />"
                toReturn += "<a href='/post/update-tag/?sentence="+str(sententenceId)+"&annotator="+str(annotatorId)+"&post="+str(postId)+"'>[EDIT SENTENCE TAGS]</a>"
            #else annotate
            else:
                # make a form
                # annotate
                results = []
                results = qryObject.getTagAndPOR()
                toReturn += '<center>'
                toReturn += '<form action="/tag/update-db/" method="post">\n'
                toReturn += '<select multiple class="form-control text-center" name="taskOption">'
                for result in results:
                    if (result[2] == 'P'):
                        # TAGID, ANNOTATORID, POSTID, SENTENCEID
                        toReturn += '<option selected="selected" value="' + "" + str(result[0]) + " " + str(annotatorId) + " " + str(
                            postId) + " " + str(sententenceId) + '">' + str(result[1]) + " & " + 'PROVIDE' + "</option>"
                    elif (result[2] == 'R'):
                        toReturn += '<option selected="selected" value="' + "" + str(result[0]) + " " + str(annotatorId) + " " + str(
                            postId) + " " + str(sententenceId) + '">' + str(result[1]) + " & " + 'REQUEST' + "</option>"
                    else:
                        toReturn += '<option selected="selected" value="' + "" + str(result[0]) + " " + str(annotatorId) + " " + str(
                            postId) + " " + str(sententenceId) + '">' + str(result[1]) + "</option>"
                toReturn += '</select>'

                toReturn += '<input class="btn btn-primary" type="submit" value="Submit" />'
                toReturn += '</form>'
                toReturn += '</center>'


        return toReturn