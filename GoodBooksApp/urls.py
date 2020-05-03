from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from .views import BookList, bookDetails
from .views import Homepage, profileView
from .views import deleteFeedback, addReadBook, delReadBook
from .views import logoutRequest, deleteProfile
from .views import UserLoginView, signup, login_request, handleAnon
urlpatterns = [
    path('book-list/', BookList, name='book-list'),
    path('details/<int:id>/', bookDetails, name='book-detail'),
    path('', Homepage),
    path('profile/', profileView),
    path("login/", login_request, name="login"),
    path('signup/', signup),
    path('delete-feedback/', deleteFeedback),
    path('add-read-book/', addReadBook),
    path('del-read-book/', delReadBook),
    path('logout/', logoutRequest, name='logout'),
    path('delete-profile/', deleteProfile),
    path('anonuser/', handleAnon)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
