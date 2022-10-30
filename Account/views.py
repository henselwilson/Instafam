from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import AccountCreateSerializer
from django.contrib.auth.models import User
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
    

    user = User.objects.create_user(username, email, password)
    acc = Account.objects.create(user=user)
    data={
        'user':user,
        'AccountType':'pub'
    }
    serializer = AccountCreateSerializer(data=data)
    return Response(data)

