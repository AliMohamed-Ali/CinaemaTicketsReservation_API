from django.shortcuts import render
from django.http.response import JsonResponse, Http404
from rest_framework import status, filters

from .models import Guest, Reservation, Movie
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets


# Create your views here.
# 1- without  rest framework  no model query FBV
def no_rest_no_model(request):
    guest = [
        {
            'id': 1,
            'name': "omar",
            "mobile": 12345
        }, {
            'id': 2,
            'name': "ali",
            "mobile": 12345
        },
    ]

    return JsonResponse(guest, safe=False)


# 2-model no_rest

def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        "guests": list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)


# List ==Get
# Create == post
# pk query == Get
# update == put
# delete == delete

# 3 Function based views
# 3.1 GET
@api_view(['POST', 'GET'])
def FBV_List(request):
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    # PUT
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE

    if request.method == 'DELETE':
        guest.delete()
        return Response(data={'massage': 'Delete is Done'}, status=status.HTTP_204_NO_CONTENT)


# CBV Class based views APIView
# 4.1 list and Create == GET and POST
class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# 4.2 GET PUT DELETE Class based views  ---pk
class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Exception as e:
            print(str(e))
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5 mixins
# 5.1 mixins list
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# 5.2 mixins get put delete

class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.delete(request)


# 6 Generics
# 6.1 get and post
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


# 6.2 put , retrieve ,delete

class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


# 7 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backend = [filters.SearchFilter]
    search_fields = ['movie']


class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


# 8 Find movie
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        movie=request.data['movie'], hall=request.data['hall'])
    serializer = MovieSerializer(movies, many=True)
    return Response(data=serializer.data)
#9 create new reservation
@api_view(['POST'])
def new_reservation(request):
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()
    movie  = Movie.objects.get(
        movie= request.data['movie'],
        hall = request.data['hall']
    )
    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    serializer = ReservationSerializer(reservation)
    return Response(serializer.data , status=status.HTTP_201_CREATED)