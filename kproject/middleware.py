# kproject/middleware.py

from datetime import datetime, timedelta
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Only logged in users will have a session
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            now = datetime.now()

            if last_activity:
                last_activity = datetime.strptime(last_activity, "%Y-%m-%d %H:%M:%S.%f")
                elapsed_time = (now - last_activity).seconds
                if elapsed_time > 30:
                    messages.success(request,"您已30秒無活動,請重新登入!")
                    logout(request)
            # Update the last activity timestamp
            request.session['last_activity'] = now.strftime("%Y-%m-%d %H:%M:%S.%f")
