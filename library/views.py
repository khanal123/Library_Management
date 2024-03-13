from rest_framework import generics, permissions, status
from django.utils import timezone
from django.db.models import F
import time

from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Books, BorrowedBook
from .serializers import BookSerializer, BorrowedBookSerializer, ReturnBookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .filter import BookFilter
from .utils import accessfunction
from .decorators import loginrequired
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from User_Profile.models import MyUser


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer

class BorrowBookView(APIView):
    serializer_class = BorrowedBookSerializer
    # permission_classes = [IsAuthenticated]
    # @loginrequired()
    def get(self,request,*args,**kwargs):
        userid = request.user.id
        try:
            # Retrieve the user instance based on the user id
            # user = MyUser.objects.get(pk = userid)
            # Retrieve a list of borrowed books for the specified user
            # borrowed_books = BorrowedBook.objects.filter(user = user)
            borrowed_books = BorrowedBook.objects.all()
            # Serialize the data
            serializer = self.serializer_class(borrowed_books, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except MyUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request, *args, **kwargs):
        userid = accessfunction(self.request)
        print(request.data)

        book_id = request.data.get('book')
        if not book_id:
            return Response({'error': 'Book ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ensure book_id is cast to integer
            book = Books.objects.get(id=book_id)
            print(f'bookbookbookbookbook{book}')
        except (ValueError, Books.DoesNotExist):
            return Response({'error': 'Invalid Book ID or Book not found'}, status=status.HTTP_404_NOT_FOUND)

        quantity_value = book.quantity
        print(f'Book quantity: {quantity_value}, type: {type(book.quantity)}')  

        # Use book.quantity directly in the comparison
        user = MyUser.objects.get(id = request.data['user'])
        if book.quantity > 0:
            print(type(request.data['user']))
            borrowed_book = BorrowedBook.objects.create(
                user=user,
                book=book,
                due_date=timezone.now() + timezone.timedelta(days=14)
            )
            # Update the book quantity
            book.quantity -= 1
            book.save()

            return Response({'message': f'Book "{book.title}" borrowed successfully'})
        
        return Response({'error': f'Book "{book.title}" is out of stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        # if userid:
        #     serializer = BorrowedBookSerializer(data= request.data)
        #     print(request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(
        #             {
        #             "success":True,
        #         }, status= status.HTTP_201_CREATED
        #         )
            
        #     return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        # return Response({'success':False}, status= status.HTTP_401_UNAUTHORIZED)
        # serializer.save(user=self.request.user)
    

# class BorrowBookView(generics.CreateAPIView):
#     serializer_class = BorrowedBookSerializer
    

#     def create(self, serializer, request):
#         userid = accessfunction(self.request)
#         print(userid)
#         serializer.save(user=self.request.user)
        
    
    

class ReturnBookView(generics.UpdateAPIView):
    queryset = BorrowedBook.objects.all()
    serializer_class = ReturnBookSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # @loginrequired


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # due_date = request.data['due_date']
        returned_date = request.data['returned_date']
        returned_date = datetime.strptime(returned_date, '%Y-%m-%d')
        due_date = datetime.strptime(str(instance.due_date), '%Y-%m-%d')
        # print(f'dueeeee     {due_date}')
        fine_amount = 0
        try:
   

            print(due_date)
            if returned_date > due_date:
                days_late = (returned_date - due_date).days
                # fine is 15 rupees per day
                fine_amount = days_late * 15
                # Update the returned_date in the BorrowedBook instance
                instance.returned_date = returned_date
                instance.save()
                return Response({'fine_amount': fine_amount})
            return Response({'no fine '})
        except ValueError as e:
             # Handle the parsing error
            return Response({'error': f'Error parsing returned_date: {str(e)}'})



    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     due_date= timezone.now()

    #     returned_date = instance.returned_date
    #     fine_amount = 0

    #     # newdate1 = time.strptime(due_date, "%d/%m/%Y")
    #     # newdate2 = time.strptime(returned_date, "%d/%m/%Y")

    #     if returned_date > due_date:
    #         print('yetassssssssssssssssssssssssssssss')
    #         days_late = (instance.returned_date - instance.due_date).days
    #         print(days_late)
    #         # fine is 5 rupeees 
    #         fine_amount = days_late * 5 
    #         return Response({'fine_amount': fine_amount})
    #     return Response({'fine_amount': 0})  # No fine if returned on or before the due date
            
            # instance.user.profile.balance -= fine_amount

            
        # instance.save()
        # serializer = self.get_serializer(instance)
        # return Response(serializer.data)