from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'^books$', views.show_books),
    url(r'^books/(?P<id>\d+)$', views.show_book),
    url(r'^books/new$', views.new_book),
    url(r'^books/add$', views.add_book),
    url(r'^users/(?P<id>\d+)$', views.show_user),
    url(r'^create_user$', views.create_user),
    url(r'^users/logout$', views.logout),
    url(r'^users/login$', views.login),
    url(r'^books/review/delete/(?P<id>\d+)$', views.delete_review),
    url(r'^books/review/add/(?P<id>\d+)$', views.add_review),


]