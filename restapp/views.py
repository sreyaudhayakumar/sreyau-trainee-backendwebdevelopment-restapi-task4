from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import UserRegistration
from .serializer import UserRegistrationSerializer,UserLoginSerializer,UserRegistrationUpdateSerializer, UserRegistrationDeleteSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Q
from rest_framework.filters import OrderingFilter
from django.utils import timezone


class UserRegistrationCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

 
class UserLogin(APIView):
    permission_classes = [AllowAny]
 
 
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
           
            if user is not None:
        
                user.last_login = timezone.now()
                user.save() 
 
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 


class UserRegistrationList(APIView):
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
    filter_backends = [OrderingFilter]  

    def get_queryset(self):
        query = self.request.query_params.get('q', '')  
        queryset = UserRegistration.objects.filter(
            Q(username__icontains=query) |  
            Q(email__icontains=query) | 
            Q(age__icontains=query) |  
            Q(role__name__icontains=query) 
        )

        min_age = self.request.query_params.get('min_age')
        max_age = self.request.query_params.get('max_age')
        if min_age:
            queryset = queryset.filter(age__gte=min_age)
        if max_age:
            queryset = queryset.filter(age__lte=max_age)
            

        ordering = self.request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        paginator = self.pagination_class()  
        results = paginator.paginate_queryset(queryset, request)  
        serializer = UserRegistrationSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

class UserRegistrationUpdate(APIView):
    def put(self, request, pk):
        user = UserRegistration.objects.get(pk=pk)
        serializer = UserRegistrationUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = UserRegistration.objects.get(pk=pk)
        serializer = UserRegistrationUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationDelete(APIView):
    def delete(self, request, pk=None):
        # Delete by ID
        if pk:
            try:
                user = UserRegistration.objects.get(pk=pk)
                user.delete()
                return Response({'message': 'User deleted successfully'})
            except UserRegistration.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    
        serializer = UserRegistrationDeleteSerializer(data=request.data)
        if serializer.is_valid():
            ids = serializer.validated_data['ids']
            users = UserRegistration.objects.filter(id__in=ids)
            users.delete()
            return Response({'message': 'Users deleted successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)