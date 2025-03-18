# -*- coding: utf-8 -*-
from random import randint

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse
from userapp.models import UserInfo


class RegisterView(View):
    def get(self, request):
        # Return the registration page
        return render(request, 'register.html')

    def post(self, request):
        try:
            # Get the account and password from the POST request
            account = request.POST.get('account')
            pwd = request.POST.get('password')

            # Ensure both account and password are provided
            if account and pwd:
                userid = f"{account}{randint(100, 999)}"

                # Check if the user already exists
                if UserInfo.objects.filter(uname=account).exists():
                    data = {
                        'code': '409',
                        'isCertified': False,
                        'message': 'Account already exists!'
                    }
                    return JsonResponse(data=data, safe=False)

                # Create a new user and save it to the database
                user = UserInfo.objects.create(uname=account, pwd=pwd, userid=userid)

                # If user is successfully created, store the user in the session
                if user:
                    request.session['user'] = {'id': user.id, 'uname': user.uname}
                    data = {
                        'data': {'id': user.id, 'uname': user.uname, 'userid': user.userid},
                        'code': '200',
                        'isCertified': True,
                        'message': 'Account created successfully!'
                    }
                else:
                    data = {
                        'code': '406',
                        'isCertified': False,
                        'message': 'Account creation failed!'
                    }
            else:
                data = {
                    'code': '400',
                    'isCertified': False,
                    'message': 'Account or password missing!'
                }

        except Exception as e:
            # Handle any unexpected errors
            data = {
                'code': '500',
                'isCertified': False,
                'message': f'Error occurred: {str(e)}'
            }

        return JsonResponse(data=data, safe=False)


class CenterView(View):
    def get(self, request):
        # Render the user center page
        return render(request, 'center.html')
