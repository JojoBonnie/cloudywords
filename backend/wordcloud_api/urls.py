from django.urls import path
from .views import (
    WordCloudListCreateView,
    WordCloudDetailView,
    GenerateWordCloudView,
    AIWordSuggestionsView,
    UserCreditView,
    WordCloudExportView
)

urlpatterns = [
    path('wordclouds/', WordCloudListCreateView.as_view(), name='wordcloud-list-create'),
    path('wordclouds/<int:pk>/', WordCloudDetailView.as_view(), name='wordcloud-detail'),
    path('wordclouds/generate/', GenerateWordCloudView.as_view(), name='wordcloud-generate'),
    path('wordclouds/<int:pk>/export/', WordCloudExportView.as_view(), name='wordcloud-export'),
    path('ai/suggestions/', AIWordSuggestionsView.as_view(), name='ai-word-suggestions'),
    path('user/credits/', UserCreditView.as_view(), name='user-credits'),
]
