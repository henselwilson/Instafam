from django.urls import path
from .views import register_view,register_web_view,follow_view, requestList_view,followersList_view, accept_view, unfollow_view


urlpatterns = [
    path('register',register_view),
    path('reg',register_web_view),
    path('follow',follow_view),
    path('pending_requests',requestList_view),
    path('followersList',followersList_view),
    path('acceptrequest',accept_view),
    path('unfollow',unfollow_view),

]