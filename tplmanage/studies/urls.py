from django.urls import path
from . import views
from .views import StudiesHome, StudyDetail, StudyUpdate, CreateStudy, SampleUpdate, SampleDetail, MetricsCharts, ResultCharts

app_name = 'studies'
urlpatterns = [
    path('home/', views.index, name='home'),
    path('studies/', StudiesHome.as_view(), name='study-home'),
    path('studies/<pk>/detail/', StudyDetail.as_view(), name='study-detail'),
    path('studies/sample/<pk>/detail', SampleDetail.as_view(), name='sample-detail'),
    path('studies/create/', CreateStudy.as_view(), name='study-create'),
    path('studies/<pk>/update/', StudyUpdate.as_view(), name='study-update'),
    path('studies/sample/<pk>/update/', SampleUpdate.as_view(), name='sample-update'),
    path('studies/metrics', MetricsCharts.as_view(), name='metrics'),
    path('studies/trends', ResultCharts.as_view(), name='trends')

]