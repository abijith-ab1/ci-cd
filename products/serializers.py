from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'sku']
        extra_kwargs = {
            'sku': {'required': False} 
        }