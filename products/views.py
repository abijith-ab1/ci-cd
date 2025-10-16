from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404


class ProductListCreateView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'status': 'ok', 'count': products.count(), 'data': serializer.data})


    def post(self, request):
        payload = request.data

        match payload:
            case {'name': str(name), 'price': price}:
                payload['sku'] = str(uuid.uuid4())[:8]
                serializer = ProductSerializer(data=payload)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            case {'sku': str(sku)}:
                try:
                    product = Product.objects.get(sku=sku)
                    serializer = ProductSerializer(product)
                    return Response(serializer.data)
                except Product.DoesNotExist:
                    return Response({'detail': 'Product with SKU not found.'}, status=404)
            case _:
                return Response({'detail': 'Invalid payload shape.'}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=204)