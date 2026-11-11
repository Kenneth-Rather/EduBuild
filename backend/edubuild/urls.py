"""URL routes for the EduBuild prototype backend."""

from django.urls import include, path

urlpatterns = [
    path("api/", include("games.urls")),
]

"""Django Template"""