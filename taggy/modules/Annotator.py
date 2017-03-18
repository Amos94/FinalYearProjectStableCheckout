from taggy.modules.Queries import Queries

class Annotator:

    """
    * id of user
    *
    * @var int
    """
    id = 0

    """
    * verbose system name
    *
    * @var string
    """
    username = ""

    """
    * type of user
    *
    * @var string
    """
    usertype = ""

    def __init__(self, aID):
        """

        :type qryObject: Queries
        """
        qryObject = Queries()
        self.id = int(aID)
        results = qryObject.getAnnotators('', self.id)

        if(results == None):
            raise Exception('AnnotatorID ' + aID + ' does not exist.' )

        for row in results:
            username = row[1]#username
            usertype = row[3]#usertype

            print('usertype= '+ usertype)

    """
    * am I an 'admin' user?
    *
    * @return bool true if admin
    """
    def isAdmin(self):
        return (self.usertype == "admin")

    """
    * am I an 'adjudicator' user?
    *
    * @return bool true if Annotator can Adjudicate
    """
    def canAdjudicate(self):
        toReturn = False

        print self.usertype

        if(self.usertype == 'adjudicator'):
            toReturn = True

        if(self.usertype == 'admin'):
            toReturn = True

        return toReturn