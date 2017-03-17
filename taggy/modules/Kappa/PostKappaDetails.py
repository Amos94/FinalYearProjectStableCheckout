class PostKappaDetails():
    def __init__(self):
        print('post kappa details')

    def display_nav_tagpost(self, set, post, adjudicateFlag):
        parseHtml = ''
        parseHtml += "<p></p>"

        if(set):
            if(adjudicateFlag == 'true'):
                parseHtml += "<a href=\"/set/adjudicate/?s=-1\">[go back to list of sets]</a> "
                parseHtml += "<a href=\"sadjudicate/?s="+str(set.setId)+"\">[go back to set "+str(set.setId)+"]</a> "
            else:
                parseHtml += "<a href=\"/set/tag/?s=-1\">[go back to list of sets]</a>"
                parseHtml += "<a href=\"/set/tag/?s="+str(set.setId)+"\">[go back to set "+str(set.setId)+"]</a> "
            parseHtml += "<a href='/tag/post/?&setId="+str(set.setId)+"&postId="+str(post.postId)+"&adjudicateFlag=true'>[go back to post "+str(post.postId)+"]</a> "
        elif(post):
            parseHtml += "<a href='/tag/post/?&setId="+str(set.setId)+"&postId="+str(post.postId)+"&adjudicateFlag=true'>[go back to post "+str(post.postId)+"]</a> "
            parseHtml += "<form action=\"/tag/post/ method=\"GET\">"
            parseHtml += "[tag post id: <input type=\"text\" name=\"postID\" />"
            parseHtml += "<input type=\"submit\" value=\"Submit\" /> ]"
            parseHtml += "</form>"

        return parseHtml