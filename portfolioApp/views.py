from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
import bcrypt

# Create your views here.
def main(request):
    return render(request,'main.html')

def register(request):
    errors = User.objects.registerVal(request.POST)
    if len(errors) > 0:                    
        for keys, val in errors.items():  
           messages.error(request, val)
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    newuser = User.objects.create(
        firstname = request.POST['fname'],
        lastname = request.POST['lname'],
        email = request.POST['email'],
        password = pw_hash
    )
    if newuser:
        request.session['loginid'] = newuser.id
    return redirect('/home')

def login(request):
    errors = User.objects.loginVal(request.POST)
    if len(errors) > 0:                    
        for keys, val in errors.items():  
           messages.error(request, val)
        return redirect('/')
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['loginid'] = logged_user.id
            return redirect('/home')
    
def home(request):
    if 'loginid' not in request.session:
        return redirect('/')
    else:
        getuser = User.objects.get(id = request.session['loginid'])
        allitem = Item.objects.all()
        paginator = Paginator(allitem, 9) #show 9 itmes per page
        page = request.GET.get('page')
        allitem = paginator.get_page(page)
        context = {
            'user': getuser,
            'items': allitem
        }
    return render(request,'home.html', context)

def aboutme(request):
    getuser = User.objects.get(id = request.session['loginid'])
    context = {
        'user': getuser,
    }
    return render(request, 'aboutme.html', context)

def mywork(request):
    getuser = User.objects.get(id = request.session['loginid'])
    allitem = Item.objects.all()
    #filters
    filterbyall = Item.objects.all()
    filterbyweb = Item.objects.filter(category = 'Web')
    filterbydesign = Item.objects.filter(category = 'Design')
    filterbylogo = Item.objects.filter(category = 'Logo')
    filterbyphoto = Item.objects.filter(category = 'Photography')
    #pageinator starts here
    paginator = Paginator(allitem, 9) #show 9 itmes per page
    page = request.GET.get('page')    
    allitem = paginator.get_page(page)
    context = {
        'user': getuser,
        'items': allitem,
        'all': filterbyall,
        'web': filterbyweb,
        'design': filterbydesign,
        'logo': filterbylogo,
        'photo': filterbyphoto
    }
    return render(request, 'mywork.html', context)

def item(request, itemid):
    getuser = User.objects.get(id = request.session['loginid'])
    getitem = Item.objects.get(id = itemid)
    otheritem = Item.objects.exclude(id = itemid)
    #pageinator starts here
    paginator = Paginator(otheritem, 6) 
    page = request.GET.get('page')    
    otheritem = paginator.get_page(page)
    context = {
        'user': getuser,
        'item': getitem,
        'others': otheritem
    }
    return render(request, 'item.html', context)

def addtolist(request, itemid):
    getuser = User.objects.get(id = request.session['loginid'])
    getitem = Item.objects.get(id = itemid)
    
    addtolist = List.objects.create(
        buyer = getuser,
        obj = getitem,
        quantity = request.POST['quantity']
    )
    return redirect('/list')

def itemlist(request):
    getuser = User.objects.get(id = request.session['loginid'])
    allitemlist = List.objects.filter(buyer = getuser)
    context = {
        'user': getuser,
        'alllist': allitemlist,
        
    }
    print(allitemlist)
    print('***********************')
    return render(request, 'list.html', context)

def delete(request, itemid):    
    getitem = List.objects.get(id = itemid)
    getitem.delete()
    return redirect('/list')

def checkout(request):
    getuser = User.objects.get(id = request.session['loginid'])
    context = {
        'user': getuser,
    }
    return render(request, 'checkout.html', context)

def contact(request):
    getuser = User.objects.get(id = request.session['loginid'])
    context = {
        'user': getuser,
    }
    
    return render(request, 'contact.html', context)

def sendemail(request):
    #send_mail(sub, msg, from ,to, fail_silently=True)
    from_email = request.POST.get('email', '')
    print('***************')
    print(from_email)
    print(type(from_email))
    print('***************')
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    to_list = [settings.EMAIL_HOST_USER]
    if subject and message and from_email:
        send_mail(subject, from_email+" "+message, from_email, to_list, fail_silently=False)
    return redirect('/home')

def edit(request):
    getuser = User.objects.get(id = request.session['loginid'])
    context = {
        'user': getuser,
    }
    return render(request, 'edit.html', context)

def update(request):
    getuser = User.objects.get(id = request.session['loginid'])
    if bcrypt.checkpw(request.POST['password'].encode(), getuser.password.encode()):
        newpassword = request.POST['newpw']
        pw_hash = bcrypt.hashpw(newpassword.encode(), bcrypt.gensalt()).decode()
        getuser.firstname = request.POST['fname']
        getuser.lastname = request.POST['lname']
        # print('***************')
        # print(getuser.picture)
        # print('***************')
        # if 'img' in request.POST:
        #     getuser.picture = request.POST['img']
        #     print('***************')
        #     print(getuser.picture)
        #     print('***************')
        getuser.password = pw_hash
        getuser.save()
    return redirect('/edit')

def logout(request):
    request.session.clear()
    return redirect("/")