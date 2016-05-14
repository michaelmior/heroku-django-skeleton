from django.conf.urls import url

import app.main.views


urlpatterns = [
    url(r'^', app.main.views.index),
]
