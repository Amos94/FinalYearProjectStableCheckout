import random

import MySQLdb
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

    #gets just one
    def getOne(self,qry):
        # execution of the query 'qry'
        with connection.cursor() as cursor:
            cursor.execute(qry)
            # fetching all data of the query 'qry'
            qryResult = cursor.fetchone()
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
        qry += "WHERE postID="+postid


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
        number = self.getData(qry)['num']
        rnd = random.uniform(0, number-1)
        randomNumber = int(rnd)

        # execution of the query 'qry'
        qry = "" #just want to make sure qry is empty, even though, in if-else statement, qry will get another value
        if(DBName == "perseus"):
            qry =  "SELECT postId,forumId,topicId,"
            qry += "DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "profileID,postState,content "
            qry += "FROM taggy_posts "
            qry += "WHERE postState='PARSED' "
            qry += "LIMIT 1 OFFSET "+randomNumber
        else:
            qry =  "SELECT postId,forumId,"
            qry += "DATE_FORMAT(creationDate,'%e-%b-%Y') AS creation,"
            qry += "postState,content "
            qry += "FROM taggy_posts "
            qry += "WHERE postState='PARSED' "
            qry += "LIMIT 1 OFFSET "+randomNumber

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
        qry += "WHERE postId="+postid+" "
        qry += "AND taggy_posts.profileId=taggy_profiles.profileID"


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
        qry += "WHERE ((postId="+postid+") AND (annotatorId="+annotatorid+")) "

        # execution of the query 'qry'
        qryResult = self.getData(qry)

        #Create if none exists

        if(not qryResult):
            insertQry =  "INSERT INTO taggy_posts_annotators (annotatorId, postId, numSentencesInPost, comment, numSentencesTagged, lastUpdated) "
            insertQry += "SELECT "+annotatorid+" as annotatorId, "+postid+" as postId, "
            insertQry += "count(sentenceId) as numSentencesInPost, " # count sentences in the post
            insertQry += "'' as comment, 0 as numSentencesTagged, NOW() as lastUpdated " # default values (move into Table Definition?)
            insertQry += "FROM sentences WHERE (postId="+postid+") "

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
        qry +=      "WHERE (postId = "+postid+") AND (annotatorId = "+annotatorid+")) "

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

    def updatePostState(self, postid, postState = None):

        if(postState != None):
            newPostState = None  # initially no change
        else:
            #update post state
            #get old post state
            result = self.getData("SELECT postState FROM taggy_posts WHERE postId="+postid)
            row = self.getOne(result)
            oldPostState = row['postState']

            #Check if PostState is able to be updated based on postAnnotatorStates
            if(oldPostState in ["PARSED", "ANNOTATED", "ADJUDICATED"]):
                # Get counts of postAnnotatorStates
                cntSQL =  "SELECT postAnnotatorState, count(*) AS n "
                cntSQL += "FROM taggy_posts_annotators "
                cntSQL += "WHERE (postId = '"+postid+"')  "
                cntSQL += "GROUP BY postAnnotatorState"

                result = self.getData(cntSQL)

                numStates = []

                #Build a map of postAnnotatorState => n
                while(row == self.getOne(result)):
                    numStates[row["postAnnotatorState"]] = row["n"]


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
        if(newPostState != None):
            qry =  "UPDATE taggy_posts "
            qry += "SET postState='"+newPostState+"' "
            qry += "WHERE postID="+postid

            updateStatus = self.getData(qry)

            return updateStatus

        return True




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
        qry += "WHERE postId="+postid


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
        if($DBName == "perseus" ):
            qry =  "SELECT tagId,tagName,tagDescription,provideOrRequest "
            qry += "FROM taggy_tags "

            if(option != ''):
                qry += "WHERE provideOrRequest='"+option+"' "

            qry += "ORDER BY tagName,provideOrRequest"

        else:
            qry =  "SELECT tagID,tagName,tagDescription "
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
        qry =  "SELECT tagName, MIN(tagID) AS tagID1, MAX(tagID) AS tagID2 "
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
        qry =  "SELECT postId,sentenceId,sentence,paragraphInPost,sentenceInParagraph "
        qry += "FROM taggy_sentences "
        qry += "WHERE postId="+postid+" "
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
        qry =  "SELECT sentences.postId,sentenceId,sentence,paragraphInPost,sentenceInParagraph "
        qry += "FROM taggy_sentences,taggy_posts_sets "
        qry += "WHERE setId="+setid+" "
        qry += "AND posts_sets.postId=sentences.postId "
        qry += "ORDER BY postId,sentenceId,paragraphInPost,sentenceInParagraph"

        # execution of the query 'qry'
        qryResult = self.getData(qry)

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
        qry += "WHERE sentenceId = "+sentenceid
        qry += " AND postId = "+postid
        ary += " AND annotatorId = "+annotatorid

        #execution of the query 'qry'
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
        qry += "WHERE sentenceId = "+sentenceid
        qry += " AND annotatorId = "+annotatorid
        qry += " AND tagId IN "+tagidstring

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
        qry += "WHERE (postId = "+postid+") "

        qry += " AND (annotatorID IN ("
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
        qry += "VALUES ("+sentenceid+","+tagid+","+postid+","+annotatorid+",NOW())"

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
        qry += "WHERE ((sentenceId = "+sentenceid+") "
        qry += "AND (tagId = "+tagid+") "
        qry += "AND (postId = "+postid+") "
        qry += "AND (annotatorId = "+annotatorid+"))"

        # execution of the query 'qry'
        status = self.getData(qry)

        #return status
        return status