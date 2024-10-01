from rest_framework import serializers
from .models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = '__all__'


    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)
        new_position = [StockProduct(stock = stock,**position)for position in positions]
        StockProduct.objects.bulk_create(new_position)
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions',[])

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        stock.positions.all().delete()
        new_position = [StockProduct(stock = stock,**position)for position in positions]
        StockProduct.objects.bulk_create(new_position)
        return stock