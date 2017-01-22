from django.db.models import Q as Q
from taggy.models import Annotators as Annotators
from taggy.models import Posts as Posts
from taggy.models import Posts_annotators as Posts_annotators
from django.db import connection

class Queries:



    #THIS FUNCTION IS FOR CODE OPTIMIZATION AS IS USED TO RETRIEVE DATA FROM A QUERY
    #ALL FUNCTIONS BELOW THIS FUNCTION, WILL USE getData()
    #Instead of repeating the code inside getData(), better just call the function.
    def getData(self, qry):
        # execution of the query 'qry'
        with connection.cursor() as cursor:
            cursor.execute(qry)
            # fetching all data of the query 'qry'
            qryResult = cursor.fetchall()
        return qryResult


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
        qryResult = self.getData(qry)

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
        qryResult = self.getData(qry)

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
        qryResult = self.getData(qry)

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
        qryResult = self.getData(qry)

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
        qryResult = self.getData(qry)

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
        qryResult = self.getData(qry)

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
        qryResult = self.getData(qry)

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
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    #----- FUNCTIONS THAT HANDLE TOPICS -----------------------------------------


    """
    * getTopics()
    *
    * returns all data from topics within the specified forum
    *
    * NOTE: only used by PERSEUS (not used by LEO)
    *
    * @param integer $forumID  forum id number
    """

    def getTopic(self, forumid):

        # Building the SQL query
        qry = "SELECT topicId,url,title,DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
        qry += "profileId,DATE_FORMAT(lastDate,'%e-%b-%Y') AS last,numViews "
        qry += "FROM taggy_topics "
        qry += "WHERE forumId="+forumid+" "
        qry += "ORDER BY lastDate DESC"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult



    """
    * getTopicCreator()
    *
    * returns the name of the creator of the specified topic
    *
    * NOTE: only used by PERSEUS (not used by LEO)
    *
    * @param integer $topicID  topic id number
    """


    def getTopicCreator(self, topicid):

        # Building the SQL query
        qry =  "SELECT userName "
        qry += "FROM taggy_topics, taggy_profiles "
        qry += "WHERE topicID="+topicid+" "
        qry += "AND taggy_topics.profileId = taggy_profiles.profileId "
        qry += "ORDER BY topicID"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


  #----- FUNCTIONS THAT HANDLE POSTS ------------------------------------------

    """
    * getPosts()
    *
    * returns data from posts within the specified topic within the specified forum
    *
    * NOTE: difference between PERSEUS and LEO versions is that PERSEUS has topics and profiles,
    * and LEO does not
    *
    * @param integer $forumID  forum id number
    * @param integer $topicID  topic id number (only used by PERSEUS; not used by LEO)
    """

    def getPosts(self, forumid, topicid='', postState=''):

        # Building the SQL query
        if(DBName = "perseus"):
            qry =  "SELECT postId,DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "profileId,postState,content "
            qry += "FROM taggy_posts "
            qry += "WHERE forumId="+forumid+" AND topicId="+topicid+" "

            if(postState):
                qry += "AND postState='"+postState+"'"
            qry += "ORDER BY creationDate"
        else:
            qry =  "SELECT postID,DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "postState,content "
            qry += "FROM taggy_posts "
            qry += "WHERE forumId="+forumid+" "

            if(postState):
                qry += "AND postState='"+postState+"'"
            qry += "ORDER BY creationDate"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    """
    * getPost()
    *
    * returns data for specified post---but only if:
    * postState='PARSED' (posts that are ready to be annotated), or
    * postState='ANNOTATED' (posts that are ready to be adjudicated), or
    * postState='ADJUDICATED' (posts that have been annotated and adjudicated)
    *
    * NOTE: difference between PERSEUS and LEO versions is that PERSEUS has topics and profiles,
    * and LEO does not
    *
    * @param integer $postID  post id number
    """
    def getPost(self, postid):

        # Building the SQL query
        if (DBName = "perseus"):
            qry =  "SELECT postId,forumId,topicId,"
            qry += "DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "profileId,postState,content "
            qry += "FROM taggy_posts "
            qry += "WHERE postID="+postid+" "
            qry += "AND (postState='PARSED' OR "
            qry +=      "postState='ANNOTATED' OR "
            qry +=      "postState='ADJUDICATED')"
        else:
            qry =  "SELECT postId,forumId,"
            qry += "DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "postState,content "
            qry += "FROM taggy_posts "
            qry += "WHERE postId="+postid+" "
            qry += "AND (postState='PARSED' OR "
            qry +=      "postState='ANNOTATED' OR "
            qry +=      "postState='ADJUDICATED')"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    """
    * getPostState()
    *
    * returns the post state as a string
    *
    * @param integer $postID  post id number
    """

    def getPostState(self, postid):

        # Building the SQL query
        qry =  "SELECT postState "
        qry += "FROM taggy_posts "
        qry += "WHERE postID="+postid+" "

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult