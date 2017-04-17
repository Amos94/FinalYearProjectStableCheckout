import random

#import MySQLdb
#import MySQLdb
import MySQLdb
from django.db.models import Q as Q

from django.db import connection
from FYP import settings

class Queries:

    DBName = ''
    domainId = 0
    #"perseus"
    def __init__(self):
        try:
            qry = "SELECT name taggy_domains WHERE id = "+str(self.domainId)
            results = self.getData(qry)
            for result in results:
                self.DBName = result[0]
        except:
            self.DBName = "perseus"

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

    #gets just one
    def getOne(self,qry):
        # execution of the query 'qry'

        with connection.cursor() as cursor:
            cursor.execute(qry)
            # fetching all data of the query 'qry'
            qryResult = cursor.fetchone()
        return qryResult

    def insertOrUpdate(self, qry):
        # execution of the query 'qry'
        with connection.cursor() as cursor:
            res = cursor.execute(qry)
            # fetching all data of the query 'qry'

            return res


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
        qry = 'SELECT annotatorId,username,password,usertype '
        qry += 'FROM taggy_annotators '

        if (username != ''):
            qry += "WHERE username='"+username+"'"
        elif (userid != None):
            qry += "WHERE annotatorId='"+str(userid)+"'"


        qryResult = self.getData(qry)
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
        qry =  "SELECT taggy_posts_annotators.annotatorId, taggy_annotators.username "
        qry += "FROM taggy_posts_annotators, TAGGY_annotators "
        qry += "WHERE postId='"+str(postid)+"' "
        qry += "AND taggy_annotators.usertype='annotator' "
        qry += "AND taggy_posts_annotators.annotatorId = taggy_annotators.annotatorId "
        qry += "ORDER BY taggy_posts_annotators.annotatorId"

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
        qry += "WHERE setId='"+str(setid)+"' "
        qry += "AND taggy_annotators.usertype='annotator' "
        qry += "AND taggy_annotators_sets.annotatorId = taggy_annotators.annotatorId "
        qry += "ORDER BY taggy_annotators_sets.annotatorId"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult



    """
    * getAnnotatorsForSet()
    *
    * returns the Annotator IDs for a particular Set ID
    *
    * @param integer $setid  set ID
    """
    def getUsersForSet(self, setid):

        # Building the SQL query
        qry =  "SELECT taggy_annotators_sets.annotatorId, taggy_annotators.username "
        qry += "FROM taggy_annotators_sets, taggy_annotators "
        qry += "WHERE setId='"+str(setid)+"' "
        qry += "AND taggy_annotators_sets.annotatorId = taggy_annotators.annotatorId "

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
        qry += "WHERE postId='"+str(postId)+"' "

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
        qry =  "SELECT username, postAnnotatorState "
        qry += "FROM taggy_annotators, taggy_posts_annotators "
        qry += "WHERE postId='"+str(postid)+"' "
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

    def insertAnnotator(self,  username, password, usertype='annotator'):
        # Building the SQL query
        qry =  "INSERT INTO  taggy_annotators (username, password, usertype) "
        qry += "VALUES ('"+str(username)+"','"+str(password)+"','"+str(usertype)+"')"


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
            updates.append("password= '"+str(password)+"' ")

        if(usertype):
            updates.append("usertype= '"+str(usertype)+"' ")

        qry =  "UPDATE taggy_annotators SET"
        qry += ",".join(updates)
        qry += "WHERE (username='"+str(username)+"')"


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
        if(self.DBName == "perseus"):
            qry =  "SELECT forumId, forumName, forumDescription, catName, taggy_forums.domainId, taggy_categories.domainId "
            qry += "FROM taggy_forums, taggy_categories "
            qry += "WHERE taggy_forums.categoryId = taggy_categories.categoryId "
            qry += "ORDER BY forumId"
        else:
            qry =  "SELECT forumId, forumName, forumDescription, domainId "
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
        qry =  "SELECT forumName,formDescription,categoryId, domainId "
        qry += "FROM taggy_forums "
        qry += "WHERE forumId="+str(forumid)

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
        qry += "profileId,DATE_FORMAT(lastDate,'%e-%b-%Y') AS last,numViews, forumId, domainId "
        qry += "FROM taggy_topics "
        qry += "WHERE forumId="+str(forumid)+" "
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
        qry += "WHERE topicId="+str(topicid)+" "
        qry += "AND taggy_topics.profileId = taggy_profiles.profileId "
        qry += "ORDER BY topicId"

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
        if(self.DBName == "perseus"):
            qry =  "SELECT postId,DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "profileId,postState,content, domainId "
            qry += "FROM taggy_posts "
            qry += "WHERE forumId="+str(forumid)+" AND topicId="+str(topicid)+" "

            if(postState):
                qry += "AND postState='"+postState+"'"
            qry += "ORDER BY creationDate"
        else:
            qry =  "SELECT postId,DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "postState,content, domainId "
            qry += "FROM taggy_posts "
            qry += "WHERE forumId="+str(forumid)+" "

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
        if (self.DBName == "perseus"):
            qry =  "SELECT postId,forumId,topicId,"
            qry += "DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "profileId,postState,content, domainId "
            qry += "FROM taggy_posts "
            qry += "WHERE postId="+str(postid)+" "
            qry += "AND (postState='PARSED' OR "
            qry +=      "postState='ANNOTATED' OR "
            qry +=      "postState='ADJUDICATED')"
        else:
            qry =  "SELECT postId,forumId,"
            qry += "DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "postState,content, domainId "
            qry += "FROM taggy_posts "
            qry += "WHERE postId="+str(postid)+" "
            qry += "AND (postState='PARSED' OR "
            qry +=      "postState='ANNOTATED' OR "
            qry +=      "postState='ADJUDICATED')"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult

    def getPostContent(self, postid):
        # Building the SQL query
        qry = "SELECT content "
        qry += "FROM taggy_posts "
        qry += "WHERE postId= " + str(postid)+" "


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
        qry += "WHERE postId="+str(postid)+" "

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult

    """
    * getPostParseInfo()
    *
    * returns data for specified post that relates to the parse history
    *
    * @param integer $postID  post id number
    """

    def getPostParseInfo(self, postid):

        # Building the SQL query
        qry =  "SELECT postState,DATE_FORMAT(dateReviewed,'%e-%b-%Y') AS reviewed,"
        qry += "DATE_FORMAT(dateParsed,'%e-%b-%Y') AS parsed,"
        qry += "parseHistory,parseVersion,parseTool "
        qry += "FROM taggy_posts "
        qry += "WHERE postId="+str(postid)


        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult

    """
    * getPostAtRandom()
    *
    * returns all data for a randomly selected post (takes a while to run because posts table is big)
    * NOTE: ONLY RETURNS POSTS WHERE postState='PARSED' (posts that are ready to be annotated)
    *
    * NOTE: difference between PERSEUS and LEO versions is that PERSEUS has topics and profiles,
    * and LEO does not
    """

    def getPostAtRandom(self):

        # Building the SQL query
        qry = "SELECT COUNT(*) as num FROM taggy_posts"

        # creating a random number between 0 and num
        number = self.getData(qry)[0]
        for i in number:
            a=i
        rnd = random.uniform(0, a-1)
        randomNumber = int(rnd)

        # execution of the query 'qry'
        qry = "" #just want to make sure qry is empty, even though, in if-else statement, qry will get another value
        if(self.DBName == "perseus"):
            qry =  "SELECT postId,forumId,topicId,"
            qry += "DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "profileId,postState,content, domainId "
            qry += "FROM taggy_posts "
            qry += "WHERE postState='PARSED' "
            qry += "LIMIT 1 OFFSET "+str(randomNumber)
        else:
            qry =  "SELECT postId,forumId,"
            qry += "DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "postState,content, domainId "
            qry += "FROM taggy_posts "
            qry += "WHERE postState='PARSED' "
            qry += "LIMIT 1 OFFSET "+str(randomNumber)

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult

    """
    * getPostCreator()
    *
    * returns all the name of the creator of the specified post
    *
    * NOTE: only used by PERSEUS (not used by LEO)
    *
    * @param integer $postID  post id number
    """

    def getPostCreator(self, postid):

        # Building the SQL query
        qry =  "SELECT userName "
        qry += "FROM taggy_posts, taggy_profiles "
        qry += "WHERE postId="+str(postid)+" "
        qry += "AND taggy_posts.profileId=taggy_profiles.profileId"


        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    """
    * getPostAnnotation()
    *
    * returns the post's comments, number of sentences tagged, percentDone (specific to
    * annotator)
    *
    * @param integer $postID  post id number
    * @param integer $annotatorID  annotator id number
    """

    def getPostAnnotation(self, postid, annotatorid):

        #get the annotators for the post or annotator
        # Building the SQL query
        qry =  "SELECT comment, numSentencesTagged, (numSentencesTagged/numSentencesInPost) as percentDone, postAnnotatorState "
        qry += "FROM taggy_posts_annotators "
        qry += "WHERE ((postId="+str(postid)+") AND (annotatorId="+str(annotatorid)+")) "

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        #Create if none exists

        if(not qryResult):
            insertQry =  "INSERT INTO taggy_posts_annotators (annotatorId, postId, numSentencesInPost, comment, numSentencesTagged, lastUpdated) "
            insertQry += "SELECT "+str(annotatorid)+" as annotatorId, "+str(postid)+" as postId, "
            insertQry += "count(sentenceId) as numSentencesInPost, " # count sentences in the post
            insertQry += "'' as comment, 0 as numSentencesTagged, NOW() as lastUpdated " # default values (move into Table Definition?)
            insertQry += "FROM taggy_sentences WHERE (postId="+str(postid)+") "

            insertStatus = self.getData(insertQry)

            if(insertStatus):
                qryResult = self.getData(qry)


        # return the data
        return qryResult


    """
    * updatePostAnnotation()
    *
    * updates the number of tagged sentences, and (optionally) the
    * postAnnotation's comments, and/or a new postAnnotationState
    *
    *
    * @param integer $postID  post id number
    * @param integer $annotatorID  annotator id number
    * @param string $unescaped_comment  post annotation's comment (optional)
    * @param string $state new post annotation state (optionall)
    """

    def updatePostAnnotation(self, postid, annotatorid, unescaped_comment = None, state = None):

        # Building the SQL query
        qry =  "UPDATE taggy_posts_annotators  "
        qry += "SET numSentencesTagged = ( "
        qry +=      "SELECT count(DISTINCT sentenceId) "
        qry +=      "FROM taggy_sentences_tags "
        qry +=      "WHERE (postId = "+str(postid)+") AND (annotatorId = "+str(annotatorid)+")) "

        if(unescaped_comment != None):
            escaped_comment = MySQLdb.escape_string(unescaped_comment)
            qry += ", comment = '"+escaped_comment+"' "

        if(state != None):
            state = MySQLdb.escape_string(state)
            qry += ", postAnnotatorState = '"+state+"' "
        qry += "WHERE ((postId="+postid+") AND (annotatorId="+annotatorid+")) "

        updateStatus = self.getData(qry)

        if(state != None and updateStatus):
            self.updatePostState(postid)

        return updateStatus


    """
    * updatePostState()
    *
    * updates the postState field in the posts table
    *
    * @param integer $postID  post id number
    * @param integer $postState  state to set post to *optional*, if left out
    *                            postState is based upon PostAnnotation states
    """

    def updatePostState(self, postid, postState = ''):
        updateStatus = []
        if(postState != ''):
            newPostState = postState  # initially no change
        else:
            #update post state
            #get old post state
            result = self.getData("SELECT postState FROM taggy_posts WHERE postId="+str(postid))
            for r in result:
                row = r
            oldPostState = row[0]

            #Check if PostState is able to be updated based on postAnnotatorStates
            if(oldPostState in ["PARSED", "ANNOTATED", "ADJUDICATED"]):
                # Get counts of postAnnotatorStates
                cntSQL =  "SELECT postAnnotatorState, count(*) AS n "
                cntSQL += "FROM taggy_posts_annotators "
                cntSQL += "WHERE (postId = '"+str(postid)+"')  "
                cntSQL += "GROUP BY postAnnotatorState"

                result = self.getData(cntSQL)

                numStates = []

                #Build a map of postAnnotatorState => n
                for row in result:
                    numStates[row[0]] = row[1]


                #check for a new PostState based on postAnnotatorStates
                if(('ADJUDICATED' in numStates) and (numStates['ADJUDICATED'] > 0)):
                    # Post is ADJUDICATED if any postAnnotatorStates are set to 'ADJUDICATED'
                    newPostState = 'ADJUDICATED'

                elif(('DONE' in numStates) and (numStates['DONE'] > 1)):
                    # post is ANNOTATED if any postAnnotatorStates are set to 'DONE'
                    newPostState = 'ANNOTATED'

                elif(('IN_PROGRESS' in numStates) and (numStates['IN_PROGRESS'] > 1)):
                    #post is PARSED if any postAnnotatorStates are set to 'IN_PROGRESS'
                    newPostState = 'PARSED'

                # otherwise, make no changes to postState
                # else postState is INITIAL', 'SELECTED', 'REPARSE'

        if(newPostState != ''):
            qry =  "UPDATE taggy_posts "
            qry += "SET postState='"+newPostState+"' "
            qry += "WHERE postId="+str(postid)

            updateStatus = self.getData(qry)


        return updateStatus

        #return True




    """
    * updateParseTool()
    *
    * updates the parseTool and postState fields in the posts table.
    *
    * NOTE that if the parseTool argument is empty (""), then parseTool
    * will be set to NULL and postState is set to 'REPARSE'.
    *
    * @param integer $postID    post id number
    * @param integer $parseTool value to set post to
    """

    def updateParseTool(self, postid, parsetool, poststate):

        # Building the SQL query
        qry =  "UPDATE taggy_posts "
        qry += "SET postState='"+poststate+"', "


        if(parsetool == ""):
            qry += " parseTool=NULL, "

        else:
            qry += " parseTool='"+parsetool+"', "

        qry += " dateReviewed=now() "
        qry += "WHERE postId="+str(postid)


        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult



