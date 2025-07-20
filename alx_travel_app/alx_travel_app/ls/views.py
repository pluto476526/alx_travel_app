from django.shortcuts import render

# Create your views here.



from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def index(request):
    """
    Basic API endpoint for listings
    """
    return Response({
        'message': 'Welcome to ALX Travel App API',
        'version': 'v1',
        'app': 'listings'
    })