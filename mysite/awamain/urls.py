from django.urls import path
from .views import (HomeView,
                    BookDetailView,
                    AddBookView,
                    UpdateBookView,
                    DeleteBookView,
                    CategoryView,
                    LikeView,
                    AddCommentView,
                    UserBooksView,
                    )


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('user_books', UserBooksView.as_view(), name='user-books'),
    path('book/<int:pk>', BookDetailView.as_view(), name='book-detail'),
    path('add_book/', AddBookView.as_view(), name='add-book'),
    path('book/edit/<int:pk>', UpdateBookView.as_view(), name='update-book'),
    path('book/delete/<int:pk>', DeleteBookView.as_view(), name='delete-book'),
    path('categories/<str:cats>/', CategoryView, name='category'),
    path('like/<int:pk>', LikeView, name='like_book'),
    path('book/<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
]
