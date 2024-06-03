from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import date
from django.db.models import Q


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "username": user.username,
                "email": user.email,
                "parent_type": user.profile.parent_type
            }
        }, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this profile.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this profile.")
        instance.delete()

class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Child.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this child.")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this child.")
        instance.delete()

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this blog.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this blog.")
        instance.delete()

class VlogViewSet(viewsets.ModelViewSet):
    queryset = Vlog.objects.all()
    serializer_class = VlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vlog.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this vlog.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this vlog.")
        instance.delete()

class HomeFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get_age_group(self, child):
        today = date.today()
        age = (today - child.date_of_birth).days // 365
        if age <= 1:
            return '0-1'
        elif age <= 3:
            return '1-3'
        elif age <= 7:
            return '3-7'
        elif age <= 10:
            return '7-10'
        else:
            return 'all'

    def get(self, request, *args, **kwargs):
        user = request.user
        
        children = Child.objects.filter(user=user)

        blogs = Blog.objects.none()
        vlogs = Vlog.objects.none()

        if children.exists():
            for child in children:
                age_group = self.get_age_group(child)
                gender = child.gender

                blogs = blogs | Blog.objects.filter(Q(age_group=age_group) | Q(gender=gender), status=True)
                vlogs = vlogs | Vlog.objects.filter(Q(age_group=age_group) | Q(gender=gender), status=True)        
        else:
            blogs = Blog.objects.filter(status=True)
            vlogs = Vlog.objects.filter(status=True)

        blog_serializer = BlogSerializer(blogs, many=True)
        vlog_serializer = VlogSerializer(vlogs, many=True)

        return Response({
            'blogs': blog_serializer.data,
            'vlogs': vlog_serializer.data,
        })

class DetailVlogBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        vlog_id = request.query_params.get('vid')
        blog_id = request.query_params.get('bid')

        if vlog_id:
            vlog = get_object_or_404(Vlog, id=vlog_id)
            response_data = VlogSerializer(vlog).data
            return Response(response_data, status=status.HTTP_200_OK)

        if blog_id:
            blog = get_object_or_404(Blog, id=blog_id)
            response_data = BlogSerializer(blog).data
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({'detail': 'Missing vlog or blog ID'}, status=status.HTTP_400_BAD_REQUEST)