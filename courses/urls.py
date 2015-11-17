"""online_learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from rest_framework import routers
from courses.views import CourseView, CourseSessionView, EventsView

router = routers.DefaultRouter()
router.register('course', CourseView, base_name='course')

urlpatterns = [
    url(r'^course/(?P<course_id>[0-9]+)/session/$', CourseSessionView.as_view(actions={'get': 'list'}),
        name='course_session'),

    url(r'^course/(?P<course_id>[0-9]+)/session/(?P<pk>[0-9]+)/$',
        CourseSessionView.as_view(actions={'get': 'retrieve'}), name='course_session'),

    url(r'^course/(?P<course_id>[0-9]+)/session/(?P<pk>[0-9]+)/complete_chapter/$',
        CourseSessionView.as_view(actions={'get': 'complete_chapter'}), name='complete_chapter'),

    url(r'^course/(?P<course_id>[0-9]+)/session/(?P<pk>[0-9]+)/enroll/$',
        CourseSessionView.as_view(actions={'get': 'enroll'}), name='enroll'),

    url(r'^events/$', EventsView.as_view(), name='events')
]

urlpatterns += router.urls



