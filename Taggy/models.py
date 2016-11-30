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
    creationDate = models.DateField()
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
