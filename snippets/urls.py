from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path('snippets/', views.snippet),
    path('snippets/<int:snippet_id>/', views.snippet_detials),

    path('users/', views.users),
    path('users/<int:user_id>/', views.user_detail),


    path('snippets_class/', views.Snippets.as_view()),
    path('snippets_class/<int:pk>/', views.Snippets_Detials.as_view()),

    path('snippets_mixin/', views.Snippets_Mixin.as_view()),
    path('snippets_mixin/<int:pk>/', views.Snippets_Mixin_details.as_view()),


    path('snippets_generic/', views.Snippets_Generic.as_view()),
    path('snippets_generic/<int:pk>/', views.Snippets_Generic_Detials.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
