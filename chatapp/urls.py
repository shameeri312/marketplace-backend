from .views import MessageView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"messages", MessageView, basename="messages")

urlpatterns = router.urls
