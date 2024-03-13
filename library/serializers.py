from rest_framework import serializers
from .models import Books,BorrowedBook

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'
        
class BorrowedBookSerializer(serializers.ModelSerializer):
    # The book serializer is used for nested serialization
    class Meta:
        model  = BorrowedBook
        fields = ['book','due_date','user']

class ReturnBookSerializer(serializers.ModelSerializer):
    # borrowed_book =BorrowedBookSerializer()
    class Meta:
        model = BorrowedBook
        fields = ['returned_date','user']