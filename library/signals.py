from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BorrowedBook
from django.core.mail import send_mail
@receiver(post_save, sender = BorrowedBook)
def book_returned_notification(sender,instance,**kwargs):
    if instance.returned_date:
        user_email = instance.user.email
        subject = "Book returned notification"
        message = f"The book {instance.book.title} has been returned"
        from_email = "noreply@gmail.com"
        recipient_list =[user_email]
        send_mail(subject, message, from_email, recipient_list,fail_silently= False)
#         send_mail(
#     'Book returned notification',
#     'The book {instance.book.title} has been returned',
#     'sandbox.smtp.mailtrap.io',
#     ['suman1@gmail.com'],
#     fail_silently=False,
# )
