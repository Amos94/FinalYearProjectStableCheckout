from taggy.modules.Kappa.CohensKappa import ChosenKappa
import random
#import MySQLdb
import MySQLdb
from django.db.models import Q as Q
from django.db import connection
from FYP import settings

class SetKappa():
    ck = None
    def __init__(self):
        self.ck = ChosenKappa()

    def chosenKappaForSet(self, setId):
        annotator1 = 10
        annotator2 = 8

        qry = "SELECT COUNT(DISTINCT S1.sentenceId) FROM taggy_sentences_tags S1 INNER JOIN (SELECT sentenceId FROM taggy_sentences_tags WHERE annotatorId = "+str(annotator2)+") S2 ON S1.sentenceId = S2.sentenceId WHERE S1.annotatorId = "+str(annotator1)+" AND EXISTS (SELECT postId FROM taggy_posts_sets P1 WHERE P1.postId = S1.postId AND P1.setId = "+str(setId)+");"
        with connection.cursor() as cursor:
            cursor.execute(qry)
            totalSentences = cursor.fetchall()

        qry = "SELECT DISTINCT tagName FROM taggy_tags"
        with connection.cursor() as cursor:
            cursor.execute(qry)
            tags = cursor.fetchall()
        sum = 0
        tagCount = 0
        for t in tags:
            tagIds = self.ck.getTagIds(t[0])
            results = self.ck.countsBySet(annotator1, annotator2, tagIds, setId)
            neither = totalSentences - (results[0] + results[1] + results[2])
            sum += self.ck.chosenKappa(results[0], results[1], results[2], neither)
            tagCount += 1

        average = sum / tagCount
        return average