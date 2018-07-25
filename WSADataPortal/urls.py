from django.conf.urls import include, url
from django.contrib import admin
from data import views as basketballViews
from baseball import views as baseballViews
from wnba import views as wnbaViews
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Examples:
    # url(r'^$', 'WSADataPortal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
    url(r'^$', basketballViews.index, name="index"),
    url(r'^basket$', basketballViews.baskethome, name="basketball"),
    url(r'^wnba$', wnbaViews.index, name="wnba"),
    url(r'^baseball$', baseballViews.index, name="baseball"),
    url(r'^data/', include('data.urls')),
    url(r'^baseball/', include('baseball.urls')),
    url(r'^wnba/', include('wnba.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]
