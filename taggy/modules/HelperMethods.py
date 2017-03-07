from taggy.modules.Queries import Queries


class HelperMethods():


    ####
    #SET ASSIGN HELPER METHODS
    def annotators_lookup(self):
        qryObject = Queries()
        a = []
        annotators_results = qryObject.getAnnotators()

        for annotator in annotators_results:
            a.insert(annotator[0], {'id':annotator[0],'name':annotator[1], 'type':annotator[3]})


        return a

    def annotatorssets_divs(self, annotators, setId):
        divs = ""
        print(annotators)
        qryObject = Queries()
        annotators_results = qryObject.getAnnotatorsSets(setId)
        print(annotators_results)
        for annotator in annotators_results:
            typeClass = "annotator" + self.ucfirst(annotators[annotator[0]]['type'])
            divs += " <div id='a"+ str(annotator[0])+"' class='annotatorInstance annotator "+typeClass+"' setId='"+str(setId)+"'>"
            divs += annotators[annotator[0]]['name']
            divs += "</div> "
        return divs


    def ucfirst(self, string):
        stringToReturn = string[0].upper()
        stringToReturn += string[1:]

        return stringToReturn
    # END OF  SET ASSIGN HELPER METHODS
    ####



    ####
    #SET BROWSE HELPER METHODS

    # def renderAnnotationProgress(self, setId):
    #     qryObject = Queries()
    #     posts = qryObject.getSet(setId)
    #     counter = 0
    #     for post in posts:
    #         counter = counter +1
    #     total_posts = counter
    #
    #     results = qryObject.getAnnotatorsSets(setId)
    #     counter = 0
    #     for result in results:
    #         counter = counter + 1
    #
    #     progress = ""
    #     for result in results:
    #         annotator_results = qryObject.getAnnotatorsProgressInSet( result[1], setId )
    #         if (counter) > 0):
    #             annotator = annotator_results
    #             progress += annotator[1]+"("+annotator[0]+"/"+total_posts+") "
    #         else:
    #             annotator_results = qryObject.getAnnotators(annotator[0])
    #             annotator = annotator_results
    #             progress += annotator[1]+"(0/"+ total_posts+") "
    #
    #     return progress
    # END OF  SET BROWSE HELPER METHODS
    ####

    ####
    #TAG POST HELPER METHODS



    def display_nav_tagpost(self, set, post, adjudicateFlag):
        toReturn = ''
        if(set):
            if(adjudicateFlag == 'true'):
                toReturn += '<a href="/set/adjudicate/?s=-1">[go back to list of sets]</a> '
                toReturn +='<a href="/set/adjudicate./?s='+set.setId+'>[go back to set '+set.setId+']</a> '

                prevPostId = set.getPrevPostId(post.postId)
                if(prevPostId < 0):
                    toReturn +='[ <i>at BEGINNING of set</i> ] '
                else:
                    toReturn +='<a href="/post/tag/?setId='+set.setId+'&postId='+prevPostId+'&adjudicateFlag=true>[adjudicate PREVIOUS post in set]</a> '

                nextPostId = set.getNextPostId(post.postId)
                if(nextPostId < 0):
                    toReturn += "[ <i>at END of set</i> ] "
                else:
                    toReturn += '<a href="/post/tag/?setId='+set.setId+'&postId='+nextPostId+'&adjudicateFlag=true>[adjudicate NEXT post in set]</a> '

            else:
                toReturn += '<a href="/set/adjudicate/?s=-1">[go back to list of sets]</a> '
                toReturn += '<a href="/set/adjudicate./?s=' + set.setId + '>[go back to set ' + set.setId + ']</a> '

                prevPostId = set.getPrevPostId(post.postId)
                if (prevPostId < 0):
                    toReturn += '[ <i>at BEGINNING of set</i> ] '
                else:
                    toReturn += '<a href="/post/tag/?setId=' + set.setId + '&postId=' + prevPostId + '&adjudicateFlag=false>[tag PREVIOUS post in set]</a> '

                nextPostId = set.getNextPostId(post.postId)
                if (nextPostId < 0):
                    toReturn += "[ <i>at END of set</i> ] "
                else:
                    toReturn += '<a href="/post/tag/?setId=' + set.setId + '&postId=' + nextPostId + '&adjudicateFlag=false>[tag NEXT post in sett]</a> '

        elif(post):
            toReturn += '<form action="/post/tag/?method="get">'
            toReturn += '[tag post id: <input type="text" name="postId" />'
            toReturn += '<input type="submit" value="Submit" /> ]'
            toReturn += '</form>'

        return toReturn

    # END OF  TAG POST HELPER METHODS
    ####