from taggy.modules.Queries import  Queries
import sys

class Kappa:

    postId = 0

    """
    *Constructor for the Kappa object
    """
    def __init__(self, postId):
        self.postId = postId


    """
    * getAnnotatorIDsString()
    *
    * queries the database to get the annotatorID number(s) of the annotators
    * who annotated this post. The string is formatted like this:
    * $annIDString = "(9,10)" -- if there are multiple tagIDs that match the name
    * $annIDString = "(9)" -- if there is only one tagID that matches the name
    * $annIDString = "()" -- if no tagIDs match the name
    """

    def getAnnotatorIDsString(self, qryObject):
        """
        :type qryObject: Queries
        """

        annIDsString = "("
        results  = qryObject.getAnnotatorsForPost(self.postId)
        num = results.count()
        for i in range(0, num):
            annIDsString += results['annotatorId']

            if(i < num-1):
                annIDsString += ","
        annIDsString += ")"
        return annIDsString


    """
    * getTagIDsString()
    *
    * queries the database to get the tagID number(s) that match(es)
    * the $tagName member variable, and formats the string like this:
    *
    * $tagIDString = "(9,10)" -- if there are multiple tagIDs that match the name
    * $tagIDString = "(9)" -- if there is only one tagID that matches the name
    * $tagIDString = "()" -- if no tagIDs match the name
    """
    def getTagIDsString(self, qryObject, tagName):
        """
            :type qryObject: Queries
            """

        tagIDsString = "("
        results = qryObject.getTagIDs(tagName)
        num = results.count()
        for i in range(0, num):
            tagIDsString += results['tagId']

            if (i < num - 1):
                tagIDsString += ","
            tagIDsString += ")"
        return tagIDsString

    """
    * getTagKappa()
    *
    * queries the database for the list of sentences in $this->postid
    * where either annotator (listed in $annIDs, there should be 2
    * entries) used the tags in $tagIDs;
    * then tallies:
    *   the number of sentences tagged by the first annotator ($annIDs[0]) but not the second
    *   the number of sentences tagged by the second annotator ($annIDs[1]) but not the first
    *   the number of sentences tagged by both
    """
    def getTagKappa(self, qryObject, tagIDs, annIDs ):
        """

        :type qryObject: Queries
        """
        ann1 = annIDs[0]
        ann2 = annIDs[1]
        ann1Only = 0
        ann2Only = 0
        both = 0
        neither = 0
        results = qryObject.getTagMatchesByPost(self.postId, tagIDs, annIDs)
        num_results = results.count()
        annCount = []
        if(num_results > 0):
            sentenceID = -1
            annCount[0] = 0
            annCount[1] = 0

            for row in results:
                print("row=["+row['sentenceId']+","+row['annotatorId']+"] ")

                if(sentenceID == -1):
                    sentenceID = row['sentenceID']
                    if(row['annotatorId'] == ann1):
                        annCount[0] = annCount[0]+1
                    else:
                        annCount[1] = annCount[1] + 1

                elif(row['sentenceId'] == sentenceID):
                    if(row['annotatorId'] == ann1):
                        annCount[0] = annCount[0] + 1
                    else:
                        annCount[1] = annCount[1] + 1
                else:
                    if(annCount[0] > 0):
                        if(annCount[1] > 0):
                            both =  both+1
                            print("both <br />")
                        else:
                            ann1Only = ann1Only+1
                            print("ann1<br />")
                    else:
                        if(annCount[1] > 0):
                            ann2Only = ann2Only + 1
                            print("ann2<br />")
                        else:
                            neither = neither + 1
                            print(" neither<br />")
                    sentenceID = row['sentenceId']
                    annCount[0] = 0
                    annCount[1] = 0
                    if ( row['annotatorId'] == ann1 ):
                        annCount[0] = annCount[0] + 1;
                    else :
                        annCount[1] = annCount[1] + 1;

                print(sys.stdout.flush())

            if(annCount[0] > 0):
                if(annCount[1] > 0):
                    both = both + 1
                    print(" both<br />")
                else:
                    ann1Only = ann1Only + 1
                    print(" ann1<br />")
            else:
                if(annCount[1] > 0 ):
                    ann2Only = ann2Only + 1
                    print(" ann2<br />")
                else:
                    neither = neither + 1
                    print(" neither<br />")
            print(sys.stdout.flush())
            array = [ ann1Only, ann2Only, both, neither ]
            return array
        else:
            return None



    """
    * cohensKappa()
    *
    """
    def chosensKappa(self, ann1Only, ann2Only, both, neither):
        total = ann1Only + ann2Only + both + neither
        prA = (both + neither) / total
        prOneYes = (both + ann1Only) / total
        prTwoYes = (both + ann2Only) / total
        prOneNo = (ann2Only + neither) / total
        prTwoNo = (ann1Only + neither) / total
        prE = (prOneYes * prTwoYes) + (prOneNo * prTwoNo)

        if(ann1Only == 0 and ann2Only == 0):
            ck = 1
        else:
            ck = (prA - prE) / (1 - prE)

        return ck
