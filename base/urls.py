from django.urls import path
from .views import Home, RegisterUser, RegisterRevenue, RevenuePage, UserPage, FavoritesRecipes, DeleteMessage, FilterRecipes, User ,loginUser, logoutUser
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('register-user', RegisterUser.as_view(), name='register-user'),
    path('register-revenue', login_required(RegisterRevenue.as_view(), login_url='/login'), name='register-revenue'),
    path('login/', loginUser, name='login-user'),
    path('logout', logoutUser, name='logout-user'),
    path('user-page', UserPage.as_view(), name='user-page'),
    path('busca', FilterRecipes.as_view(), name='filtered-recipes'),
    path('user-page/favorites-recipe', FavoritesRecipes.as_view(), name='favorites-recipes'),

    path('recipe/<str:pk>', RevenuePage.as_view(), name='recipe-page'),
    path('delete-message/<str:pk>', DeleteMessage.as_view(), name='delete-message'),
    path('user/<str:pk>', User.as_view(), name='user'),
]