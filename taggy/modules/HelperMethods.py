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
        qryObject = Queries()
        annotators_results = qryObject.getAnnotatorsSets(setId)
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
