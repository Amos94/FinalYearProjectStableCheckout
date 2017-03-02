from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Annotators(models.Model):

    annotatorId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=32)
    usertype = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Annotators"




class Annotators_sets(models.Model):

    setId = models.AutoField(primary_key=True)
    annotatorId = models.IntegerField()

    class Meta:
        verbose_name_plural = "Annotators sets"




class Categories(models.Model):

    categoryId = models.AutoField(primary_key=True)
    catName = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"




class Check_posts(models.Model):

    postId = models.IntegerField()
    forumId = models.IntegerField()
    topicId = models.IntegerField()
    creationDate = models.DateTimeField()
    profileId = models.IntegerField()
    authorName = models.TextField()

    class Meta:
        verbose_name_plural = "Check posts"




class Emoticons(models.Model):

    emoticonId = models.AutoField(primary_key=True)
    canonicalForm = models.TextField()

    class Meta:
        verbose_name_plural = "Emoticons"



class Emoticons_tag(models.Model):

    tagId = models.AutoField(primary_key=True)
    emoticonId = models.IntegerField()
    rawTag = models.IntegerField()

    class Meta:
        verbose_name_plural = "Emoticons tag"


class Forums(models.Model):

    forumId = models.IntegerField()
    forumName = models.CharField(max_length=100)
    forumDescription = models.CharField(max_length=250)
    categoryId = models.IntegerField()

    class Meta:
        verbose_name_plural = "Forums"




class Posts(models.Model):

    postId  = models.AutoField(primary_key=True)
    forumId = models.IntegerField()
    topicId = models.IntegerField()
    creationDate = models.DateTimeField()
    profileId = models.IntegerField()
    content = models.TextField()
    postState = models.TextField(default='INITIAL')
    dateReviewed = models.DateTimeField()
    dateParsed = models.DateTimeField()
    parseVersion = models.IntegerField(default=0)
    parseTool = models.TextField()
    parseHistory = models.TextField()


    class Meta:
        verbose_name_plural = "Posts"



class Posts_annotators(models.Model):

    annotatorId = models.IntegerField()
    postId = models.IntegerField()
    numSentencesInPost = models.IntegerField()
    comment = models.TextField()
    numSentencesTagged = models.IntegerField()
    lastUpdated = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Posts annotators"


class Posts_emoticons(models.Model):

    postId = models.IntegerField()
    emoticonId = models.IntegerField()
    tagId = models.IntegerField()

    class Meta:
        verbose_name_plural = "Post emoticons"




class Posts_sets(models.Model):

    setId = models.IntegerField()
    postId = models.IntegerField()

    class Meta:
        verbose_name_plural = "Posts sets"




class Profiles(models.Model):

    profileId = models.IntegerField()
    userName = models.CharField(max_length=50)
    memberSince = models.DateField()
    lastLogin = models.DateField()
    location = models.CharField(max_length=100)
    dob = models.DateField()
    occupation = models.CharField(max_length=150)
    biography = models.TextField()
    diagnosis = models.CharField(max_length=100)
    diagnosed = models.DateField()
    recurrent = models.CharField(max_length=150)
    metastatic = models.CharField(max_length=10)
    stage = models.CharField(max_length=10)
    lymph = models.CharField(max_length=10)
    posLymphNodes = models.CharField(max_length=10)
    tumorSize = models.CharField(max_length=20)
    tumorGrade = models.CharField(max_length=30)
    hormoneReceptor = models.CharField(max_length=100)
    herStatus = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Profiles"




class Sentences(models.Model):

    sentenceId = models.AutoField(primary_key=True)
    postId = models.IntegerField()
    sentence = models.TextField()
    paragraphInPost = models.IntegerField()
    sentenceInParagraph = models.IntegerField()

    class Meta:
        verbose_name_plural = "Sentences"





class Sentences_tags(models.Model):

    sentenceId = models.IntegerField()
    tagId = models.IntegerField()
    postId = models.IntegerField()
    annotatorId = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Sentences tags"




class Sets(models.Model):

    setId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    description = models.TextField()
    creatordId = models.IntegerField()

    class Meta:
        verbose_name_plural = "Sets"




class Signatures(models.Model):

    postId = models.IntegerField()
    profileId = models.IntegerField()
    signatures = models.TextField()

    class Meta:
        verbose_name_plural = "Signatures"




class Tags(models.Model):

    tagId = models.AutoField(primary_key=True)
    tagName = models.CharField(max_length=4)
    tagDescription = models.CharField(max_length=250)
    provideOrRequest = models.CharField(max_length=1)

    class Meta:
        verbose_name_plural = "Tags"



class Topics(models.Model):

    topicId = models.IntegerField()
    url = models.CharField(max_length=25)
    title = models.CharField(max_length=150)
    creationDate = models.DateTimeField()
    profileId = models.IntegerField()
    lastDate = models.DateTimeField()
    numViews = models.IntegerField()
    forumId = models.IntegerField()

    class Meta:
        verbose_name_plural = "Topics"