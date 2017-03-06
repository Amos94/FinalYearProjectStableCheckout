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

    def __init__(self, qryObject, aID):
        """

        :type qryObject: Queries
        """
        self.id = aID
        results = qryObject.getAnnotators('', self.id)

        if(results == None):
            raise Exception('AnnotatorID ' + aID + ' does not exist.' )

        for row in results:
            username = row[1]#username
            usertype = row[3]#usertype

    """
    * am I an 'admin' user?
    *
    * @return bool true if admin
    """
    def isAdmin(self):
        return (self.usertype == "ADMIN_TYPE")

    """
    * am I an 'adjudicator' user?
    *
    * @return bool true if Annotator can Adjudicate
    """
    def canAdjudicate(self):
        return(self.usertype == "ADJUD_TYPE" or self.usertype == "ADMIN_TYPE")