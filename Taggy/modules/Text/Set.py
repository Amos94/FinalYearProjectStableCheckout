class Set():

    __setId = -1
    __setName = ""
    __setDescription = ""
    __postIds = []


    def __init__(self, setId, setName, setDescription, postIds):
        self.__setId = setId
        self.__setName = setName
        self.__setDescription = setDescription
        self.__postIds = postIds

    def containsPost(self, postId):
        toReturn = False

        for id in self.__postIds:
            if(postId == id):
                toReturn = True

        return toReturn

    #TO COMPLETE PREV POST GET POST NEXT POST ETC.