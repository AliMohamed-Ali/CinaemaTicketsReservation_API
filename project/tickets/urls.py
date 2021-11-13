from django.urls import path, include
from .views import no_rest_no_model, no_rest_from_model, FBV_List, FBV_pk, CBV_List, CBV_pk, mixins_list, mixins_pk,\
    viewsets_movie, viewsets_reservation,generics_list, generics_pk, viewsets_guest,find_movie,new_reservation
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests', viewsets_guest)
router.register('movie', viewsets_movie)
router.register('reservation', viewsets_reservation)

urlpatterns = [
    path('', no_rest_no_model, name='no_rest_no_model'),
    path('model_no_rest/', no_rest_from_model, name='no_rest_from_model'),
    path('rest/fbv/', FBV_List, name='rest-fbv'),
    path('rest/fbv/<int:pk>', FBV_pk, name='rest-fbv'),
    path('rest/cbv/', CBV_List.as_view(), name='rest-cbv'),
    path('rest/cbv/<int:pk>', CBV_pk.as_view(), name='rest-cbv'),
    path('rest/mixins/', mixins_list.as_view(), name='rest-mixins'),
    path('rest/mixins/<int:pk>', mixins_pk.as_view(), name='rest-mixins'),
    path('rest/generics/', generics_list.as_view(), name='rest-generics-list'),
    path('rest/generics/<int:pk>', generics_pk.as_view(), name='rest-generics-pk'),
    path('rest/viewsets/', include(router.urls)),
    path('fbv/find-movie/',find_movie ),
    path('fbv/new-reservation/',new_reservation ),
]
