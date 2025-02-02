from django.shortcuts import render

# Create your views here.
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *


class ItemListView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        items = Item.objects.all().order_by("-created_at")
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()  # Copy data to modify it safely

        data["user"] = request.user.id

        ad_title = data.get("ad_title", "").strip()
        if ad_title:
            keywords = ", ".join(
                set(ad_title.split())
            )  # Convert set to comma-separated string
            data["keywords"] = keywords

        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ItemDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, *args, **kwargs):
        item = get_object_or_404(Item, id=id)
        serializer = ItemSerializer(item)
        return Response(serializer.data)


class ItemByCategoryView(APIView):
    def get(self, request, category, *args, **kwargs):
        items = Item.objects.filter(category=category).order_by("-created_at")
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
