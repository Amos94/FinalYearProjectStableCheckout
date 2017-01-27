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
    def render_as_row(self):
        print("<tr id='s"+ self.sentenceID +"' class='sentenceRow'>")
        print("<td align=\"right\" valign=\"middle\">"+self.paragraphInPost+"."+self.sentenceInParagraph+"</td>")
        print("<td align=\"left\" valign=\"middle\">"+self.sentence+"</td>")

        self.render_tag_columns()

        print("</tr>\n")

    def render_tag_columns(self):
        return