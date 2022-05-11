from django.urls import path
from .views import LoginView, LogoutView, PageRedirect, MySchemesView, CreateSchemeView, DeleteSchemeView, \
    EditSchemeView, DataSetsView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('', LogoutView.as_view(), name='signout'),
    path('signup/', PageRedirect.as_view(), name='signup'),
    path('schemes/', MySchemesView.as_view(), name='list'),
    path("schemes/create", CreateSchemeView.as_view(), name="create"),
    path("schemes/edit/<int:pk>", EditSchemeView.as_view(), name="edit"),
    path("schemes/delete/<int:pk>", DeleteSchemeView.as_view(), name="delete"),
    path("schemes/export/<pk>", DataSetsView.as_view(), name="datasets"),
    path('accounts/', PageRedirect.as_view(), name='profile'),
    path('accounts/profile/', PageRedirect.as_view(), name='profile'),
]