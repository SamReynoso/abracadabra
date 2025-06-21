from django.urls import path
from app.api import organization_division, image

def api(name: str) -> str:
    return f"api_{name}"


urlpatterns = [
    path("organization-division", organization_division, name=api("organization_division")),
    path("image/", image, name=api("image")),
]
