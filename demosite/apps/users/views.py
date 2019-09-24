from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

class LoginView(View):
	def get(self, request):
		request.session['login_reference_page'] = request.META.get("HTTP_REFERER", '/')
	    return render(request, "user/login.html")

def user_logout(request):
	logout(request)
	return redirect(request.META.get('HTTP_REFERER', '/'))