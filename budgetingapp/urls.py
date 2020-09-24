"""budgetingapp URL Configuration

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
from django.urls import path, re_path
from django.views.generic.base import TemplateView
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from . import views
import accounts.views
import budget.views
import goals.views
import resources.views


# path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
favicon_view = RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('favicon.ico/', favicon_view),
    re_path(r'^favicon\.ico$', favicon_view),
    path('', views.home, name='home'), 
    path('home/', views.home), 
    path('welcome/', TemplateView.as_view(template_name='welcome.html'), name='welcome'), 
    path('onboarding/', views.onboarding, name='onboarding'), 
    path('budget/', budget.views.budgetpage, name='budget'), 
    path('goals/<pk>/', goals.views.GoalUpdate.as_view()), 
   # path('goals.html', goals.views.goalspage, name='goals'),
    path('new-goals/', goals.views.GoalCreate.as_view(), name='newgoal'), 
    path('new-income/', budget.views.IncomeCreate.as_view(), name='newincome'), 
    path('new-budget-expense/', budget.views.BudgetExpenseCreate.as_view(), name='newbudgetexpense'),
    path('new-account/', accounts.views.AccountCreate.as_view(), name='newaccount'),
    path('test/', views.test), 
    path('accounts/', accounts.views.accounts_page, name='accounts'),
    path('resources/', resources.views.ResourceListView.as_view(), name='resources')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # path('signup.html', accounts.views.SignUp.as_view(), name='signup'),
