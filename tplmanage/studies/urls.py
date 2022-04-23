from django.urls import path
from . import views
from .views import StudiesHome, StudyDetail, StudyUpdate, CreateStudy, SampleUpdate

app_name = 'studies'
urlpatterns = [
    path('home/', views.index, name='home'),
    path('studies/', StudiesHome.as_view(), name='study-home'),
    path('studies/<pk>/detail/', StudyDetail.as_view(), name='study-detail'),
    path('studies/create/', CreateStudy.as_view(), name='study-create'),
    path('studies/<pk>/update/', StudyUpdate.as_view(), name='study-update'),
    path('studies/sample/<pk>/update/', SampleUpdate.as_view(), name='sample-update'),
    path('studies/metrics', views.metrics, name='metrics'),
    path('studies/trends', views.trend_data, name='trends')

]