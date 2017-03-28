from taggy.modules.Kappa.CohensKappa import ChosenKappa
import random
#import MySQLdb
import MySQLdb
from django.db.models import Q as Q
from django.db import connection
from FYP import settings

class PostKappa():
    ck = None
    def __init__(self):
        print('PostKappa')
        ck = ChosenKappa()

    def renderPostKappa(self, postId, setId, annotatorId, adjudicateFlag):
        qry = "SELECT P.annotatorId FROM taggy_posts_annotators P INNER JOIN annotators A ON P.annotatorId = A.annotatorId WHERE postId = "+postId+" AND usertype = 'annotator';"
        with connection.cursor() as cursor:
            cursor.execute(qry)
            results = cursor.fetchall()

        if(results.count != 2):
            return

        for result in results:
            if(result):
                annotator1 = result[0]

        for result in results:
            if(result):
                annotator2 = result[0]


        query = "SELECT COUNT(DISTINCT S1.sentenceID) FROM taggy_sentences_tags S1 INNER JOIN (SELECT sentenceID FROM taggy_sentences_tags WHERE annotatorID = "+annotator2+" AND postID = "+postId+") S2 ON S1.sentenceID = S2.sentenceID WHERE S1.annotatorID = "+annotator1+" AND postID = "+postId+";"
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        totalSentences = results[0]

        query = "SELECT DISTINCT tagName FROM taggy_tags"
        with connection.cursor() as cursor:
            cursor.execute(qry)
            tags = cursor.fetchall()

        sum = 0
        for t in tags:
            tagsIDs = self.ck.getTagIDs(t[0])
            results = self.ck.countsByPost(annotator1, annotator2, tagsIDs, postId)
            neither = totalSentences - (results[0] + results[1] + results[2])
            sum += self.ck.cohensKappa(results[0], results[1], results[2], neither)

        average = sum/11
        return "<b><span id='kappaDisplay'><a href='postkappadetails.php?p="+str(postId)+"&s="+str(setId)+"&a="+annotatorId+"&f="+adjudicateFlag+"'>Kappa = "+str(average)+"</a></span></b>"