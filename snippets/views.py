from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from snippets.serializers import SnippetSerializer, UserSnippetSerializer
from snippets.models import Snippet
from snippets.permisions import IsOwnerOfSnippetOrReadOnly, IsSameUserOrReadOnly


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def snippet(request, format=None):
    if request.method == "GET":
        data = Snippet.objects.all()
        serializer = SnippetSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        serializer.owner = request.user
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,  status= status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly, IsOwnerOfSnippetOrReadOnly])
def snippet_detials(request, snippet_id, format=None):
    snippet_ = get_object_or_404(Snippet, id=snippet_id)
    if request.method == "GET":
        serializer = SnippetSerializer(snippet_)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = SnippetSerializer(snippet_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        snippet_.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST', "GET"])
def users(request):
    if request.method == "GET":
        serializer = UserSnippetSerializer(User.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = UserSnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', "GET", "DELETE"])
@permission_classes([IsSameUserOrReadOnly])
def user_detail(request, user_id):
    user = get_object_or_404(User, id = user_id)

    if request.method == "GET":
        serializer = UserSnippetSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = UserSnippetSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



### CBV #############################################
class Snippets(APIView):
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=requests.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Snippets_Detials(APIView):
    def get(self, request, pk, format=None):
        snippet_ = get_object_or_404(Snippet, id=pk)
        serializer = SnippetSerializer(snippet_)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk,format=None):
        snippet_ = get_object_or_404(Snippet, id=pk)
        serializer = SnippetSerializer(snippet_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk,format=None):
        snippet_ = get_object_or_404(Snippet, id=pk)
        snippet_.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Snippets_Mixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    ## in Mixin
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class Snippets_Mixin_details(mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class Snippets_Generic(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class Snippets_Generic_Detials(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer



