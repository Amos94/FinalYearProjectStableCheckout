"""FYP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from taggy.views import importJson
from taggy.views import index as index
from taggy.views import about as about
from taggy.views import annotation as annotation
from taggy.views import adjudication as adjudication
from taggy.views import setCreate as setCreate
from taggy.views import successPage as success
from taggy.views import failPage as fail
from taggy.views import editSet as editSet
from taggy.views import deleteSet as deleteSet
from taggy.views import assignSet as assignSet
from taggy.views import browseSet as browseSet
from taggy.views import tagSet as tagSet
from taggy.views import adjudicateSet as adjudicateSet
from taggy.views import tagPost as tagPost
from taggy.views import reviewSet as reviewSet
from taggy.views import reviewParse as reviewParse
from taggy.views import postKappaDetails
from taggy.views import tagAction
from taggy.views import list
from taggy.views import editSetAdd
from taggy.views import editSetTopic
from taggy.views import assignSetAdd
from taggy.views import assignSetAnnotator
from django.conf.urls.static import static
from FYP import settings
from taggy.views import domainCreate
from taggy.views import domainEdit
from taggy.views import editDomainName
from taggy.views import assignDomain
from taggy.views import assignDomainAdd
from taggy.views import assignDomainAnnotator
from taggy.views import createTag
from taggy.views import createTagAdd
from taggy.views import deleteTag
from taggy.views import deleteTagAction
from taggy.views import tagUpdateDb
from taggy.views import deletePostTags
from taggy.views import tagDeleteDb
from taggy.views import parseJson
import registration.backends.default.urls as registration
from taggy.views import postFinalize
from taggy.views import deleteSetAnnotator
from taggy.views import delete_annotator_set_view
from taggy.views import deleteAnnotatorSetAction

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name="index"),
    url(r'^about/', about, name="about"),
    url(r'^annotation/', annotation, name="annotation"),
    url(r'^adjudication/', adjudication, name="adjudication"),
    url(r'^set/create/', setCreate, name="create_set"),
    url(r'^set/edit/', editSet, name="edit_set"),
    url(r'^set/edit-add/', editSetAdd, name="edit_set_add"),
    url(r'^set/topic-add/', editSetTopic, name="edit_set_topic"),
    url(r'^set/assign-add/', assignSetAdd,name="assign_set_add"),
    url(r'^set/assign-add-annotator/',assignSetAnnotator, name="assign_set_annotator"),
    url(r'^set/review/', reviewSet, name="review_set"),
    url(r'^review/parse/', reviewParse, name="review_parse"),
    url(r'^set/delete/', deleteSet, name="delete_set"),
    url(r'^set/assign/', assignSet, name="assign_set"),
    url(r'^set/browse/', browseSet ,name="browse_set"),
    url(r'^set/tag/',tagSet, name='tag_set'),
    url(r'^action/tag/', tagAction, name='tag_action'),
    url(r'^tag/update-db/', tagUpdateDb, name='tag_post_update'),
    url(r'^upload/json/', list, name='list'),
    url(r'^postkappadetails/', postKappaDetails, name='postKappaDetails'),
    url(r'^post/update-tag/', deletePostTags, name='update_post_tags'),
    url(r'^post/delete-tag/', tagDeleteDb, name='delete_post_tags'),
    url(r'^set/adjudicate/', adjudicateSet, name='adjudicate_set'),
    url(r'^domain/create/',domainCreate ,name="create_domain"),
    url(r'^domain/edit/',domainEdit ,name="edit_domain"),
    url(r'^domain/edit-name/',editDomainName ,name="edit_domain_name"),
    url(r'^domain/assign/', assignDomain, name='assign_domain'),
    url(r'^domain/assign-add/', assignDomainAdd, name='assign_domain_add'),
    url(r'^domain/assign-add-annotator/',assignDomainAnnotator, name="assign_domain_annotator"),
    url(r'^tag/create/', createTag, name="create_tag"),
    url(r'^tag/create-add/', createTagAdd, name="create_tag_add"),
    url(r'^tag/delete/', deleteTag, name="delete_tag"),
    url(r'^tag/delete-tag/', deleteTagAction, name="delete_tag_action"),
    url(r'^post/tag/', tagPost, name='tag_post'),
    url(r'^post/finalize/', postFinalize, name='finalize_post'),
    url(r'^set/delete-annotator/', deleteSetAnnotator, name='delete_set_annotator'),
    url(r'^set/delete-annotator-set/', delete_annotator_set_view, name='delete_annotator_set_view'),
    url(r'^set/delete-annotator-set-action/', deleteAnnotatorSetAction, name='delete_annotator_set_action'),
    url(r'^import/json/', importJson, name='import_json'),
    url(r'^parse/json/', parseJson, name='parse_json'),
    url(r'^accounts/', include(registration)),
    url(r'success/', success, name="success"),
    url(r'fail/', fail, name="fail")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'T.A.G.G.Y. ADMINISTRATION BOARD'
admin.site.site_title = 'T.A.G.G.Y.'
