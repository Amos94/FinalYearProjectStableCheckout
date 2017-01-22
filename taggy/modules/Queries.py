from django.db.models import Q as Q
from taggy.models import annotators as Annotators
from taggy.models import posts as Posts
from taggy.models import posts_annotators as Posts_annotators
from django.db import connection

class Queries:





    """
   * getAnnotators()
   *
   * returns data from annotators table with username matching argument
   * If none is given, then return the entire Annotators table.
   *
   * @param text $usr  username argument
   * @param text $userid  (alternatively) query by annotatorID argument
    """
    def getAnnotators(self, username='', userid=None):

        if (username != ''):
            qryResult = Annotators.objects.filter(username__exact=username)
        elif (userid != None):
            qryResult = Annotators.objects.filter(annotatorId__exact=userid)
        else:
            qryResult = Annotators.objects.all()

        return qryResult







    """
   * getAnnotatorsForPost()
   *
   * returns the Annotator IDs for a particular Post ID
   *
   * @param integer $postid  postID
    """
    def getAnnotatorsForPost(self, postid):

        #Building the query
        qry =  "SELECT TAGGY_posts_annotators.annotatorId, TAGGY_annotators.username "
        qry += "FROM TAGGY_post_annotators, TAGGY_annotators "
        qry += "WHERE postId='"+postid+"' "
        qry += "AND TAGGY_annotators.usertype='ANNOT_TYPE' "
        qry += "AND TAGGY_posts_annotators.annotatorId = TAGGY_annotators.annotatorId "
        qry += "ORDER BY TAGGY_posts_annotators.annotatorId"

        #execution of the query 'qry'
        with connection.cursor() as cursor:
            cursor.execute(qry)
            #fetching all data of the query 'qry'
            qryResult = cursor.fetchall()

        #return the data
        return qryResult







    """
    * getAnnotatorsForSet()
    *
    * returns the Annotator IDs for a particular Set ID
    *
    * @param integer $setid  set ID
    """
    def getAnnotatorsForSet(self, setid):

        qry = ""

        with connection.cursor() as cursor:
            cursor.execute(qry)
            qryResult = cursor.fetchall()

        return qryResult