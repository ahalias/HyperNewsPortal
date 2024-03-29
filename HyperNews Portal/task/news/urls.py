from django.urls import path, re_path
from news.views import MainPageView, NewsView, NewsArticleView, CreateNewsFormView
from django.conf import settings
from django.conf.urls.static import static
from news import views

urlpatterns = [
    path('', MainPageView.as_view()),
    path('news/', NewsView.as_view()),
    path('news/<int:link>/', NewsArticleView.as_view()),
    path('news/create/', CreateNewsFormView.as_view()),
    path('news/?P<query>\w+/', NewsView.as_view(), name='search')
]

urlpatterns += static(settings.STATIC_URL)