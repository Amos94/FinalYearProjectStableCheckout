import random

#import MySQLdb
import MySQLdb
from django.db.models import Q as Q

from django.db import connection
from FYP import settings

class CohensKappa():
    def __init__(self):
        print('CohensKappa')

    def countsByPost(self, ann1, ann2, tagIds, postId):

        tags = '('

        for tagId in tagIds:
            tags += "'"+str(tagId[0]) + "', "
        tags = tags[:-2]
        tags += ")"

        masterSQL = ''
        masterSQL += "SELECT DISTINCT S1.sentenceId "
        masterSQL += "FROM taggy_sentences_tags S1 "
        masterSQL += "INNER JOIN (SELECT sentenceId FROM taggy_sentences_tags WHERE annotatorId = "+str(ann2)
        masterSQL += ") S2 "
        masterSQL += "ON S1.sentenceId = S2.sentenceId "
        masterSQL += "WHERE S1.annotatorId = "+str(ann1)
        masterSQL += " "
        masterSQL += "AND S1.tagId IN "+tags
        masterSQL += " "
        masterSQL += "AND S1.postId = "+str(postId)
        masterSQL += " "
        masterSQL += "ORDER BY S1.sentenceId"


        slaveSQL = ''
        slaveSQL += "SELECT DISTINCT S1.sentenceId "
        slaveSQL += "FROM taggy_sentences_tags S1 "
        slaveSQL += "INNER JOIN (SELECT sentenceId FROM taggy_sentences_tags WHERE annotatorId = "+str(ann1)
        slaveSQL += ") S2 "
        slaveSQL += "ON S1.sentenceId = S2.sentenceId "
        slaveSQL += "WHERE S1.annotatorId = "+str(ann2)
        slaveSQL += " "
        slaveSQL += "AND S1.tagId IN "+tags
        slaveSQL += " "
        slaveSQL += "AND S1.postId = "+str(postId)
        slaveSQL += " "
        slaveSQL += "ORDER BY S1.sentenceId"

        return self.counts(masterSQL, slaveSQL)

    def countsBySet(self, ann1, ann2, tagIds, setId):
        masterSQL = ''
        masterSQL += "SELECT DISTINCT S1.sentenceId "
        masterSQL += "FROM taggy_sentences_tags S1 "
        masterSQL += "INNER JOIN (SELECT sentenceId FROM taggy_sentences_tags WHERE annotatorId = "+str(ann2)+") S2 "
        masterSQL += "ON S1.sentenceId = S2.sentenceId "
        masterSQL += "WHERE S1.annotatorId = "+str(ann1)+" "
        masterSQL += "AND S1.tagId IN "+str(tagIds)+" "
        masterSQL += "AND EXISTS (SELECT postId FROM taggy_posts_sets P1 WHERE P1.postId = S1.postId AND P1.setId = "+str(setId)+") "
        masterSQL += "ORDER BY S1.sentenceId;"

        slaveSQL = ''
        slaveSQL += "SELECT DISTINCT S1.sentenceId "
        slaveSQL +=  "FROM taggy_sentences_tags S1 "
        slaveSQL += "INNER JOIN (SELECT sentenceId FROM taggy_sentences_tags WHERE annotatorId = "+str(ann1)+") S2 "
        slaveSQL += "ON S1.sentenceId = S2.sentenceId "
        slaveSQL += "WHERE S1.annotatorId = "+str(ann2)+" "
        slaveSQL += "AND S1.tagId IN "+str(tagIds)+" "
        slaveSQL += "AND EXISTS (SELECT postId FROM taggy_posts_sets P1 WHERE P1.postId = S1.postId AND P1.setId = "+str(setId)+") "

        slaveSQL +=  "ORDER BY S1.sentenceId;"
        return self.counts( masterSQL, slaveSQL )

    def counts(self, masterSQL, slaveSQL):

        # execution of the query masterSQL
        with connection.cursor() as cursor:
            cursor.execute(masterSQL)
            master = cursor.fetchall()

        # execution of the query slaveSQL
        with connection.cursor() as cursor:
            cursor.execute(slaveSQL)
            slave = cursor.fetchall()

        ann1Only = 0
        ann2Only = 0
        both = 0

        if(master and slave):
            for m,s in zip(master, slave):
                if(m['stentenceId'] == s['sentenceId']):
                    both = both+1
                elif(m['stentenceId'] > s['sentenceId']):
                    ann2Only = ann2Only + 1
                elif(m['stentenceId'] < s['sentenceId']):
                    ann1Only = ann1Only + 1

        return [ann1Only, ann2Only, both]

    def chosenKappa(self, ann1Only, ann2Only, both, neither):
        total = ann1Only + ann2Only + both + neither
        prA = (both + neither) / total
        prOneYes = (both + ann1Only) / total
        prTwoYes = (both + ann2Only) / total
        prOneNo = (ann2Only + neither) / total
        prTwoNo = (ann1Only + neither) / total
        prE = (prOneYes * prTwoYes) + (prOneNo * prTwoNo)

        if (ann1Only == 0 and ann2Only == 0):
            ck = 1
        else:
            ck = (prA - prE) / (1 - prE)

        return ck

    def getTagIds(self, tagName):
        switcher = {
            "PERS":'(1,2)',
            "FIND": '(3,4)',
            "TEST": '(5,6)',
            "DIAG": '(7,8)',
            "TREA": '(9,10)',
            "HSYS": '(11,12)',
            "DAIL": '(13,14)',
            "NUTR": '(15,16)',
            "ALTR": '(17,18)',
            "RSRC": '(19,20)',
            "MISC": '(21,22)'
        }

        return switcher.get(tagName, "nothing")
