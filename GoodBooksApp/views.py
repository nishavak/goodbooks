from collections import Counter
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.template.defaulttags import register
from django.db.models import Avg
from .models import Book, Feedback, Tag, Profile
from .forms import SignUpForm, FeedbackForm, ProfileForm
from django.db.models import Q
import operator
import random


def handleAnon(request):
    return render(request, "GoodBooksApp/anonuser.html")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect(BookList)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="GoodBooksApp/login.html",
                  context={"form": form})


def deleteProfile(request):
    if not request.user.is_authenticated:
        return redirect(handleAnon)
    current_user_id = request.POST.get('userid')
    user = User.objects.all().get(id=current_user_id)
    try:
        user.delete()
        messages.success(request, "The user is deleted")
    except User.DoesNotExist:
        messages.error(request, "User doesn't exist")
    return redirect(Homepage)


def logoutRequest(request):
    logout(request)
    return redirect(Homepage)


def BookList(request):
    query = request.GET.get("key")
    books = Book.objects.all()
    queryFeedback = Feedback.objects.all()
    queryTag = Tag.objects.all()
    ratings = {}
    for i in books.values():
        f = queryFeedback.filter(book_id=i.get('id')).aggregate(
            Avg('rating')).get('rating__avg')
        if f == None:
            ratings[i.get('id')] = 'Not Rated'
        else:
            ratings[i.get('id')] = round(float(f), 2)
    rating_cleaned = ratings.copy()
    for i in rating_cleaned.keys():
        if rating_cleaned[i] == 'Not Rated':
            rating_cleaned[i] = 0.0
    requestedBooksFromRatings = []
    try:
        if query:
            for i in rating_cleaned.keys():
                if float(query) == int(rating_cleaned[i]):
                    requestedBooksFromRatings.append(i)
                elif float(query) == float(rating_cleaned[i]):
                    requestedBooksFromRatings.append(i)
    except:
        pass
    del rating_cleaned
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(published_date__icontains=query) |
            Q(tag__tagname__icontains=query) |
            Q(author__name__icontains=query) |
            Q(id__in=requestedBooksFromRatings)
        ).distinct()
    del requestedBooksFromRatings
    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)
    context = {
        'books': books.order_by('-published_date'),
        'queriesFeedback': queryFeedback,
        'queriesTag': queryTag,
        'rating': ratings,
    }
    return render(request, "GoodBooksApp/book_list.html", context)


def deleteFeedback(request):
    if not request.user.is_authenticated:
        return redirect(handleAnon)
    book_id = request.POST.get('book_id')
    feedback_id = request.POST.get('feedback_id')
    Feedback.objects.get(id=feedback_id).delete()
    return redirect(bookDetails, id=book_id)


