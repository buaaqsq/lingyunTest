from django.conf.urls import patterns, include, url

from django.contrib import admin,auth
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hadoop.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),   
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^qsq/hbase$', 'qsq.views.initHbaseConf', name='hbase'),
    url(r'^qsq/snapshot$', 'qsq.views.snapshot', name='hbase'),
    url(r'^qsq/dashboard', 'qsq.views.dashboard', name='hbase'),
    url(r'^qsq/heatmaps', 'qsq.views.heatmaps', name='hbase'),
    url(r'^qsq/services', 'qsq.views.services', name='hbase'),
    url(r'^qsq/jobs', 'qsq.views.getJobs', name='hbase'),
    url(r'^qsq/hosts', 'qsq.views.hosts', name='hbase'),
    url(r'^qsq/step6hadoop/$', 'qsq.views.step6hadoop', name='install'),
    url(r'^qsq/step6hbase/$', 'qsq.views.step6hbase', name='install'),
    url(r'^qsq/step6hive/$', 'qsq.views.step6hive', name='install'),
    url(r'^qsq/step6spark/$', 'qsq.views.step6spark', name='install'),
    url(r'^qsq/review/$', 'qsq.views.getReview', name='install'),
    url(r'^qsq/step/(?P<step>\d\d)/$', 'qsq.views.getStep', name='install'),
    url(r'^qsq/test', 'qsq.views.test', name='test'),
    url(r'^qsq/install', 'qsq.views.install', name='install'),
)
