from django.shortcuts import render, redirect, HttpResponse 
from models import *
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'books/index.html')
def show_books(request):
    books = Book.objects.all()
    book3=[]
    for book in books[:3]:
        book3.append(book)
    books_list = []
    for book in books[3:]:
        books_list.append(book)
    reviews = Review.objects.all()
    users = User.objects.all()
    current_user = User.objects.get(id = request.session['id'])
    return render(request, 'books/show.html',{'reviews': reviews, 'users': users, 'current_user': current_user, 'book3':book3, 'books_list': books_list})
    



def show_book(request, id):
    book = Book.objects.get(id=id)
    author_id = book.author_id
    print author_id
    author = Author.objects.get(id = author_id)
    print author
    reviews = Review.objects.filter(book_id = id)
    context={
        'book': book,
        'author': author.name,
        'reviews': reviews,
        'users': User.objects.all()
    }
    
    return render(request, 'books/show_book.html', context)












def new_book(request):
    authors = Author.objects.all()
    return render(request, 'books/new.html', {'authors': authors, 'name': 'hi'})

def add_book(request):
    r = request.POST.get('author_list', False)
    if r != False:
        print request.POST['author_list']
        print "ikiiiiiiiiii"
        author_id = request.POST['author_list']
    else:
        print 'hiiiiiiiiieeeee'
        author_name = request.POST['author_name']
        author = Author.objects.create(name=author_name)
        author_id = author.id
    
    body = request.POST['body']
    rating = request.POST['rating']       
    book = Book.objects.create(title = request.POST['title'], author_id = author_id)
    book_id = book.id
    review = Review.objects.create(body = body, rating = rating, user_id = request.session['id'], book_id = book_id)
    return redirect('/books/{}'.format(book_id))

def show_user(request, id):
    user_id = id
    user = User.objects.get(id = user_id)  
    return render(request, 'books/show_user.html', {'user':user})


def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        password = request.POST['password'].encode()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        user = User.objects.create(name= request.POST['name'], alias= request.POST['alias'], email = request.POST['email'], password = hashed)
        print user.password
        print hashed
        request.session['id'] = user.id
        return redirect('/books') 
def logout(request):
    id = request.session['id']
    del request.session['id'] 
    return redirect('/')
def login(request):
    email = request.POST['email']
    password = request.POST['password']
    
    if User.objects.filter(email=email):
        user = User.objects.filter(email=email)
    else:
        messages.error(request, "User does not exist. Please create an account")
        return redirect('/')
    u_password = user.first().password
    if user.count() > 0 and user.first().email == email and bcrypt.checkpw(password.encode(), u_password.encode()):
        request.session['id'] = user.first().id
        return redirect('/books')
    else:
        messages.error(request, "User name and password does not match")
        return redirect('/')
def add_review(request,id):
    book_id = id
    review = Review.objects.create(body = request.POST['body'], rating = request.POST['rating'], user_id = request.session['id'], book_id = book_id)
    return redirect('/books/{}'.format(book_id))

def delete_review(request,id):
    review = Review.objects.get(id = id)
    review.delete()
    return redirect('/books/{}'.format(review.book_id))

 