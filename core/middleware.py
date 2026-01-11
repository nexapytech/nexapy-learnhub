from django.http import HttpResponseForbidden

class BlockCopierMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define a list of known website copier user-agents
        forbidden_agents = ['HTTrack', 'WebCopier', 'Wget', 'curl']

        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

        # Check if user-agent matches any known website copiers
        if any(agent.lower() in user_agent for agent in forbidden_agents):
            return HttpResponseForbidden("Access Denied")

        # Proceed with request
        return self.get_response(request)