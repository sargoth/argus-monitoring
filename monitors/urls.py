from django.urls import path, include

from monitors import views

app_name = 'monitors'

urlpatterns = [
    path('tags/', include([
        path('', views.TagListView.as_view(), name='list_tags'),
        path('create/', views.TagCreateView.as_view(), name='create_tag'),
        path('<int:pk>/edit/', views.TagUpdateView.as_view(), name='edit_tag'),
        path('<int:pk>/delete/', views.TagDeleteView.as_view(), name='delete_tag')
    ])),
    path('', include([
        path('', views.MonitorListView.as_view(), name='list_monitors'),
        path('create/', views.MonitorCreateView.as_view(), name='create_monitor'),
        path('<int:pk>/', include([
            path('', views.MonitorDetailView.as_view(), name='detail_monitor'),
            path('edit/', views.MonitorUpdateView.as_view(), name='edit_monitor'),
            path('delete/', views.MonitorDeleteView.as_view(), name='delete_monitor')
        ]))
    ]))
]
