from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='Home'),
    path('diary/index', (views.Index.as_view()), name='Index'),
    path('diary/create/', (views.CreateDiaryView.as_view()), name='CreateDiary'),
    path('diary/list/', (views.DiariesListView.as_view()), name='DiariesList'),
    path('diary/update/<int:diary_id>', (views.DiaryUpdateView.as_view()), name='UpdateDiary'),
    path('diary/delete/<int:pk>', login_required(views.delete_diary), name='DeleteDiary'),
    path('diary/update/<int:diary_id>/note/create', login_required(views.create_note), name='CreateNote'),
    path('diary/update/<int:diary_id>/note/<int:note_id>/edit', login_required(views.edit_note), name='UpdateNote'),
    path('diary/update/<int:diary_id>/note/<int:note_id>/delete', login_required(views.delete_note), name='DeleteNote'),             
]