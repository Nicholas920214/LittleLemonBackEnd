from django.urls import path, include
from . import views

# for viewset, later inspect on
# for API root
from rest_framework.routers import DefaultRouter

router: DefaultRouter = DefaultRouter()
router.register(r"tables", views.BookingViewSet)


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("book/", views.book, name="book"),
    path("reservations/", views.reservations, name="reservations"),
    path("menu/", views.menu, name="menu"),
    path("menu_item/<int:pk>/", views.display_menu_item, name="menu_item"),
    path("bookings/", views.bookings, name="bookings"),
    # API paths
    path("api/menu", views.MenuItemsView.as_view(), name="api"),
    path("api/menu/<int:pk>", views.SingleMenuItemView.as_view(), name="api"),
    path("api/booking", include(router.urls), name="api"),
]
