
class User():

    """
    private parameters

    username - username of the user registered
    userId - id of the user registered
    userType - type of the user registered.
        user types: Admin, Annotator, Adjudecator [TO BE EXTENDED WITH PLUGIN]

    """
    _username = ""
    _userId = ""
    _userType = ""

    """
    Constructor
    """
    def __init__(self, username, userId, userType):
        self.__username = username
        self.__userId = userId
        self.__userType = userType

    """
    Function:
        Returns the username
    """
    def getUsername(self):
        return self.__username

    """
    Function:
        Returns the userId
    """
    def getUserId(self):
        return self.__userId

    """
    Function:
        Returns the userType
    """
    def getUserType(self):
        return self.__userType

    """
    Function:
        Sets the username.
        Useful when you want to change a username.

    TO ADD DATABASE UPDATE
    """
    def setUsername(self, username):

        oldUsername = self.__username
        self.__username = username
        return oldUsername

    """
    Function:
        Sets the username.
        Useful when you want to change a type.*maybe from annotator to adjudicator*

    TO ADD DATABASE UPDATE
    """
    def setUserType(self, userType):

        oldUserType = self.__userType
        self._userType = userType
        return oldUserType


    def isAdmin(self):

        toReturn = False
        if(self.__userType == "ADMIN"):
            toReturn = True
        return toReturn

    def canAdjudicate(self):

        toReturn = False
        if(self.__userType == "ADMIN" or self.__userType == "ADJUD"):
            toReturn = True
        return toReturn