# from django.db import DatabaseError
# from django.shortcuts import render

# class DatabaseErrorMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         try:
#             response = self.get_response(request)
#         except DatabaseError:
#             response = render(request, 'pages/db_error.html', status=500)
#         return response
