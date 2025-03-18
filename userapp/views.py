# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View

from userapp.models import UserInfo


class RegisterView(View):
    def get(self, request):
        # Return the registration page
        return render(request, 'register.html')

    def post(self, request):
        # Get the account and password from the POST request
        account = request.POST.get('account')
        pwd = request.POST.get('password')

        # Ensure both account and password are provided
        if account and pwd:
            # Create a new user and save it to the database
            user = UserInfo.objects.create(uname=account, pwd=pwd)

            # If user is successfully created, store the user in the session
            if user:
                request.session['user'] = user
                return HttpResponseRedirect('/user/center/')
        # If registration failed, redirect back to the registration page
        return HttpResponseRedirect('/user/register/')


class CenterView(View):
    def get(self, request):
        # Render the user center page
        return render(request, 'center.html')
