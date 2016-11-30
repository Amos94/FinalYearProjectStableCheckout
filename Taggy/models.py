from __future__ import unicode_literals

from django.db import models

# Create your models here.

class annotators(models.Model):

    annotatorId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=32)
    usertype = models.CharField(max_length=10)




class annotators_sets(models.Model):

    setId = models.AutoField(primary_key=True)
    annotatorId = models.IntegerField()




class categories(models.Model):

    categoryId = models.AutoField(primary_key=True)
    catName = models.CharField(max_length=100)




class chack_posts(models.Model):

    postId = models.IntegerField()
    forumId = models.IntegerField()
    topicId = models.IntegerField()
    creationDate = models.DateTimeField()
    profileId = models.IntegerField()
    authorName = models.TextField()




class emoticons(models.Model):

    emoticonId = models.AutoField(primary_key=True)
    canonicalForm = models.TextField()



class emoticons_tag(models.Model):

    tagId = models.AutoField(primary_key=True)
    emoticonId = models.IntegerField()
    rawTag = models.IntegerField()



class forums(models.Model):

    forumId = models.IntegerField()
    forumName = models.CharField(max_length=100)
    forumDescription = models.CharField(max_length=250)
    categoryId = models.IntegerField()





class posts(models.Model):

    postId  = models.AutoField(primary_key=True)
    forumId = models.IntegerField()
    topicId = models.IntegerField()
    creationDate = models.DateTimeField()
    profileId = models.IntegerField()
    content = models.TextField()




class posts_annotators(models.Model):

    annotatorId = models.IntegerField()
    postId = models.IntegerField()
    numSentencesInPost = models.IntegerField()
    comment = models.TextField()
    numSentencesTagged = models.IntegerField()
    lastUpdated = models.DateTimeField()




class posts_emoticons(models.Model):

    postId = models.IntegerField()
    emoticonId = models.IntegerField()
    tagId = models.IntegerField()