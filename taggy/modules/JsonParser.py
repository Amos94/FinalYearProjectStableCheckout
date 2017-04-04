import json
#from taggy.modules.Queries import Queries
from taggy.modules.Queries import Queries


class JsonPostsParser():
    """
    LOADING THE POSTS.
    RETURN A JSON OBJECT
    """
    def loadPostsJSON(self, jsonString):
        jsonObject = json.loads(jsonString)
        return jsonObject

    def printPostsContent(self, jsonObject):
        for atribute, value in jsonObject:
            print(atribute+ " "+ value)


    def insertPostToDatabase(self, jsonObject):
        qryObject = Queries()
        for atribute, value in jsonObject:
            qryObject.insertPost()



a = JsonPostsParser()
b = file('C:\\Users\\Amos Madalin Neculau\\Desktop\\FinalYearProject2\\taggy\\modules\\data.json')
load = b.read()
print(load)
a.printPostsContent(load)
