from taggy.modules.Queries import Queries
import json

class SetAction():
    def __init__(self):
        print('Set action')

    def action(self, annotatorId, array):
        qryObject = Queries()
        if(array['action'] == 'INSERT'):
            results = qryObject.insertAnnotatorsSets(annotatorId, array['setId'])

            if(results):
                toEncode = {
                    'status': "SUCCESS",
                    'action': array['action'],
                    'annotatorId': array['annotatorId'],
                    'setId': array['setId'],
                    'msg': "Successfully assigned set "+set(array['setId'])
                }
            toReturn = json.dumps(toEncode)

        if(array['action'] == 'DELETE'):
            results = qryObject.deleteAnnotatorsSets(annotatorId, array['setId'])

            if(results):
                toEncode = {
                    'status': "SUCCESS",
                    'action': array['action'],
                    'annotatorId': array['annotatorId'],
                    'setId': array['setId'],
                    'msg': "Successfully unassigned annotator " + str(annotatorId)
                }
            toReturn = json.dumps(toEncode)

        return toReturn