from django.urls import path, include
from rest_framework.routers import DefaultRouter

from DiscoCodeClient import views

router = DefaultRouter()
router.register(r'configuration', views.ConfigurationViewSet, basename='configuration')
router.register(r'state', views.StateViewSet, basename='state')
router.register(r'errlogs', views.ErrLogViewSet)
router.register(r'eventlogs', views.EventLogViewSet)
router.register(r'discord-servers', views.DiscordServerViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'languages', views.LangViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", include(router.urls)),
    path('runtimes', views.forward_runtime, name='forward_runtimes'),
    path('execute', views.forward_execute, name='forward_execute'),
]
