from taggy.modules.Queries import Queries


class HelperMethods():


    ####
    #SET ASSIGN HELPER METHODS
    def annotators_lookup(self, qryObject):

        """

        :type qryObject: Queries
        """
        a = []
        annotators_results = qryObject.getAnnotators()

        for annotator in annotators_results:
            a[annotator['annotatorId']] = {'name':annotator['username'], 'type':annotator['usertype']}

        return a

    def annotatorssets_divs(self, qryObjdect, annotators, setId):
        divs = ""

        annotators_results = qryObjdect.getAnnotatorsSets(setId)
        for annotator in annotators_results:
            typeClass = "annotator" + self.ucfirst(annotators[annotator['annotatorID']]['type'])
            divs += " <div id='a"+ annotators['annotatorID']+"' class='annotatorInstance annotator "+typeClass+"'>"
            divs += annotators[annotator['annotatorID']]['name']
            divs += "</div> "


    def ucfirst(self, string):
        stringToReturn = string[0].upper()
        stringToReturn += string[1:]

        return stringToReturn
    # END OF  SET ASSIGN HELPER METHODS
    ####