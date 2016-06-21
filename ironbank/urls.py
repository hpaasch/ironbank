
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required


from bank_app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', views.IndexView.as_view(), name='index_view'),
    url(r'^register/$', views.CreateUserView.as_view(), name='create_user_view'),
    url(r'^accounts/profile/$', login_required(views.AccountView.as_view()), name='account_view'),
    url(r'^detail/(?P<pk>\d+)/$', login_required(views.TransDetailView.as_view()), name='detail_view'),
    url(r'^transaction/$', views.CreateTransView.as_view(), name='create_trans_view'),
    url(r'^overdraft/$', views.OverdraftView.as_view(), name='overdraft_view'),
    url(r'^transfer/$', views.MakeTransferView.as_view(), name='make_transfer_view'),

]
