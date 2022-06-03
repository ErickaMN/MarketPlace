from django.db.models import Q
from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from movies import serializers
from movies.models import Genre, Movie, Comment, Likes
from movies.serializers import GenreSerializer, MovieSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.AllowAny,)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    # serializer_class = MovieSerializer
    # permission_classes = (permissions.IsAdminUser,)
    # queryset = Movie.objects.all()
    # serializer_class = serializers.MovieSerializer
    # filter_backends = (DjangoFilterBackend)
    # filterset_fields = ('genre',)
    # search_fields = ('title',)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q))
        serializer = MovieSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'search', 'genre']:
            return [permissions.AllowAny(),]
        else:
            return [permissions.IsAdminUser(),]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.MovieSerializer
        else:
            return serializers.MovieSerializer



    @action(detail=False, methods=['get'])
    def genre(self, request, ):
        queryset = self.get_queryset()
        queryset = queryset.filter(genre=self.genre)
        serializer = MovieSerializer(queryset, many=True, request=request)
        return Response(serializer.data)

    # @action(detail=False, methods=['get'])
    # def genres(self, request, pk=None):
    #     genres = request.query_params.get('genres')
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(Q(genre__icontains=genres))
    #     serializer = MovieSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #api/v1/posts/<id>/comments/
    @action(['GET'], detail=True)
    def comments (self, request, pk):
        post = self.get_object()
        comments = post.comments.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response (serializer.data)

    #api/v1/posts/<id>/add_to_likes/
    @action(['POST'], detail=True)
    def add_to_liked (self, request, pk):
        post = self.get_object()
        if request.user.liked.filter(post=post).exists():
           # request.user.liked.filter(post=post).delete():
            return Response('Вы уже лайкали этот пост', status=status.HTTP_400_BAD_REQUEST)
        Likes.objects.create(post=post, user=request.user)
        return Response('Вы поставили лайк', status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True)
    def remove_from_liked(self, request, pk):
        post = self.get_object()
        if not request.user.liked.filter(post=post).exists():
            return Response('Вы не лайкали пост', status=status.HTTP_400_BAD_REQUEST)
        request.user.liked.filter(post=post).delete()
        return Response('Ваш лайк удален', status=status.HTTP_204_NO_CONTENT)

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)







