from django.urls import path
from . import views


urlpatterns = [

    # ----------- Blocks and Transitions ----------
    path('blocks/', views.BlockViewSet.as_view({'get': 'list', 'post': 'create'}), name='block-list'),
    path('blocks/<str:pk>/', views.BlockViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='block-detail'),

    path('transitions/', views.TransitionViewSet.as_view({'get': 'list', 'post': 'create'}), name='transition-list'),
    path('transitions/<str:pk>/', views.TransitionViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='transition-detail'),

    # ----------- History ----------
    path('block-history/<str:pk>/', views.BlockHistory.as_view({'get': 'retrieve'})),
    path('comment-history/<str:pk>/', views.CommentHistory.as_view({'get': 'retrieve'})),

    # ---------- Comment -----------
    path('comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments'),
    path('comments/<str:pk>/', views.CommentViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update',
                                                             'delete': 'destroy'}), name='comment-detail'),

    ]
