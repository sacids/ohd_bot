from django.urls import path
from . import views

app_name = 'threads'

urlpatterns = [
    path('lists', views.ThreadListView.as_view(), name='lists'),
    path('show/<str:pk>', views.ThreadDetailView.as_view(), name='show'),
    path('create', views.ThreadCreateView.as_view(), name='create'),
    path('edit/<str:pk>', views.ThreadUpdateView.as_view(), name='edit'),
    path('delete/<str:pk>', views.ThreadDeleteView.as_view(), name='delete'),

    path('delete-sub/<str:pk>', views.SubThreadDeleteView.as_view(), name='delete-sub'),

    path('get-lists/<str:thread_id>', views.get_sub_threads, name='sub-thread-lists'), 
    
    path('links', views.ThreadLinkListView.as_view(), name='links'),
    path('links/delete/<str:pk>', views.ThreadLinkDeleteView.as_view(), name='delete-link'),

    path('privacy-policy',views.privacy_policy, name="privacy-policy")

    
]