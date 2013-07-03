from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView#, DetailView
#from tumblelog import PostDetailView
from tumblelog.views import PostDetailView
from tumblelog.models import Post

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(
        queryset=Post.objects.all(),
        context_object_name="posts_list"),
        name="home"
    ),
    url(r'^post/(?P<slug>[a-zA-Z0-9-]+)/$', PostDetailView.as_view(
        queryset=Post.objects.all(),
        context_object_name="post"),
        name="post"
    ),
    url(r'^admin/', include(admin.site.urls)),

    # Examples:
    # url(r'^$', 'tumblelog.views.home', name='home'),
    # url(r'^tumblelog/', include('tumblelog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
