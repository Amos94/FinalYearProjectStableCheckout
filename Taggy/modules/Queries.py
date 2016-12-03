from django.db.models import Q as Q
from Taggy.models import annotators as Annotators
from Taggy.models import posts as Posts
from Taggy.models import posts_annotators as Posts_annotators

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
            qryResult = Annotators.objects.filter(annotatorId__exact=userId)
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

    def getAnnotatorsForPost(self, postId):

        qryResult = Posts.objects.get(Q(postId=postId))

        return qryResult
