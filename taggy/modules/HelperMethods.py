from taggy.modules.Queries import Queries


class HelperMethods():


    ####
    #SET ASSIGN HELPER METHODS
    def annotators_lookup(self):
        qryObject = Queries()
        a = []
        annotators_results = qryObject.getAnnotators()

        for annotator in annotators_results:
            a.insert(annotator[0], {'name':annotator[1], 'type':annotator[3]})


        return a

    def annotatorssets_divs(self, qryObjdect, annotators, setId):
        divs = ""

        annotators_results = qryObjdect.getAnnotatorsSets(setId)
        for annotator in annotators_results:
            typeClass = "annotator" + self.ucfirst(annotators[annotator[0]][3])
            divs += " <div id='a"+ annotators[0]+"' class='annotatorInstance annotator "+typeClass+"'>"
            divs += annotators[annotator[0]][1]
            divs += "</div> "


    def ucfirst(self, string):
        stringToReturn = string[0].upper()
        stringToReturn += string[1:]

        return stringToReturn
    # END OF  SET ASSIGN HELPER METHODS
    ####