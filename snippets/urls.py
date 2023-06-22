from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path('snippets/', views.snippet),
    path('snippets/<int:snippet_id>/', views.snippet_detials),
    path('snippets_class/', views.Snippets.as_view()),
    path('snippets_class/<int:pk>/', views.Snippets_Detials.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
