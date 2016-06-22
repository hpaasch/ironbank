
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required


from bank_app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', views.IndexView.as_view(), name='index_view'),
    url(r'^register/$', views.UserCreateView.as_view(), name='user_create_view'),
    url(r'^accounts/profile/$', login_required(views.AccountView.as_view()), name='account_view'),
    url(r'^detail/(?P<pk>\d+)/$', login_required(views.TransactionDetailView.as_view()), name='transaction_detail_view'),
    url(r'^transaction/$', views.TransactionCreateView.as_view(), name='transaction_create_view'),
    url(r'^transfer/$', views.TransferCreateView.as_view(), name='transfer_create_view'),

]
