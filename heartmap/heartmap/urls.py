from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'dating.views.index'),
    url(r'^signup/$', 'dating.views.signup'),
    url(r'^login/$', 'dating.views.do_login'),
    url(r'^logout/$', 'dating.views.do_logout'),
    url(r'^me/$', 'dating.views.me'),
    url(r'^match/(?P<match_id>\d+)/$', 'dating.views.match'),
    url(r'^matches/$', 'dating.views.matches'),
    url(r'^incoming/$', 'dating.views.incoming'),
    url(r'^outgoing/$', 'dating.views.outgoing'),
    url(r'^connect/$', 'dating.views.connect'),
    # url(r'^$', 'heartmap.views.home', name='home'),
    # url(r'^heartmap/', include('heartmap.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
