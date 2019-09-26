from django.urls import path

from training.views import Train, TrainingForm

urlpatterns = [
    path('', Train.as_view(), name='training'),
    path('training_form', TrainingForm.as_view(), name='training_form')
]