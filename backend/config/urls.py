"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from api.views import RegisterView, LoginView, ProfileView, NoteListView, MedicineListView, NoteDetailView, \
    MedicineDetailView, DeleteAccountView, LogoutView, DocumentListView
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/profile/notes/', NoteListView.as_view()),
    path('api/profile/medicines/', MedicineListView.as_view()),
    path('api/profile/notes/<int:pk>/', NoteDetailView.as_view()),
    path('api/profile/medicines/<int:pk>/', MedicineDetailView.as_view()),
    path('api/documents/', DocumentListView.as_view()),
    path('api/delete-account/', DeleteAccountView.as_view(), name='delete-account'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)