def bookDetails(request, id):
    if not request.user.is_authenticated:
        return redirect(handleAnon)
    form = FeedbackForm(request.POST)
    PO = Profile.objects.get(user=request.user)
    fb = Feedback.objects.filter(user=PO).filter(book_id=id)
    current_user = Profile.objects.get(user=request.user)
    read_books = current_user.books.all()
    try:
        read_books = read_books.get(id=id).id
    except:
        read_books = -1
    if request.POST:
        if form.is_valid():
            obj = form.save(commit=False)
            if fb is None:
                obj.user = current_user
                obj.book_id = id
                obj.save()
                form = FeedbackForm(request.POST)
            else:
                if obj is not None:
                    fb.delete()
                obj.user = current_user
                obj.book_id = id
                obj.save()
                form = FeedbackForm(request.POST)
    users = User.objects.all()
    logged_in_user = str(request.user)
    queryset = Book.objects.get(id=id)
    queryFeedback = Feedback.objects.all()
    f = queryFeedback.filter(book_id=id)
    f2 = f
    f = f.aggregate(Avg('rating'))
    f = f.get('rating__avg')
    ratings = {}
    if f == None:
        ratings[id] = 'Not Rated'
    else:
        ratings[id] = round(float(f), 2)

    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key, -1)

    @register.filter
    def get_username(dictionary, key):
        return str(dictionary.get(id=key).username)
    context = {
        'form': form,
        'book': queryset,
        'rating': ratings,
        'feedbackObject': f2.values(),
        'count_of_ratings': f2,
        'users': users,
        'logged_in_user': logged_in_user,
        'read_books': read_books,
    }
    return render(request, 'GoodBooksApp/book_details2.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            form = SignUpForm()
            return redirect(Homepage)
    else:
        form = SignUpForm()
    return render(request, 'GoodBooksApp/user_create.html', {'form': form})


def UserLoginView(request):
    username = request.POST.get('username')
    password = request.POST.get('password')


def Homepage(request):
    current_user = request.user
    queryFeedback = Feedback.objects.all()
    queryset = Book.objects.all()
    ratings = {}
    for i in queryset.values():
        f = queryFeedback.filter(book_id=i.get('id'))
        f = f.aggregate(Avg('rating'))
        f = f.get('rating__avg')
        if f == None:
            ratings.setdefault(i.get('id'), 0)
        else:
            ratings.setdefault(i.get('id'), round(float(f), 2))
    rating_sorted = sorted(
        ratings.items(), key=operator.itemgetter(1), reverse=True)[:7]
    temp = {}
    for i in rating_sorted:
        temp.setdefault(i[0], i[1])
    rating_sorted = temp
    del temp
    rating_sorted_keys = rating_sorted.keys()
    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    @register.filter
    def get_title(dictionary, key):
        return str(dictionary.get(id=key).title)

    @register.filter
    def get_cover(dictionary, key):
        return str(dictionary.get(id=key).cover.url)

    @register.filter
    def get_quote(dictionary, key):
        return str(dictionary.get(id=key).quote)
    context = {
        'user': current_user,
        'books': queryset,
        'rating_sorted': rating_sorted,
        'rating_sorted_keys': list(rating_sorted_keys),
    }
    return render(request, 'GoodBooksApp/Homepage.html', context)


def profileView(request):
    if not request.user.is_authenticated:
        return redirect(handleAnon)
    current_user = Profile.objects.get(user=request.user)
    user_linked = User.objects.get(id=current_user.user_id)
    feedbacks = Feedback.objects.filter(user_id=current_user.user_id)
    count = len(feedbacks.values())
    rating = feedbacks.aggregate(Avg('rating'))
    rating = rating.get('rating__avg')
    books = Book.objects.filter(profile=current_user.user_id)
    form = ProfileForm(request.POST, request.FILES)
    if request.POST:
        if form.is_valid():
            user_obj = form.save(commit=False)
            current_user.profile_picture = user_obj.profile_picture
            current_user.save()
            form = ProfileForm()
        else:
            form = ProfileForm
    queryTag = Tag.objects.all()
    tag_list = []
    for i in queryTag.values():
        tag_list.append(i['tagname'])
    cnt = Counter()
    for book in books:
        tags_in_book = book.tag.all()
        for item in tags_in_book.values():
            cnt[item.get('tagname')] += 1
    cnt = dict(cnt)
    labels = list(cnt.keys())
    values = list(cnt.values())
    colors = []
    def r():
        return random.randint(0, 255)
    for i in range(0, len(tag_list)):
        colors.append('#%02X%02X%02X' % (r(), r(), r()))
    context={
        'profile': current_user,
        'user': user_linked,
        'feedbacks': feedbacks,
        'count': count,
        'avg_rating': rating,
        'books': books,
        'form': form,
        'labels': labels,
        'values': values,
        'colors': colors,
    }
    return render(request, 'GoodBooksApp/profile.html', context)


def addReadBook(request):
    if not request.user.is_authenticated:
        return redirect(handleAnon)
    bookid=request.POST.get('book_id')
    user=request.user
    po=Profile.objects.get(id=user.id)
    book=Book.objects.get(id=bookid)
    po.books.add(book)
    return redirect(bookDetails, id=bookid)


def delReadBook(request):
    if not request.user.is_authenticated:
        return redirect(handleAnon)
    bookid=request.POST.get('book_id')
    user=request.user
    po=Profile.objects.get(id=user.id)
    book=Book.objects.get(id=bookid)
    po.books.remove(book)
    return redirect(bookDetails, id=bookid)
