from django.http import HttpResponse
from django.shortcuts import render_to_response
from visitors.models import visitorToken, session
from django.contrib.auth import authenticate, login
from django.template import RequestContext, loader
import datetime
import uuid
import math
#from django.utils.timezone import utc
from django.contrib.auth import logout

diff_requests_error=600
visitor_netwrk_error=0
#Expiry Time is 60 min
expiry_period=3600

#Called when token creation view is requested
def windowUserLogin(request):
    if request.method == 'POST': 
       input_user= request.POST['username']
       password= request.POST['password']
       window_user = authenticate(username=input_user,password=password)
       if window_user is not None:
          login(request, window_user)
          return HttpResponse('Success')
       else:
          return HttpResponse('Authenticate Fail') 
    else: 
       return HttpResponse('Enter Username and Password')

def windowUserLogout(request):
    logout(request)
    return HttpResponse('You have successfully logged out')


#Called When Token Creation view is requested
def tokenCreate(request):   
	if request.user.is_authenticated():
		token_museumID=request.user.get_profile().museum
		mod = token_museumID.id/10
		if mod:
			digits=0
		else:
			digits=1

		if digits==1:
			museumID_2bits="%s%d" % ('0',token_museumID.id)
		else:
			museumID_2bits="%d" % (token_museumID.id)
		#Intialisation of vToken_exit.
		generate_token_exit=1
		while generate_token_exit!=0: 
			randomNumber=str(uuid.uuid1()).split('-')[0][:4]
			generate_token="%s%s" % (museumID_2bits,randomNumber)
			try:
				token_obj=visitorToken.objects.get(visitorToken=generate_token)
			except visitorToken.DoesNotExist:
				token_obj=None
			#Token Check:Generated TokenID doesnt exists in the visitorToken table
			if token_obj==None:
				generate_token_exit=0 
				time_now=datetime.datetime.utcnow()
				time_created=time_now
				token_expiry_time=time_now+datetime.timedelta(seconds=expiry_period)
				token1=visitorToken.objects.create(visitorToken=generate_token,museum=token_museumID,time_created=time_created,token_expiry_time=token_expiry_time)
			else:
				time_now=datetime.datetime.utcnow()
				if token_obj.token_expiry_time < time_now:
					active_session.delete()
					requestToken_Obj.delete()
					generate_token_exit=0 
					time_created=time_now
					token_expiry_time=time_now+datetime.timedelta(seconds=expiry_period)
					token1=visitorToken.objects.create(visitorToken=generate_token,museum=token_museumID,time_created=time_created,token_expiry_time=token_expiry_time)
			
		return HttpResponse(generate_token)
	else:
		return HttpResponse('You are not authorised to create Token')
      
      

#Called when visitor login view is requested
def visitorLogin(request):
	#Current DateTime with timezone supported
	time_now=datetime.datetime.utcnow()
	if request.method == 'POST': 
		input_token = request.POST['token']
		try: 
			loginToken_Obj=visitorToken.objects.get(visitorToken=input_token)
		except visitorToken.DoesNotExist: 
			loginToken_Obj=None
		if loginToken_Obj is not None:
			if loginToken_Obj.token_expiry_time < time_now:
				active_session.delete()
				requestToken_Obj.delete()
				return HttpResponse("Token Expired")
			
			active_sessions=session.objects.filter(visitortoken=input_token).count()
			#First time login
			if active_sessions == 0:
				loginToken_Obj.login_time=time_now
				loginToken_Obj.save()
				key = str(uuid.uuid4()).replace('-','')
				session.objects.create(visitortoken=loginToken_Obj,last_request_time=time_now,key=key) #Starting Session
				return HttpResponse(key)
			#Session Already Exist
			else:
				active_session=session.objects.get(visitortoken=input_token)
				#User login after network prolem 
				if (time_now-active_session.last_request_time).seconds >=diff_requests_error:
					active_session.last_request_time=time_now
					active_session.save()
					return HttpResponse(key)
				else:
					return HttpResponse("Someone is already using this token")	
		else:
			return HttpResponse("Invalid Token")			
	else:
		return HttpResponse("Enter Token ID ")	


#Called when visitor requests for a museum item after login  
# def processRequest(request):
    # key=request.POST['key']  #Using XML or requests.token, we can extract token_id
	# active_session = session.objects.get(key=key)
	
	# if active_session is None:
		# return HttpResponse("Invalid Request")
			
    # try:
        # requestToken=visitorToken.objects.get(visitorToken=active_session.visitortoken)
    # except visitorToken.DoesNotExist:
        # requestToken=None
    # if requestToken is not None:
		#if the token expiry time is reached
		# if requestToken.token_expiry_time<datetime.datetime.utcnow():
			# active_session.delete()
			# requestToken.delete()
			# return HttpResponse("Your Token has expired.You cant use this token anymore")
          
                  
                  
             
             
             
          
    


