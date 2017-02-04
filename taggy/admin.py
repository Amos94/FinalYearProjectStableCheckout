from django.contrib import admin
from models import Annotators, Annotators_sets, Categories, Check_posts, Emoticons, Emoticons_tag, Forums, Posts, Posts_annotators, Posts_emoticons, Posts_sets, Profiles, Sentences, Sentences_tags, Sets, Signatures, Tags, Topics
# Register your models here.
class AnnotatorsAdmin(admin.ModelAdmin):
    list_display = ['annotatorId','username','password','usertype']

admin.site.register(Annotators, AnnotatorsAdmin)


class Annotators_setsAdmin(admin.ModelAdmin):
    list_display = ['setId', 'annotatorId']

admin.site.register(Annotators_sets, Annotators_setsAdmin)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['categoryId', 'catName']

admin.site.register(Categories, CategoriesAdmin)


class Check_postsAdmin(admin.ModelAdmin):
    list_display = ['postId', 'forumId', 'topicId', 'creationDate', 'profileId', 'authorName']

admin.site.register(Check_posts, Check_postsAdmin)



class EmoticonsAdmin(admin.ModelAdmin):
    list_display = ['emoticonId', 'canonicalForm']

admin.site.register(Emoticons, EmoticonsAdmin)


class Emoticons_tagAdmin(admin.ModelAdmin):
    list_display = ['tagId', 'emoticonId', 'rawTag']

admin.site.register(Emoticons_tag, Emoticons_tagAdmin)



class ForumsAdmin(admin.ModelAdmin):
    list_display = ['forumId', 'forumName', 'forumDescription', 'categoryId']

admin.site.register(Forums, ForumsAdmin)





class PostsAdmin(admin.ModelAdmin):
    list_display = ['postId', 'forumId', 'topicId', 'creationDate', 'profileId', 'content']

admin.site.register(Posts, PostsAdmin)



class Posts_annotatorsAdmin(admin.ModelAdmin):
    list_display = ['annotatorId', 'postId', 'numSentencesInPost', 'comment', 'numSentencesTagged', 'lastUpdated']

admin.site.register(Posts_annotators, Posts_annotatorsAdmin)



class Posts_emoticonsAdmin(admin.ModelAdmin):
    list_display = ['postId', 'emoticonId', 'tagId']

admin.site.register(Posts_emoticons, Posts_emoticonsAdmin)



class Posts_setsAdmin(admin.ModelAdmin):
    list_display = ['setId', 'postId']

admin.site.register(Posts_sets, Posts_setsAdmin)



class ProfilesAdmin(admin.ModelAdmin):
    list_display = ['profileId', 'userName', 'memberSince', 'lastLogin', 'location', 'dob', 'occupation', 'biography', 'diagnosis', 'diagnosed', 'recurrent', 'metastatic', 'stage', 'lymph', 'posLymphNodes', 'tumorSize', 'tumorGrade', 'hormoneReceptor', 'herStatus']

admin.site.register(Profiles, ProfilesAdmin)



class SentencesAdmin(admin.ModelAdmin):
    list_display = ['sentenceId', 'postId', 'sentence', 'paragraphInPost', 'sentenceInParagraph']

admin.site.register(Sentences, SentencesAdmin)




class Sentences_tagsAdmin(admin.ModelAdmin):
    list_display = ['sentenceId', 'tagId', 'postId', 'annotatorId', 'timestamp']

admin.site.register(Sentences_tags, Sentences_tagsAdmin)



class SetsAdmin(admin.ModelAdmin):
    list_display = ['setId', 'name', 'description', 'creatordId']

admin.site.register(Sets, SetsAdmin)



class SignaturesAdmin(admin.ModelAdmin):
    list_display = ['postId', 'profileId', 'signatures']

admin.site.register(Signatures, SignaturesAdmin)




class TagsAdmin(admin.ModelAdmin):
    list_display = ['tagId', 'tagName', 'tagDescription', 'provideOrRequest']

admin.site.register(Tags, TagsAdmin)



class TopicsAdmin(admin.ModelAdmin):
    list_display = ['topicId', 'url', 'title', 'creationDate', 'profileId', 'lastDate', 'numViews', 'forumId']

admin.site.register(Topics, TopicsAdmin)