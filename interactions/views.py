from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from users.models import Connect

class ExistingConnections(LoginRequiredMixin, View): 

    template_name = 'interactions/connections.html'

    def get(self, request, *args, **kwargs): 

        try: 
            connections = Connect.objects.all().filter(
                user=request.user
            ).filter(
                connected=True 
            )

        except: 
            connections = None 

        context = {
            'connections': connections,
        }

        return render(request, self.template_name, context=context)    