from django.urls import path
from askit_app import views

app_name = 'askit_app'
urlpatterns = [
    path('',views.index),
    path('about',views.about),
    path('signup',views.signup),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('questions',views.QuestionListView.as_view(), name="question-list"),
    path('questions/<int:pk>',views.QuestionDetailView.as_view(), name="question-detail"),
    path('questions/new',views.QuestionCreateView.as_view(), name="question-create"),
    path('questions/<int:pk>/update',views.QuestionUpdateView.as_view(), name="question-update"),
    path('questions/<int:pk>/delete',views.QuestionDeleteView.as_view(), name="question-delete"),
    path('questions/<int:pk>/comment',views.AddCommentView.as_view(), name="question-comment"),
    path('like/<int:pk>',views.like_view),
    path('makepayment',views.makepayment),
    path('sendmail/<username>',views.sendusermail),
    path('pricing',views.pricing),
]