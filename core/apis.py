from ninja import NinjaAPI, Query
from ninja.pagination import paginate, PageNumberPagination
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from core.schema import *

from django.contrib.auth.models import User
from core.models import Category, Transaction, TransactionImage
from typing import List

api = NinjaAPI(
    title="API Keuangan",
    version="1.0.0",
    description="Dokumentasi API untuk aplikasi manajemen keuangan",
)

api.add_router("/auth/", mobile_auth_router)
apiauth = HttpJwtAuth()

@api.get("hello")
def helloapi(request):
    """Sekadar Hello world applikasi"""
    return {"message": "Selamat datang di API manajemen keuangan"}

@api.get('/hello_login', auth=apiauth)
def hello_login(request):
    """Helo yang memastikan mekanisme login berjalan dengan baik"""
    user = User.objects.get(pk=request.user.id)
    return {"message": f"Selamat datang {user.username} di API manajemen keuangan"}

@api.post('/register', response=UserOut)
def register(request, payload: RegisterSchema):
    """Endpoint untuk registrasi user baru"""
    user_reg = User(username=payload.username, 
                    first_name=payload.first_name, 
                    last_name=payload.last_name)
    user_reg.set_password(payload.password)
    user_reg.save()
    return user_reg

@api.get('/profile', auth=apiauth, response=UserOut)
def get_profile(request):
    """Endpoint untuk mendapatkan profil user yang sedang login"""
    user = User.objects.get(pk=request.user.id)
    return user

@api.post('/category', auth=apiauth, response=CategoryOut)
def create_category(request, payload: CategoryIn):
    """Endpoint untuk membuat kategori baru"""
    user = User.objects.get(pk=request.user.id)
    category = Category.objects.create(user=user, name=payload.name) 
    return category

@api.get('/category', auth=apiauth, response=List[CategoryOut])
def list_cateogry(request):
    """Endpoint untuk mendapatkan list kategori untuk user yang sedang login"""
    categories = Category.objects.all()
    print(categories)
    return categories

@api.delete('/category/{category_id}', auth=apiauth)
def delete_category(request, category_id: int):
    """Endpoint untuk menghapus kategori yang telah dibuat"""
    user = User.objects.get(pk=request.user.id)
    category = Category.objects.get(pk=category_id)
    if category.user != user:
        return {"message": "Anda tidak memiliki akses untuk menghapus kategori ini"}
    else:
        category.delete()
        return {"message": "Kategori berhasil dihapus"}
    
@api.post('/transaction', auth=apiauth, response=TransactionOut)
def create_transaction(request, payload: TransactionIn):
    """Endpoint untuk membuat transaksi baru dengan field:
    - category_id: int id kategori
    - amount: int jumlah transaksi
    - description: teks deskripsi transaksi
    - type: string tipe transaksi ['1': pemasukan, '2': pengeluaran]
    - transaction_date: string tanggal transaksi dalam format YYYY-MM-DD
    """
    user = User.objects.get(pk=request.user.id)
    category = Category.objects.get(pk=payload.category_id)
    trans_date = datetime.strptime(payload.transaction_date[:10], '%Y-%m-%d').date()
    transaction = Transaction.objects.create(
        user=user, category=category, amount=payload.amount,
        description=payload.description, type=payload.type,
        transaction_date=trans_date)
    return transaction

@api.get('/transaction', auth=apiauth, response=List[TransactionOut])
@paginate(PageNumberPagination, page_size=50)
def list_transaction(request, filters: TransactionFilter=Query(...)):
    """Endpoint untuk mendapatkan list transaksi untuk user yang sedang login"""
    user = User.objects.get(pk=request.user.id)
    transactions = Transaction.objects.filter(user=user)
    transactions = filters.filter(transactions)
    return transactions

@api.get('/transaction/{transaction_id}', auth=apiauth, response=TransactionOut)
def get_transaction(request, transaction_id: int):
    """Endpoint untuk mendapatkan detail transaksi berdasarkan id"""
    user = User.objects.get(pk=request.user.id)
    transaction = Transaction.objects.get(pk=transaction_id)
    if transaction.user != user:
        return {"message": "Anda tidak berhak mengakses data ini"}
    else:
        return transaction
    
@api.put('/transaction/{transaction_id}', auth=apiauth, response=TransactionOut)
def update_transaction(request, transaction_id: int, payload: TransactionIn):
    """"Endpoint untuk mengubah data transaksi berdasarkan id"""
    user = User.objects.get(pk=request.user.id)
    transaction = Transaction.objects.get(pk=transaction_id)
    if transaction.user != user:
        return {"message": "Anda tidak berhak mengubah data ini"}
    else:
        transaction.category = Category.objects.get(pk=payload.category_id)
        transaction.amount = payload.amount
        transaction.description = payload.description
        transaction.type = payload.type
        transaction.transaction_date = datetime.strptime(payload.transaction_date[:10], '%Y-%m-%d').date()
        transaction.save()
        return transaction
    
@api.delete('/transaction/{transaction_id}', auth=apiauth)
def delete_transaction(request, transaction_id: int):
    """Endpoint untuk menghapus transaksi berdasarkan id"""
    user = User.objects.get(pk=request.user.id)
    transaction = Transaction.objects.get(pk=transaction_id)
    if transaction.user != user:
        return {"message": "Anda tidak berhak menghapus data ini"}
    else:
        transaction.delete()
        return {"message": "Data transaksi berhasil dihapus"}
    