#----- FUNCTIONS THAT HANDLE TAGS -------------------------------------------

    """
    * getTags()
    *
    * returns data from tags table
    *
    * NOTE: the differences between PERSEUS and LEO versions are that
    * perseus has provideOrRequest column; leo does not
    *
    * @param char $option  fetch option: 'P' for provide, 'R' for request, '' for all
    * (only used by perseus)
    *
    """
    def getTags(self, option):

        # Building the SQL query
        if(self.DBName == "perseus" ):
            qry =  "SELECT tagId,tagName,tagDescription,provideOrRequest, domainId "
            qry += "FROM taggy_tags "

            if(option != ''):
                qry += "WHERE provideOrRequest='"+option+"' "

            qry += "ORDER BY tagName,provideOrRequest"

        else:
            qry =  "SELECT tagId,tagName,tagDescription, domainId "
            qry += "FROM taggy_tags "
            qry += "ORDER BY tagName"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    """
    * getTagNamesAnd2ids()
    *
    * returns list of tag names and 2 ID numbers corresponding to each tag, from the tags table
    *
    * NOTE: for PERSEUS, there are two entries in the database table
    * for each named tag (i.e., provides or requests), so in that case,
    * this function will return 2 different IDs in each row.
    * For LEO, this function will return the same ID twice in each row.
    """
    def getTagNamesAnd2ids(self):
        qry =  "SELECT tagName, MIN(tagId) AS tagId1, MAX(tagId) AS tagId2 "
        qry += "FROM taggy_tags "
        qry += "GROUP BY tagName "
        qry += "ORDER BY tagName"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult

    """
    * getTagIDs()
    *
    * returns tagIDs from tags table
    *
    * NOTE: for PERSEUS, there are two entries in the database table
    * for each named tag (i.e., provides or requests), so in that case,
    * this function will return multiple (2) rows.
    *
    """
    def getTagIds(self, tagName):

        # Building the SQL query
        qry = "SELECT tagId FROM taggy_tags where tagName='"+tagName+"'"


        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult

