from django.db import models
# Create your models here.
from django.contrib.postgres.fields import ArrayField


class Book(models.Model):
    isbn = models.IntegerField(unique=True)
    # https://docs.djangoproject.com/en/3.1/ref/forms/widgets/#django.forms.DateTimeInput 포맷으로 인풋
    registered_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'book'
        ordering = ['isbn']


class RecommendedBook(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_query_name='recommended_book')
    # array field로 나중에 바꿔라.
    is_recommended = models.BooleanField(default=False)
    able_to_borrow = models.BooleanField(default=True)

    class Meta:
        db_table = 'recommended_book'


class UserModel(models.Model):
    kakao_id = models.IntegerField(unique=True)
    g_school_nickname = models.CharField(max_length=3, default='')
    kakao_nickname = models.CharField(max_length=20, default='')
    profile_image = models.CharField(max_length=200, default='')
    is_manager = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        db_table = 'users'
        ordering = ['kakao_id']


class BookInfo(models.Model):
    # https://brunch.co.kr/@ddangdol/10 로 쿼리
    # https://developers.kakao.com/docs/latest/ko/daum-search/dev-guide#search-book api
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE, primary_key=True, related_query_name='book')
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    thumbnail_image = models.CharField(max_length=200)
    publisher = models.CharField(max_length=25)
    page = models.IntegerField()
    published_date = models.DateTimeField()
    keyword = ArrayField(models.CharField(max_length=30))
    subtitle = models.CharField(max_length=25)
    description = models.CharField(max_length=100)
    purchase_link = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'book_info'


class LoveBook(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_query_name='loved_book')
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_query_name='lover')

    class Meta:
        db_table = 'book_loved'


class BorrowBooks(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_query_name='borrower')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_query_name='book')
    borrowed_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True)
    is_overdue = models.BooleanField(default=False)

    class Meta:
        db_table = 'book_present_condition'


class BookComment(models.Model):
    # from django.db.models import Avg
    # >>> Book.objects.all().aggregate(Avg('price')) 로 별점 평균 구하라
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_query_name='commenter')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_query_name='book')
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=20)

    class Meta:
        db_table = 'book_comment'


class RequestedBook(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_query_name='requested_user')
    book_title = models.CharField(max_length=25)
    author = models.CharField(max_length=25)
    interest_parts = models.CharField(max_length=25)
    others = models.CharField(max_length=30)

    class Meta:
        db_table = 'requested_book'
