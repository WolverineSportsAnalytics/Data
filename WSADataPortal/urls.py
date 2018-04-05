from django.conf.urls import include, url
from django.contrib import admin
from data import views as dataViews

urlpatterns = [
    # Examples:
    # url(r'^$', 'WSADataPortal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
    url(r'^base$', dataViews.basketball, name="basketball"),
    url(r'^$', dataViews.index, name="index"),
    url(r'^base$', dataViews.basketball, name="base"),
    url(r'^data/', include('data.urls'))

]
