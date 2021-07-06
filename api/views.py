from rest_framework import generics, permissions
from api import serializers
from api.models import Articles
from django.contrib.auth.models import User
from api.permissions import IsOwnerOrReadOnly


class Userlist(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class Userdetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class Articlelist(generics.ListCreateAPIView):
    queryset = Articles.objects.all().order_by('-view')
    serializer_class = serializers.ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class Articledetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articles.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get_queryset(self, **kwargs):
        pk = self.kwargs['pk']
        article = Articles.objects.get(id=pk)
        article.view+=1
        article.save()
        return Articles.objects.all()

class ViewArticleByUserView(generics.ListAPIView):
    serializer_class = serializers.ArticleByUserView
    queryset = Articles.objects.all()
    
    def get_queryset(self,**kwargs):
        userid = self.kwargs['pk']
        print(userid)
        # print(Articles.objects.filter(owner = userid).order_by('-view').query)
        data = Articles.objects.filter(owner = userid).order_by('-view')
        print(data)
        return data



    