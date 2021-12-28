from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class CheckHoTen(object):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        return self.get_response(request)
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path != reverse('haystack_search'):
            # Get the view name as a string
            view_name = '.'.join((view_func.__module__, view_func.__name__))
        
            # If the view name is in our exclusion list, exit early
            exclusion_set = getattr(settings, 'EXCLUDE_FROM_MY_MIDDLEWARE')
            if not view_name in exclusion_set:
                if request.user.is_authenticated:
                    if request.user.HoTen == "":
                        while not (request.path == reverse('UpdateInfo')):
                            return redirect(reverse('UpdateInfo'))
            else:
                print('----- Middleware view %s' % view_func.__name__)

