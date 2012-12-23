from django.conf.urls import patterns, url


urlpatterns = patterns('app.main.views',
    url(r'^$', 'index'),
)
