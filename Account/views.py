from django.shortcuts import render
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from .serializer import AccountCreateSerializer
from django.contrib.auth.models import User
from .models import Relation
from .forms import AccountForm
from .models import Account
# Create your views here.

def home_view(request,*args,**kwargs):
    return render(request,'index.html')

def register_web_view(request,*args,**kwargs):
    form=AccountForm(request.POST or None)
    context={
        'form':form
    }
    if form.is_valid():
        form.save()
        print(type(form.cleaned_data['user']))
    return render(request,'reg.html',context)

@api_view(['POST'])
def register_view(request,*args,**kwargs):
    username = request.data['username']
    password = request.data['password']
    email = request.data['email']

    try:
        user = User.objects.create_user(username, email, password)
        acct = Account.objects.create(user=user, AccountType='pub')
    except Exception as err:
        print(err)
        context={'message':'Something went wrong with your request'}
        return Response(context)
    context={
    'respond':f"Your Account {user.username} has been created"
    }
    return Response(context)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def follow_view(request,*args,**kwargs):

    user2 = request.data['follower']

    try:
        user_now = Account.objects.filter(user=request.user).first()
        #print("usernow*** ",user_now.user)
        follower_now = User.objects.filter(username=user2).first()
        #print("foll  ",follower_now.username)
        rel_exist = Relation.objects.filter(Q(user=user_now) & Q(follower=follower_now))
        #print("rel ex ",rel_exist)
        Acct_user2 = Account.objects.filter(user=follower_now).only('AccountType').first()
        #print("Acct ",Acct_user2.AccountType)
    except Exception as err:
        print(err)
        context = {'message': 'Something went wrong with your request'}
        return Response(context)
    context={'response':'You already follow this user/ you have already sent a request'}
    #print(len(rel_exist))
    if len(rel_exist)==0 and Acct_user2.AccountType == 'pub':
        #print('working*****###')
        Relation.objects.create(user=user_now, follower=follower_now, isFollower=True)
        context={'response':f"You have requested to Follow {follower_now}"}
    return Response(context)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def requestList_view(request,*args,**kwargs):

    try:
        follow_requests = Relation.objects.filter(Q(user=request.user) & Q(isFollower=False)).only('isFollower')
    except Exception as err:
        print(err)
        context = {'message': 'Something went wrong with your request'}
        return Response(context)

    return Response(follow_requests)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def followersList_view(request, *args, **kwargs):
    try:
        user_now = Account.objects.filter(user=request.user).first()
        print(type(user_now))
        followers = Relation.objects.filter(Q(user=user_now) & Q(isFollower=True)).only('isFollower')
        print(followers)
        context = serializers.serialize('json',followers)
    except Exception as err:
        print(err)
        context = {'message': 'Something went wrong with your request'}
        return Response(context)

    return Response(context)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def accept_view(request,*args,**kwargs):
    requester = request.data['requester']
    try:
        user_now = Relation.objects.filter(Q(user=request.user) & Q(follower=requester))
        user_now.isFollower = True
        context = {'response': f"You have accepted {requester}'s Follow request"}
        return Response(context)
    except Exception as err:
        print(err)
        context = {'message': 'Something went wrong with your request'}
        return Response(context)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def unfollow_view(request,*args,**kwargs):

    follower = request.data['follower']

    try:
        user_now = Account.objects.filter(user=request.user).first()
        print("***")
        unfollower = User.objects.filter(username=follower).first()
        print("###")
        unfollower = Relation.objects.filter(Q(user=user_now) & Q(follower=unfollower))
        print("$$$")
        unfollower.delete()
        context = {'response': f"You have unfollowed {follower}"}
        return Response(context)

    except Exception as err:
        print(err)
        context = {'message': 'Something went wrong with your request'}
        return Response(context)