#----- FUNCTIONS THAT HANDLE SENTENCES --------------------------------------

    """
    * getSentences()
    *
    * returns all sentences data for specified postID
    *
    * @param integer $postID  post id number
    """
    def getSentences(self, postid):

        #Building the SQL query 'qry'
        qry =  "SELECT postId,sentenceId,sentence,paragraphInPost,sentenceInParagraph, domainId "
        qry += "FROM taggy_sentences "
        qry += "WHERE postId="+str(postid)+" "
        qry += "ORDER BY paragraphInPost,sentenceInParagraph"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    """
    * getSentencesInSet()
    *
    * returns all sentences data for specified setID
    *
    * @param integer $setID  set id number
    """
    def getSentencesInSet(self, setid):

        # Building the SQL query 'qry'
        qry =  "SELECT sentences.postId,sentenceId,sentence,paragraphInPost,sentenceInParagraph, domainId "
        qry += "FROM taggy_sentences,taggy_posts_sets "
        qry += "WHERE setId="+str(setid)+" "
        qry += "AND posts_sets.postId=sentences.postId "
        qry += "ORDER BY postId,sentenceId,paragraphInPost,sentenceInParagraph"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult

    """
    * getSentencesInSet()
    *
    * returns all sentences data for specified setID
    *
    * @param integer $setID  set id number
    """
    def addPostInSet(self, setid, postid):

        # Building the SQL query 'qry'
        qry =  "INSERT INTO taggy_posts_sets (setId, postId) VALUES( '"+str(setid)+"', '"+str(postid)+"' )"

        # execution of the query 'qry'
        qryResult = self.insertOrUpdate(qry)

        # return the data
        return qryResult
