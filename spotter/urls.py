from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('client/mycards/', views.myCards, name='mycards'),
    path('register/', views.register, name='register'),
    path('client/create/', views.createCard, name='createcard'),
    path('client/edit/<int:pk>/', views.editCard, name='editcard'),

    path('client/<int:pk>/', views.clientCardDetail, name='detailcard'),
   
    path('plan/<int:plan_pk>/', views.detailPlan, name='detailplan'),
    path('trainer/plans/create/<int:response_pk>/', views.createPlan, name='createplan'),
    path('plans/all/', views.allPlans, name='allPlans'),
    path('plan/cancel/<int:plan_pk>/', views.cancelPlan, name='cancelplan'),
    path('plan/comment/add/<int:plan_pk>/', views.addComment, name='addcomment'),
    path('plan/comments/show/<int:plan_pk>/', views.showComments, name='showcomments'),
    path('plan/add/dailyplan/<int:plan_pk>/', views.addDailyPlan, name='adddailyplan'),
    path('plan/add/dailyplan/exercise/<int:dailyplan_pk>/', views.addExercise, name='addexercise'),
    path('plan/add/dailyplan/meal/<int:dailyplan_pk>/', views.addMeal, name='addmeal'),
    path('plan/edit/dailyplan/<int:dailyplan_pk>/', views.editDailyPlan, name='editdailyplan'),
    path('plan/delete/dailyplan/exercise/<int:exercise_pk>/', views.deleteExercise, name='deleteexercise'),
    path('plan/delete/dailyplan/meal/<int:meal_pk>/', views.deleteMeal, name='deletemeal'),

    path('client/card/<int:pk>/', views.clientCardDetail, name='clientCardDetail'),
    path('offer/<int:pk>/handle/', views.handleResponse, name='handleResponse'),
    path('trainer/cards/', views.card_list, name='card_list'),
    path('trainer/card/<int:pk>/', views.trainerCardDetail, name='trainerCardDetail'),
    path('trainer/card/<int:card_pk>/respond/', views.create_response, name='create_response'),
    path('trainer/portfolio/<int:trainer_id>/', views.portfolio, name='portfolio'),
    path('trainer/portfolio/<int:trainer_id>/edit/', views.editPortfolio, name='editPortfolio'),
]