import json
from taggy.modules.Queries import Queries

"""
the JSON to be parsed must have the following shape:

[
for each table, the json will parse data and add/ create/ insert into a db
]
"""


class JsonPostsParser:
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
    
    
def insertPostToDatabase(self, qryObject):
  for atribute, value in jsonObject:
    qryObject.insertPost(value)
    
"""
{
'posts':['post':[...],'post':[...],....]
}
"""
def dumpPostsFromDatabase(self):
  
  posts = qry.getPosts()
  dump = json.dumps(posts)
  
  return dump
  