#----- FUNCTIONS THAT HANDLE SENTENCE_TAGS ----------------------------------

    """
    * getSentenceTags()
    *
    * gets row(s) of sentences_tags for a sentence, and particular annotator
    *
    * @param integer $postID       post id
    * @param integer $sentenceID   sentence id
    * @param integer $annotatorID  annotator id
    """
    def getSentenceTags(self, postid, sentenceid, annotatorid):

        #Building the SQL query 'qry'
        qry =  "SELECT * FROM taggy_sentences_tags "
        qry += "WHERE sentenceId = "+str(sentenceid)
        qry += " AND postId = "+str(postid)
        qry += " AND annotatorId = "+str(annotatorid)

        #execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult

    """
    * getTag()
    *
    * gets row(s) of sentences_tags for a sentence, and particular annotator
    *
    * @param integer $postID       post id
    * @param integer $sentenceID   sentence id
    * @param integer $annotatorID  annotator id
    """
    def getTag(self, tagId):
        qry =  "SELECT * FROM taggy_tags "
        qry += "WHERE tagId = "+str(tagId)

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult
    """
    * getTag()
    *
    * gets row(s) of sentences_tags for a sentence, and particular annotator
    *
    * @param integer $postID       post id
    * @param integer $sentenceID   sentence id
    * @param integer $annotatorID  annotator id
    """
    def getTagAndPOR(self):
        qry =  "SELECT tagId, tagName, provideOrRequest, domainId FROM taggy_tags "

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult
    """
    * getSentenceTagCount()
    *
    * counts row(s) of sentences_tags for a sentence and particular annotator
    *
    * @param integer $sentenceID   sentence id
    * @param integer $annotatorID  annotator id
    * @param integer $tagIDstring  string of tagIDs
    """
    def getSentenceTagCount(self, sentenceid, annotatorid, tagidstring):

        #Building the SQL query qry
        qry =  "SELECT COUNT(*) AS num FROM taggy_sentences_tags "
        qry += "WHERE sentenceId = "+str(sentenceid)
        qry += " AND annotatorId = "+str(annotatorid)
        qry += " AND tagId IN "+str(tagidstring)

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        row = self.getOne(qryResult)
        num = row['num']
        return num


    """
    * getTagMatchesByPost()
    *
    * gets row(s) of annotators and sentences within a particular post, where the annotators
    *  in the argument group of annotatorIDs entered the tags in the argument group of tagIDs
    *
    * @param integer $postID        post id
    * @param integer $tagIDs        array of tag ids
    * @param integer $annotatorIDs  array of annotator ids
    """
    def getTagMatchesByPost(self, postid, tagids, annotatorids):

        #Building the SQL query 'qry'
        qry =  "SELECT DISTINCT annotatorId, sentenceId "
        qry += "FROM taggy_sentences_tags "
        qry += "WHERE (postId = "+str(postid)+") "

        qry += " AND (annotatorId IN ("
        for a in annotatorids:
            qry += a + ","

        qry = qry.rstrip(',')

        qry += ")) AND (tagID IN ("
        for t in tagids:
            qry += t + ","

        qry = qry.rstrip(',')
        qry += ")) ORDER BY sentenceId, annotatorId"

        #execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    """
    * insertSentenceTag()
    *
    * inserts a row in the sentences_tags table
    *
    * @param integer $sentenceID   sentence id number to insert
    * @param integer $tagID        tag id number to insert
    * @param integer $postID       post id number to insert
    * @param integer $annotatorID  annotator id number to insert
    """
    def insertSentenceTag(self, sentenceid, tagid, postid, annotatorid):

        # Building the SQL query 'qry'
        qry =  "INSERT INTO taggy_sentences_tags (sentenceId,tagId,postId,annotatorId,timestamp) "
        qry += "VALUES ("+str(sentenceid)+","+str(tagid)+","+str(postid)+","+str(annotatorid)+",NOW())"

        # execution of the query 'qry'
        status = self.getData(qry)

        #return status
        return status


    """
    * deleteSentenceTag()
    *
    * deletes a row in the sentences_tags table
    *
    * @param integer $sentenceID   sentence id number to insert
    * @param integer $tagID        tag id number to insert
    * @param integer $postID       post id number to insert
    * @param integer $annotatorID  annotator id number to insert
    """
    def deleteSentenceTag(self,sentenceid, tagid, postid, annotatorid):

        # Building the SQL query 'qry'
        qry =  "DELETE FROM taggy_sentences_tags "
        qry += "WHERE ((sentenceId = "+str(sentenceid)+") "
        qry += "AND (tagId = "+str(tagid)+") "
        qry += "AND (postId = "+str(postid)+") "
        qry += "AND (annotatorId = "+str(annotatorid)+"))"

        # execution of the query 'qry'
        status = self.getData(qry)

        #return status
        return status


#----- FUNCTIONS THAT HANDLE SETS -----

    """
    * getSets()
    *
    * returns data from sets table
    *
    """
    def getSets(self):

        #Building the SQL query 'qry'
        qry =  "SELECT setId,name,description,username AS creator, domainId  "
        qry += "FROM taggy_sets, taggy_annotators "
        qry += "WHERE taggy_annotators.annotatorId = taggy_sets.creatordId "
        qry += "ORDER BY setId"

        #execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    """
    * getSetsByCreator()
    *
    * returns data from sets table created by person specified in argument
    *
    """
    def getSetsByCreator(self, creatorid):

        #Building the SQL query 'qry'
        qry =  "SELECT setId,name,description,username AS creator, domainId "
        qry += "FROM taggy_sets, taggy_annotators "
        qry += "WHERE creatorId="+str(creatorid)+" "
        qry += "AND taggy_annotators.annotatorId=taggy_sets.creatorId "
        qry += "ORDER BY setId"

        #execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    """
    * getSetsByAnnotatorID()
    *
    * gets collection of Sets by annotatorID
    *
    * @param string $annotatorID
    * @return array resultSet of Sets
    """
    def getSetsByAnnotatorId(self, annotatorid):

        # Building the SQL query 'qry'
        qry = "SELECT taggy_sets.setId, taggy_sets.name, taggy_sets.description, taggy_sets.domainId "
        qry += "FROM taggy_sets JOIN taggy_annotators_sets "
        qry += "WHERE (annotatorId = '"+str(annotatorid)+"') "
        qry += "AND (taggy_sets.setId = taggy_annotators_sets.setId) "
        qry += "ORDER BY taggy_sets.setId"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    """
    * getSet()
    *
    * returns all data for specified set
    *
    *   @param integer $setID  set id number
    """
    def getSet(self, setid):

        #Building the SQL query 'qry'
        qry =  "SELECT postId "
        qry += "FROM taggy_posts_sets "
        qry += "WHERE setId = "+str(setid)+" "
        qry += "ORDER BY postId"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    """
    * getSetMeta()
    *
    * returns meta-data about a set from sets table
    *
    * @param integer $setID  set id number
    """
    def getSetMeta(self, setid):

        # Building the SQL query 'qry'
        qry = "SELECT setId, name, description, domainId "
        qry += "FROM taggy_sets "
        qry += "WHERE setId="+str(setid)+" "

        # execution of the query 'qry'
        qryResult = self.getOne(qry)

        # return the data
        return qryResult


    """
    * getPostsInSet()
    *
    * returns data from posts within the specified set
    *
    * NOTE: difference between PERSEUS and LEO versions is that PERSEUS has topics and profiles,
    * and LEO does not
    *
    * @param integer $setID  set id number
    """
    def getPostsInSet(self, setid, postState=''):

        #Building the SQL query 'qry'
        if(self.DBName == "perseus"):
            qry =  "SELECT taggy_posts.postId, forumId, topicId,DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "profileId, postState, content "
            qry += "FROM taggy_posts, taggy_posts_sets "
            qry += "WHERE taggy_posts_sets.setId="+str(setid)+" "
            qry += "AND taggy_posts_sets.postId = taggy_posts.postId "
            if(postState):
                qry += " AND postState='"+str(postState)+"' "
            qry += "ORDER BY taggy_posts.postId ASC"
        else:
            qry = "SELECT taggy_posts.postId, forumId, DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "postState,content "
            qry += "FROM taggy_posts, taggy_posts_sets "
            qry += "WHERE taggy_posts_sets.setId="+str(setid)
            qry += " AND taggy_posts_sets.postId = taggy_posts.postId "
            if(postState):
                qry += " AND postState='"+str(postState)+"' "
            qry += "ORDER BY taggy_posts.postId ASC"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    """
    * getProgressInSet()
    *
    * returns number of posts annotated grouped by annotators
    *
    * @param integer $setID  set id number
    """
    def getProgressInSet(self, setid):

        # Building the SQL query 'qry'
        qry =  "SELECT taggy_annotators.username, taggy_annotators.annotatorId, "
        qry += "COUNT(distinct taggy_sentences_tags.postId) as numPosts "
        qry += "FROM taggy_sentences_tags JOIN(taggy_posts_sets,annotators) "
        qry += "WHERE ( (taggy_sentences_tags.postId = taggy_posts_sets.postId) "
        qry += "    AND (taggy_posts_sets.setId = " +str(setid)+ ") "
        qry += "    AND (taggy_annotators.annotatorId = taggy_sentences_tags.annotatorId) ) "
        qry += "GROUP BY annotatorId"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult

    def getAnnotatorName(self, annotatorid):
        qry = "SELECT username FROM taggy_annotators WHERE annotatorId='"+str(annotatorid)+"'"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult

    """
    * getAnnotatorsProgressInSet()
    *
    * returns number of posts annotated grouped by annotators
    *
    * @param string $annotatorID
    * @param integer $setID set id number
    """
    def getAnnotatorsProgressInSet(self, annotatorid, setid):

        # Building the SQL query 'qry'
        qry =  "SELECT taggy_annotators.username, taggy_annotators.annotatorId, "
        qry += "COUNT(distinct taggy_sentences_tags.postId) as numPosts "
        qry += "FROM taggy_sentences_tags JOIN(taggy_posts_sets,taggy_annotators) "
        qry += "WHERE ( (taggy_sentences_tags.postId = taggy_posts_sets.postId) "
        qry += "    AND (taggy_posts_sets.setId = " + str(setid) + ") "
        qry += "    AND (taggy_sentences_tags.annotatorId = " + str(annotatorid) + ") "
        qry += "    AND (taggy_annotators.annotatorId = taggy_sentences_tags.annotatorId) ) "
        qry += "GROUP BY annotatorId"


        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    """
    * insertSet()
    *
    * @param string $setname name of set
    """
    def insertSet(self, setname, setdescription, creatorid, domainId):

        # Building the SQL query 'qry'
        qry =  "INSERT INTO taggy_sets (name, description, creatordId, domainId) "
        qry += "VALUES ('"+setname+"','"+setdescription+"','"+str(creatorid)+"','"+str(domainId)+"')"

        # execution of the query 'qry'
        res = self.insertOrUpdate(qry)
        return res



    """
    * updateSet()
    *
    * NOTE: the differences between PERSEUS and LEO versions are:
    *  in PERSEUS, posts.postState=='INIITAL' is changed to 'SELECTED' when added to set
    *  in LEO, posts.postState=='PARSED' and is not changed when added to set
    *
    * BUT!! need to make sure that a post (in LEO) is not added to more than one set
    *
    """
    def updateSet(self, setid, setposts):

        # Building the SQL query 'qry'
        if(self.DBName == "perseus" ):
            qry =  "UPDATE taggy_posts, taggy_posts_sets "
            qry += "SET postState='INITIAL' "
            qry += "WHERE taggy_posts_sets.setId="+str(setid)
            qry += " AND taggy_posts_sets.postId = taggy_posts.postId"

            # execution of the query 'qry'
            status = self.getData(qry)

        qry = "DELETE FROM taggy_posts_sets WHERE setId=" + str(setid)
        # execution of the query 'qry'
        status = self.getData(qry)

        tok = setposts.split(" \n\t")

        while(tok != False):
            status = False
            qry = "SELECT COUNT(*) as count FROM taggy_posts WHERE postId="+tok+" AND (postState='INITIAL' OR postState='PARSED')"

            result = self.getData(qry)
            if(result):
                row = self.getData(result)
                if(row['count'] > 0):
                    qry = "SELECT COUNT(*) as count FROM taggy_posts_sets WHERE postId="+tok
                    result = self.getData(qry)

                    if(result):
                        row = self.getData(result)
                        if(row['count'] == 0 ):
                            qry =  "INSERT INTO taggy_posts_sets (setId,postId) "
                            qry += "VALUES ("+str(setid)+","+tok+")"

                            status = self.getData(qry)

                            if(status):
                                if(self.DBName == "perseus" ):
                                    qry = "UPDATE taggy_posts SET postState='SELECTED' WHERE postId="+tok
                                    status = self.getData(qry)

            if(status):
                print("post verified and inserted: ["+tok+"]<br />")
            else:
                print("post NOT verified and NOT inserted: [" + tok + "]<br />")

            tok = self.split(" \n\t")



    """
    * deleteSet()
    *
    * the only "fatal" error is if there  is nothing to delete from the 'sets' table.
    * because it is possible to have a set without any posts or annotations.
    * so we can fail in trying to delete from 'posts_sets' and 'annotators_sets' tables,
    * but not need to generate an error.
    *
    * @param string $setid ID number of set to delete
    *
    """
    def deleteSet(self, setid):

        qry = "DELETE FROM taggy_annotators_sets WHERE setId='"+ str(setid) +"' "
        self.insertOrUpdate(qry)

        qry = "DELETE FROM taggy_posts_sets WHERE setId='" + str(setid) + "' "
        self.insertOrUpdate(qry)

        qry = "DELETE FROM taggy_sets WHERE setId='" + str(setid) + "' "
        status = self.insertOrUpdate(qry)

        return status



#----- FUNCTIONS THAT HANDLE ANNOTATORS_SETS --------------------------------

    """
    * getAnnotatorsSets()
    *
    * returns data from annotators_sets table
    *
    * @param integer $setID  set id number
    """
    def getAnnotatorsSets(self,setid=''):

        #Building the SQL query qry
        qry =  "SELECT annotatorId, setId "
        qry += "FROM taggy_annotators_sets "

        if(setid):
            qry += "WHERE setId='"+str(setid)+"' "

        qry += "ORDER BY  setId, annotatorId"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        # return the data
        return qryResult


    """
    * insertAnnotatorsSets()
    *
    * inserts a new annotator-set relation into annotators_sets
    *
    * @param integer $annotatorID  annotator id number
    * @param integer $setID  set id number
    """

    def insertAnnotatorsSets(self, annotatorid, setid):

        #Building the SQL query qry
        qry =  "INSERT INTO  taggy_annotators_sets (annotatorId, setId) "
        qry += "VALUES ('"+str(annotatorid)+"','"+str(setid)+"')"

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status


    """
    * deleteAnnotatorsSets()
    *
    * deletes all annotator-set relations
    *
    * @param integer $annotatorID  annotator id number
    * @param integer $setID  set id number
    """
    def deleteAnnotatorsSets(self, annotatorid, setid):

        #Building the SQL query qry
        qry =  "DELETE FROM taggy_annotators_sets "
        qry += "WHERE (annotatorId='"+str(annotatorid)+"' AND setId='"+str(setid)+"')"

        # execution of the query 'qry'
        status = self.getData(qry)

        # return the data
        return status


    """
    * checkSetAnnotatorAssignment()
    *
    * checks that set is assigned to annotator
    *
    * @param string $setID
    * @param string $annotatorID
    * @return true or false
    """
    def checkSetAnnotatorAssignment(self, setid, annotatorid):

        # Building the SQL query qry
        qry =  "SELECT* "
        qry += "FROM taggy_annotators_sets "
        qry += "WHERE setId = "+str(setid)
        qry += " AND annotatorId = "+str(annotatorid)

        results = self.getData(qry)
        if(results == None):
            toReturn = False
        else:
            toReturn = True

        return toReturn


    """
    get sentences by sentence id
    """
    def getSentence(self, sentenceId):
        qry = "SELECT * FROM taggy_sentences WHERE sentenceId="+str(sentenceId)+""
        results = self.getData(qry)
        return results




    """
    QUERIES FOR CORPUS/ DOMAIN
    """

    """
    GET ALL DOMAINS
    """
    def getDomainsMeta(self):
        # Building the SQL query qry
        qry = "SELECT * FROM taggy_domains"

        # execution of the query 'qry'
        results = self.getData(qry)

        # return the data
        return results


    """
    GET ALL ANNOTATORS OF A SPECIFIC DOMAIN
    """
    def getAnnotatorsDomains(self, domainId):
        # Building the SQL query qry
        qry = "SELECT * FROM taggy_annotators_domains WHERE domainId = "+str(domainId)

        # execution of the query 'qry'
        results = self.getData(qry)

        # return the data
        return results


    """
    GET A SPECIFIC DOMAIN BY NAME
    """
    def getDomainByName(self, domainName):
        # Building the SQL query qry
        qry = "SELECT * FROM taggy_domains WHERE name='"+domainName+"'"

        # execution of the query 'qry'
        results = self.getData(qry)

        # return the data
        return results

    """
    GET A SPECIFIC DOMAIN BY ID
    """
    def getDomainById(self, domainId):
        # Building the SQL query qry
        qry = "SELECT * FROM taggy_domains WHERE id="+str(domainId)

        # execution of the query 'qry'
        results = self.getData(qry)

        # return the data
        return results


    """
        INSERT NEW DOMAIN
    """
    def insertDomain(self,domainName):
        # Building the SQL query qry
        qry = "INSERT INTO taggy_domains(name) VALUES('"+str(domainName)+"')"

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    EDIT DOMAIN
    """
    def editDomainName(self, domainId, domainName):
        # Building the SQL query qry
        qry = "UPDATE taggy_domains SET name = '"+domainName+"' WHERE id = "+str(domainId)

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    Assign annotator to a domain
    """
    def assignAnnotatorToDomain(self, annotatorId, domainId, isActive=True):
        # Building the SQL query qry
        qry = "INSERT INTO taggy_annotators_domains(annotatorId, domainId, isActive) VALUES(" + str(annotatorId) +","+ str(domainId) + ","+ str(isActive) +")"

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    Change the state of an annotator already assigned to a domain to ACTIVE (isActive = 1)
    """
    def activateAnnotatorForDomain(self, annotatorId, domainId):
        # Building the SQL query qry
        qry = "UPDATE taggy_annotators_domains SET isActive = " + str(True) + " WHERE annotatorId = " + str(annotatorId) +", AND domainId = " + str(domainId)

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status


    """
    Change the state of an annotator already assigned to a domain to INACTIVE (isActive = 0)
    """
    def deactivateAnnotatorForDomain(self, annotatorId, domainId):
        # Building the SQL query qry
        qry = "UPDATE taggy_annotators_domains SET isActive = " + str(False) + " WHERE annotatorId = " + str(annotatorId) +", AND domainId = " + str(domainId)

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status


    """
    Update domain column of a Category
    """
    def updateCategoriesDomain(self, categoryId, domainId):
        # Building the SQL query qry
        qry = "UPDATE taggy_categories SET domainId = " + str(domainId) + " WHERE categoryId = " + str(categoryId)

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    Update domain column of a Forum
    """
    def updateForumsDomain(self, forumId, domainId):
        # Building the SQL query qry
        qry = "UPDATE taggy_forums SET domainId = " + str(domainId) + " WHERE forumId = " + str(forumId)

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    Update domain column of a Post
    """
    def updatePostsDomain(self, postId, domainId):
        # Building the SQL query qry
        qry = "UPDATE taggy_posts SET domainId = " + str(domainId) + " WHERE postId = " + str(postId)

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status


    """
    Update domain column of a Sentence
    """
    def updateSentencesDomain(self, sentenceId, domainId):
        # Building the SQL query qry
        qry = "UPDATE taggy_sentences SET domainId = " + str(domainId) + " WHERE sentenceId = " + str(sentenceId)

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    Update domain column of a Set
    """
    def updateSetsDomain(self, setId, domainId):
        # Building the SQL query qry
        qry = "UPDATE taggy_sets SET domainId = " + str(domainId) + " WHERE setId = " + str(setId)

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    Update domain column of a TAG
    """
    def updateTagsDomain(self, tagId, domainId):
        # Building the SQL query qry
        qry = "UPDATE taggy_tags SET domainId = " + str(domainId) + " WHERE tagId = " + str(tagId)

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    Update domain column of a Topic
    """
    def updateTopicsDomain(self, topicId, domainId):
        # Building the SQL query qry
        qry = "UPDATE taggy_topics SET domainId = " + str(domainId) + " WHERE topicId = " + str(topicId)

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    QUERIES FOR KEYWORDS AND PREDICTION
    """

    """
    GET ALL KEYWORDS
    """
    def getKeywordsMeta(self):
        # Building the SQL query qry
        qry = "SELECT * FROM taggy_keywords"

        # execution of the query 'qry'
        results = self.getData(qry)

        # return the data
        return results


    """
    GET KEYWORDS BY DOMAIN
    """
    def getKeywordsByDomain(self, domainId):
        # Building the SQL query qry
        qry = "SELECT * FROM taggy_keywords WHERE domainId = "+str(domainId)

        # execution of the query 'qry'
        results = self.getData(qry)

        # return the data
        return results

    """
    GET KEYWORDS BY TAG
    """
    def getKeywordsByTag(self, tagId):
        # Building the SQL query qry
        qry = "SELECT * FROM taggy_keywords WHERE tagId = "+str(tagId)

        # execution of the query 'qry'
        results = self.getData(qry)

        # return the data
        return results

    """
    GET DATA BY KEYWORD
    (BECAUSE A KEYWORD CAN APPEAR FOR MORE TAGS)
    """
    def getKeyword(self, keyword):
        # Building the SQL query qry
        qry = "SELECT * FROM taggy_keywords WHERE keyword = '"+ keyword +"'"

        # execution of the query 'qry'
        results = self.getData(qry)

        # return the data
        return results

    """
    GET DATA BY KEYWORD
    (BECAUSE A KEYWORD CAN APPEAR FOR MORE TAGS)
    """
    def getKeywordById(self, keywordId):
        # Building the SQL query qry
        qry = "SELECT * FROM taggy_keywords WHERE id = "+ str(keywordId)

        # execution of the query 'qry'
        results = self.getData(qry)

        # return the data
        return results


    """
    INSERT NEW KEYWORD
    """
    def insertKeyword(self, tagId, domainId, keyword):
        # Building the SQL query qry
        qry = "INSERT INTO taggy_keywords(tagId, domainId, keyword) VALUES("+str(tagId)+ ","+str(domainId)+",'"+keyword+"')"

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    DELETE KEYWORD
    """
    def deleteKeywordById(self, keywordId):

        # Building the SQL query 'qry'
        qry =  "DELETE FROM taggy_keywords "
        qry += "WHERE id = "+str(keywordId)

        # execution of the query 'qry'
        status = self.getData(qry)

        #return status
        return status

    """
    DELETE KEYWORD
    """
    def deleteKeywordById(self, keyword):

        # Building the SQL query 'qry'
        qry =  "DELETE FROM taggy_keywords "
        qry += "WHERE keyword = '"+keyword+"' "

        # execution of the query 'qry'
        status = self.getData(qry)

        #return status
        return status

    """
    CREATE TAG
    """
    def createTag(self, tagName, tagDescription, provideOrRequest, domainId):
        # Building the SQL query qry
        qry = "INSERT INTO taggy_tags(tagName, tagDescription, provideOrRequest, domainId) VALUES('"+tagName+ "','"+tagDescription+"','"+provideOrRequest+"',"+str(domainId)+")"

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status


    """
    DELETE
    """
    def deleteTag(self, tagId):
        # Building the SQL query qry
        qry = "DELETE FROM taggy_tags WHERE tagId = "+str(tagId)

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    UPDATE TAG
    """
    def updateTag(self, tagId, tagName='', tagDescriotion='', provideOrRequest='', domainId=-1):
        # Building the SQL query qry
        qry = "UPDATE taggy_tags WHERE tagId = "+str(tagId)
        qry +=" SET tagName = '"+tagName+"',"
        qry +=      "tagDescription = '"+tagDescriotion+"', "
        qry +=      "provideOrRequest = '"+provideOrRequest+", "
        qry +=      "domainId = "+str(domainId)

        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    UPDATE TAG NAME
    """

    def updateTagName(self, tagId, tagName):
        # Building the SQL query qry
        qry = "UPDATE taggy_tags WHERE tagId = " + str(tagId)
        qry += " SET tagName = '" + tagName + "'"


        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    UPDATE TAG DESCRIPTION
    """

    def updateTagDescription(self, tagId, tagDescription):
        # Building the SQL query qry
        qry = "UPDATE taggy_tags WHERE tagId = " + str(tagId)
        qry += " SET tagDescription = '" + tagDescription + "'"


        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status


    """
    UPDATE TAG provide or request
    """

    def updateTagPOR(self, tagId, provideOrRequest):
        # Building the SQL query qry
        qry = "UPDATE taggy_tags WHERE tagId = " + str(tagId)
        qry += " SET provideOrRequest = '" + provideOrRequest + "'"


        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status

    """
    UPDATE TAG domain
    """

    def updateTagDomain(self, tagId, domainId):
        # Building the SQL query qry
        qry = "UPDATE taggy_tags WHERE tagId = " + str(tagId)
        qry += " SET domainId = " + str(domainId)


        # execution of the query 'qry'
        status = self.insertOrUpdate(qry)

        # return the data
        return status


    """
    GET TAGS OF A SPECIFIC DOMAIN
    """
    def getTagsForDomain(self, domainid):
        # Building the SQL query qry
        qry = "SELECT * FROM taggy_tags WHERE domainId = " + str(domainid)

        # execution of the query 'qry'
        results = self.getData(qry)

        # return the data
        return results


    """
    GET SENTENCE IF ANNOTATED BY ANNOTATOR
    """
    def getSentenceAnnotator(self, sententenceId, annotatorId):
        # Building the SQL query qry
        qry = "SELECT * FROM taggy_sentences_tags WHERE sentenceId = " + str(sententenceId) + " AND annotatorId = "+str(annotatorId)

        # execution of the query 'qry'
        results = self.getData(qry)

        # return the data
        return results



    """
    GET JSON DOCUMENTS
    """
    def getJSONDocumentsMeta(self):
        # Building the SQL query qry
        qry = "SELECT * FROM taggy_document"

        # execution of the query 'qry'
        results = self.getData(qry)

        # return the data
        return results