from taggy.modules.Queries import Queries
from django.db import connection

class Set():
    """
    * id of set
    *
    * @var int
    """
    setId = -1

    """
    * name of set
    *
    * @var string
    """
    name = ""

    """
    * description of set
    *
    * @var string
    """
    description = ""

    """
    * ordered collection of postID's in set
    *
    * @var string
    """
    post_ids = []

    """
    * Constructor of Set object
    *
    * @param string $qryObject
    * @param string $id setID
    """
    def __init__(self, qryObject, id):
        """

        :type qryObject: Queries
        """
        self.setId = id

        meta_results = qryObject.getSetMeta(id)

        if(meta_results.count() == 0):
            raise Exception('SetID ' + id + ' does not exist')

        with connection.cursor() as cursor:
            cursor.execute(meta_results)
            # fetching all data of the query 'qry'
            meta_row = cursor.fetchall()

            self.name = meta_row['name']
            self.description = meta_row['description']

        #QueryDB for PostIDs
        posts_results = qryObject.getSet(id)
        if(posts_results.count() == 0):
            raise Exception('SetID ' + id + ' is empty')

        with connection.cursor() as cursor:
            cursor.execute(posts_results)
            # fetching all data of the query 'qry'
            row = cursor.fetchall()

        for r in row:
            self.post_ids.append(r['postId'])


    """
        does post with id postId exist in the array?
        return ture or false;
    """
    def containsPost(self, postId):
        toReturn = False

        for id in self.post_ids:
            if(postId == id):
                toReturn = True

        return toReturn


    """
    returns first postid
    """
    def firstPostID(self):
        return self.post_ids[0]

    """
        returns next PostId
    """
    def getNextPostId(self, postId):

        for a in self.post_ids:
            if (self.post_ids[a] == postId):
                pos = a

        if(pos == False):
            return
        if((pos+1) > self.post_ids.count()):
            return -1
        return self.post_ids[pos+1]

    """
        returns previous PostId
    """
    def getPrevPostId(self, postId):

        for a in self.post_ids:
            if (self.post_ids[a] == postId):
                pos = a

        if (pos == False):
            return

        if (pos == 0):
            return -1

        return self.post_ids[pos-1]

    """
    * factory convenience method to get Set object by id
    * optionally, when annotatorID is given, it authenticates annotator
    *
    * @param string $qryObject
    * @param string $setId
    * @param string $annotatorID
    * @return void
    """

    def get_set( self, qryObject, setId, annotatorId = '' ):
        """

        :type qryObject: Queries
        """
        if(annotatorId):
            if(not(qryObject.checkSetAnnotatorAssignment( setId, annotatorId ))):
                raise Exception( 'SetID ' +setId + ' not associated with Annotator: ' +annotatorId )
        return Set(qryObject, setId)