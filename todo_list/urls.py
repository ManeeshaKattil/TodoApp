from django.urls import path
from . import views

urlpatterns = [
    # ── LOGIN / LOGOUT ──
    path('login_get/', views.login_get, name='login_get'),
    path('login_post/', views.login_post, name='login_post'),
    path('logout_get/', views.logout_get, name='logout_get'),

    # ── REGISTER ──
    path('register_get/', views.register_get, name='register_get'),
    path('register_post/', views.register_post, name='register_post'),

    # ── HOME ──
    path('home_get/', views.home_get, name='home_get'),

    # ── PROFILE ──
    path('view_profile/', views.view_profile, name='view_profile'),
    path('edit_profile_get/', views.edit_profile_get, name='edit_profile_get'),
    path('edit_profile_post/', views.edit_profile_post, name='edit_profile_post'),

    # ── TASKS ──
    path('view_tasks_get/', views.view_tasks_get, name='view_tasks_get'),
    path('view_tasks_post/', views.view_tasks_post, name='view_tasks_post'),

    # ── ADD TASK ──
    path('add_task_get/', views.add_task_get, name='add_task_get'),
    path('add_task_post/', views.add_task_post, name='add_task_post'),

    # ── EDIT TASK ──
    path('edit_task_get/<int:task_id>/', views.edit_task_get, name='edit_task_get'),
    path('edit_task_post/', views.edit_task_post, name='edit_task_post'),

    # ── DELETE TASK ──
    path('delete_task/<id>', views.delete_task),

]