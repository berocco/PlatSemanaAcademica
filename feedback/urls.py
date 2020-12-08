from django.urls import path
import feedback.views as views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    
    path("ver/", login_required(views.allfeedbacks), name='feedbacks'),
    
    path("", login_required(views.CreateFeedback), name='feedbacksAdd'),

    path('criar/', login_required(views.QuestaoCreateView.as_view()), name='createFeedQuestion'),
    path('editar/<int:pk>', login_required(views.QuestaoUpdateView.as_view()), name='editFeedQuestion'),
    path('deletar/<int:pk>', login_required(views.QuestaoDeleteView.as_view()), name='deleteFeedQuestion'),

    path('perguntas/', login_required(views.questionsAll), name='feedbackQuestions'),

]