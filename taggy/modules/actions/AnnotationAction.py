from taggy.modules.Queries import Queries
import json

class AnnotationAction():
    def __init__(self):
        print('Annotation Action')
    def updateAnnotatorsTable(self, array, annotatorId):
        qryObject = Queries()

        results = qryObject.updatePostAnnotation(array['postId'], annotatorId, array['comment'], array['state'])

        if(results):
            toEncode = {
                'status': "SUCCESS",
                'postId': array['postId']
            }
        else:
            toEncode = {
                'status': "ERROR",
                'postId': array['postId']
            }

        toReturn = json.dumps(toEncode)
        return toReturn