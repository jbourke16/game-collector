from django.urls import path
from .views import Home, GameList, GameDetail, DeveloperListCreate, DeveloperDetail, TypeList, TypeDetail, AddGenreToGame, CreateUserView, LoginView, VerifyUserView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('games/', GameList.as_view(), name='game-list'),
    path('games/<int:id>/', GameDetail.as_view(), name='game-detail'),
    path('games/<int:game_id>/developers/', DeveloperListCreate.as_view(), name='developer-list-create'),
    path('games/<int:game_id>/developers/<int:id>/', DeveloperDetail.as_view(), name='developer-detail'),
    path('type/', TypeList.as_view(), name='type-list'),
    path('type/<int:id>', TypeDetail.as_view(), name='type-detail'),
    path('games/<int:game_id>/add_genre/<int:genre_id>/', AddGenreToGame.as_view(), name='add-genre-to-game'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh')

]
