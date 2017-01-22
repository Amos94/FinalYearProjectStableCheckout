from django.db.models import Q as Q
from taggy.models import annotators as Annotators
from taggy.models import posts as Posts
from taggy.models import posts_annotators as Posts_annotators
from django.db import connection

class Queries:


    #----- FUNCTIONS THAT HANDLE ANNOTATORS -------------------------------------


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

        #Building the SQL query
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

        # Building the SQL query
        qry =  "SELECT taggy_annotators_sets.annotatorId, taggy_annotators.username "
        qry += "FROM taggy_annotators_sets, taggy_annotators "
        qry += "WHERE setId='"+setid+"' "
        qry += "AND taggy_annotators.usertype='ANNOT_TYPE.' "
        qry += "AND taggy_annotators_sets.annotatorId = taggy_annotators.annotatorId "
        qry += "ORDER BY taggy_annotators_sets.annotatorId"

        # execution of the query 'qry'
        with connection.cursor() as cursor:
            cursor.execute(qry)
            # fetching all data of the query 'qry'
            qryResult = cursor.fetchall()

        # return the data
        return qryResult






    """
   * getAnnotatorsProgressByPost()
   *
   * returns the Annotator IDs, and progress for a particular Post ID
   *
   * @param text $usr  username argument
   * @param text $userid  (alternatively) query by annotatorID argument
    """

    def getAnnotatorsProgressByPost(self, postId, state=''):

        # Building the SQL query
        qry =  "SELECT annotatorId,(numSentencesInPost / numSentencesInPost) as progress, lastUpdated, postAnnotatorState as state "
        qry += "FROM taggy_posts_annotators "
        qry += "WHERE postId='"+postId+"' "

        if(state):
            qry += "AND postAnnotatorState='"+state+"'"


        # execution of the query 'qry'
        with connection.cursor() as cursor:
            cursor.execute(qry)
            # fetching all data of the query 'qry'
            qryResult = cursor.fetchall()

        # return the data
        return qryResult


    """
    * getPostAnnotatorsAndStates()
    *
    * returns the Annotator IDs, username and state for a particular Post ID
    *
    * @param text $postid
    """

    def getPostAnnotatorsAndStates(self, postid):
        # Building the SQL query
        qry =  "SELECT username, postAnnotatorState"
        qry += "FROM taggy_annotators, taggy_posts_annotators "
        qry += "WHERE postId='"+postid+"' "
        qry += "AND taggy_posts_annotators.annotatorId = taggy_annotators.annotatorId"


        # execution of the query 'qry'
        with connection.cursor() as cursor:
            cursor.execute(qry)
            # fetching all data of the query 'qry'
            qryResult = cursor.fetchall()

        # return the data
        return qryResult

    """
   * insertAnnotator()
   *
   * inserts a new annotator account into the DB (assumes that dupe check already has
   * happened)
   *
   * @param text $username  username argument
   * @param text $password  user's password argument
   * @param text $usertype  user type (default is ANNOT_TYPE)
    """

    def insertAnnotator(self,  username, password, usertype='ANNOT_TYPE'):
        # Building the SQL query
        qry =  "INSERT INTO  annotators (username, password, usertype) "
        qry += "VALUES ('"+username+"','"+password+"','"+usertype+"')"


        # execution of the query 'qry'
        with connection.cursor() as cursor:
            cursor.execute(qry)
            # fetching all data of the query 'qry'
            qryResult = cursor.fetchall()

        # return the data
        return qryResult


    """
   * updateAnnotator()
   *
   * update an annotator account with a new password
   *
   * @param text $username  username argument
   * @param text $password  user's password argument
    """

    def updateAnnotator(self,  username, password='', usertype=''):
        # Building the SQL query
        updates = []

        if(password):
            updates.append("password= '"+password+"' ")

        if(usertype):
            updates.append("usertype= '"+usertype+"' ")

        qry =  "UPDATE taggy_annotators SET"
        qry += ",".join(updates)
        qry += "WHERE (username='"+username+"')"


        # execution of the query 'qry'
        with connection.cursor() as cursor:
            cursor.execute(qry)
            # fetching all data of the query 'qry'
            qryResult = cursor.fetchall()

        # return the data
        return qryResult


    #----- FUNCTIONS THAT HANDLE FORUMS -----------------------------------------


    """
    * getForums()
    *
    * returns all data from forums table
    *
    * NOTE: the differences between PERSEUS and LEO versions are that
    *  perseus has forums within categories; leo just has forums
    """

    def getForums(self):
        # Building the SQL query
        if(DBName == "perseus"):
            qry =  "SELECT forumId, forumName, forumDescription, catName "
            qry += "FROM taggy_forums,taggy_categories "
            qry += "WHERE taggy_forums.categoryId = taggy_categories.categoryId "
            qry += "ORDER BY forumId"
        else:
            qry =  "SELECT forumId, forumName, forumDescription "
            qry += "FROM taggy_forums "
            qry += "ORDER BY forumId"

        # execution of the query 'qry'
        with connection.cursor() as cursor:
            cursor.execute(qry)
            # fetching all data of the query 'qry'
            qryResult = cursor.fetchall()

        # return the data
        return qryResult


    """
   * getForum()
   *
   * returns data for one specified forum
   *
   * @param integer $forumID  forum id number
    """

    def getForum(self, forumid):
        # Building the SQL query
        qry =  "SELECT forumName,formDescription,categoryId "
        qry += "FROM taggy_formus "
        qry += "WHERE forumId="+forumid

        # execution of the query 'qry'
        with connection.cursor() as cursor:
            cursor.execute(qry)
            # fetching all data of the query 'qry'
            qryResult = cursor.fetchall()

        # return the data
        return qryResult