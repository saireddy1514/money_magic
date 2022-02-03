"""moneymagic URL Configuration

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

from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf.urls import include

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login1, name="login"),
    path('', views.index, name="index"),
    path('register/',views.register, name="register"),
    path('home/',views.home, name="home" ),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('credits/', views.credits, name="credits"),
    path('calendar/', views.calendar, name="calendar"),
    path('passbook/',views.passbook, name="invoice" ),
    path('transactions/',views.inbox, name="inbox" ),
    path('tutorials/',views.tutorials, name="tutorials" ),
    path('profile/', views.profile , name="profile"),
    path('time/', views.time),
    path('encrypt/',views.encryption),
    path('tips/',views.tipsandsuggestions,name="tips"),
    path('help/',views.helpcenter,name="helpcenter"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),name="password_reset_complete"),
    path('logout/',views.logout_view,name="logout"),
    path('inserttrans/',views.inserttrans,name="inserttrans"),
    path('deletetransaction/<str:tid>',views.deletetransaction,name="deletetransaction"),
    path('updatetransaction/<int:tid>',views.updatetransaction,name="updatetransaction"),
    path('updatecode/',views.updatetransactiondata,name="updatecode"),
   ]



urlpatterns += staticfiles_urlpatterns()