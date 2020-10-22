from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
import bcrypt


# Create your views here.
def index(request):
    return render(request,'index.html')

def register_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash messagecopy
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        #hashes the password
        hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print('hash password: ', hash_password)
        #create a new user
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'], 
            email=request.POST['email'], 
            password=hash_password
            )
        print('New user password: ',new_user.password)
        request.session['user_id'] = new_user.id
    return redirect('/quotes')

def login_user(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash messagecopy
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email'])
        if user: #
            logged_in_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_in_user.password.encode()):
                request.session['user_id'] = logged_in_user.id
                return redirect('/quotes')
    return redirect('/')        

def login_successful(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    print(request.POST)
    context = {
        "user": User.objects.get(id=user_id)
    }
    return render(request,"dashboard.html", context)

def logout(request):
    print(request.POST)
    print("Logging out")
    request.session.flush()
    return redirect('/')  

def show_dashboard(request):
    if 'user_id' not in request.session:
        print("NO SESSION, invalid dashboard access")
        return redirect('/')
    print(request.POST)
    
    # this_thought = Thought.objects.get(id=request.session['thought_id'])
    context = {
        'all_quotes': Quote.objects.all(),
        'user': User.objects.get(id=request.session['user_id']),
        'all_users': User.objects.all()
    }
    return render(request, 'dashboard.html', context) 

def add_quote(request):
    print(request.POST)
    errors = Quote.objects.quote_validator(request.POST)
    #Check for errors
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:
        this_user = User.objects.get(id=request.session['user_id'])                          
        quote = Quote.objects.create(quote=request.POST['quote_bar'], user_thought=this_user)
        print(quote)
        return redirect('/quotes')

def view_quote(request,quote_id):
    print(request.POST)
    this_quote = Quote.objects.get(id=quote_id)
    context = {
        'all_quotes' : Quote.objects.all(),
        'quote': this_quote
        # 'user':User.objects.all()
    }
    return render(request,'view.html', context)

def liked(request, quote_id):
    print(request.POST)
    
    #adding a relationship
    this_user = User.objects.get(id=request.session['user_id'])
    this_quote = Quote.objects.get(id=quote_id)
    this_quote.liked_quote.add(this_user)
    # print('who liked: '+ this_thought.liked_thought.add(this_user))
    return redirect(f'/quotes/{quote_id}')

def unlike(request, quote_id):
    print(request.POST)
    
    #adding a relationship
    this_user = User.objects.get(id=request.session['user_id'])
    this_quote = Quote.objects.get(id=quote_id)
    this_quote.liked_quote.remove(this_user)
    # print('who liked: '+ this_thought.liked_thought.add(this_user))
    return redirect(f'/quotes/{quote_id}')

def edit_user(request, user_id):
    print(request.POST)
    context = {
        # 'job': Job.objects.get(id=job_id),
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'edit_account.html', context)

def remove(request, quote_id):
    this_quote = Quote.objects.get(id=quote_id)
    # print("Removing quote:" + this_quote)
    this_quote.delete()
    return redirect('/quotes') 

