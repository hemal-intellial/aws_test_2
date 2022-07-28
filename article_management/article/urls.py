
from unicodedata import name
from django.contrib import admin
from django.urls import path
from article import views

urlpatterns = [
    
    path("article",views.article,name="article"),
    path("articles",views.article_publish,name="article_publish"),
    path("",views.article_list,name=""),
    path("user_registration",views.user_registration,name="user_registration"),
    path("user_login",views.user_login,name="user_login"),
    path("user_logout",views.user_logout,name="user_logout"),
    path("article_draft",views.article_publish,name="article_draft"),
    path("draft/<int:id>",views.article_publish,name="edit_draft"),
    path("article/<int:id>",views.article_publish,name="article"),
    path("draft_delete/<int:id>",views.draft_delete,name="draft_delete"),
    path("tag_data/<str:tag_name>",views.article_list,name="tag_data")

  
]