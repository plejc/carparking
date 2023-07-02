from django.urls import path
from . import views


urlpatterns = [
    path("parking-list/", views.ParkingListView.as_view()),
    path("request-parking/", views.RequestParkingView.as_view()),
    path("booked-parking-view/", views.BookedParkingView.as_view(), name='booked_parking_view'),
    path("booked-parking-detail/", views.BookedParkingDetailView.as_view()),
]