# urls.py
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MessageView

router = DefaultRouter()
router.register(r"messages", MessageView, basename="messages")
router.register(r"chats", ChatViewSet, basename="chats")

urlpatterns = router.urls
