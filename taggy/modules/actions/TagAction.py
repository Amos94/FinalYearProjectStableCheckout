from taggy.modules.Queries import Queries
import json

class TagAction():
    def __init__(self):
        print('TagAction')

    def insertSentenceTagToDb(self, annotatorId, array):
        qryObject = Queries()

        results = qryObject.insertSentenceTag(array['sentenceId'], array['tagId'], array['postId'], annotatorId)
        if(results):
            results = qryObject.updatePostAnnotation(array['postId'], annotatorId)
        if(results):
            toEncode = {
                'status': "SUCCESS",
                'action': array['action'],
                'sentenceId': array['sentenceId'],
                'tagId': array['tagId'],
                'postId': array['postId']
            }
        else:
            toEncode = {
                'status': "ERROR",
                'action': array['action'],
                'sentenceId': array['sentenceId'],
                'tagId': array['tagId'],
                'postId': array['postId']
            }
        toReturn = json.dumps(toEncode)

        return toReturn

    def detleteSentenceTagFromDb(self, annotatorId, array):
        qryObject = Queries()

        results = qryObject.deleteSentenceTag(array['sentenceId'], array['tagId'], array['postId'], annotatorId)
        if (results):
            results = qryObject.updatePostAnnotation(array['postId'], annotatorId)
        if (results):
            toEncode = {
                'status': "SUCCESS",
                'action': array['action'],
                'sentenceId': array['sentenceId'],
                'tagId': array['tagId'],
                'postId': array['postId']
            }
        else:
            toEncode = {
                'status': "ERROR",
                'action': array['action'],
                'sentenceId': array['sentenceId'],
                'tagId': array['tagId'],
                'postId': array['postId']
            }
        toReturn = json.dumps(toEncode)

        return toReturn