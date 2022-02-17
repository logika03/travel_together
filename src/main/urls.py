"""searchpeople URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from main.views import TripsPageListView, TripPageDetailView, login_view, logout_view, signup_view, \
    FAQPageListView, test, AccountView, FindView, reset, ShowMessageSendMailView, ShowMessageResetPasswordView, \
    reset_password, CreateTrip, AddParticipant, ApproveParticipant

from main.views import main_page

urlpatterns = [
                  path('', main_page, name='main'),
                  path('trip/<int:pk>/', TripPageDetailView.as_view(), name='trip'),
                  path('trips/', TripsPageListView.as_view(), name='trips'),
                  path('login/', login_view, name='login'),
                  path('logout/', logout_view, name='logout'),
                  path('signup/', signup_view, name='signup'),
                  path('account/<int:pk>/', AccountView.as_view(), name='account'),
                  path('faq/', FAQPageListView.as_view(), name='faq'),
                  path('find/', FindView.as_view(), name='find'),
                  path('test/', test, name='test'),
                  path('reset/', reset, name='reset'),
                  path('sent_mail/', ShowMessageSendMailView.as_view(), name='sent_mail'),
                  path('change_password/<int:pk>', reset_password, name='change_password'),
                  path('changed_password/', ShowMessageResetPasswordView.as_view(), name='changed_password'),
                  path('create_trip/', CreateTrip.as_view(), name='create_trip'),
                  path('add_partcipant/<int:pk>/', AddParticipant.as_view(), name='add_participant'),
                  path('approve/<int:trip_id>/<int:user_id>/', ApproveParticipant.as_view(), name='approve'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
