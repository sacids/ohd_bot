from django.urls import path
from . import views

app_name = 'threads'

urlpatterns = [
    path('', views.ThreadListView.as_view(), name='lists'),
    path('lists', views.ThreadListView.as_view(), name='lists'),
    path('show/<str:pk>', views.ThreadDetailView.as_view(), name='show'),
    path('create', views.ThreadCreateView.as_view(), name='create'),
    path('edit/<str:pk>', views.ThreadUpdateView.as_view(), name='edit'),
    path('delete/<str:pk>', views.ThreadDeleteView.as_view(), name='delete'),

    path('delete-sub/<str:pk>', views.SubThreadDeleteView.as_view(), name='delete-sub'),
    path('get-lists/<str:thread_id>', views.get_sub_threads, name='sub-thread-lists'), 

    path("list-threads/", views.list_threads, name="list-threads"),
    path("list-responses/", views.list_responses, name="list-responses"),
    path("detail-response/", views.detail_response, name="detail-response"),
    path("create-response", views.create_response, name="create-response"),
    path("edit-response/", views.edit_response, name="edit-response"),
    path("delete-response/", views.delete_response, name="delete-response"),
    
    path('links', views.ThreadLinkListView.as_view(), name='links'),
    path('current-links/', views.current_links, name='current-links'),
    path('link_thread2thread', views.link_thread2thread, name='link-thread2thread'),
    path('link_response2thread', views.link_response2thread, name='link-response2thread'),
    path('link_response2API', views.link_response2API, name='link-response2API'),

    path('delete-link/', views.delete_link, name='delete-link'),
    path('links/delete/<str:pk>', views.ThreadLinkDeleteView.as_view(), name='delete-link'),

    path('privacy-policy',views.privacy_policy, name="privacy-policy")

    
]