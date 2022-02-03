from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import RegistrationData,UserProfileEdit
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.urls import reverse_lazy
from .models import HelpCenter,Transaction
from .forms import HelpCenterData,TransactionForm
import random
from django.contrib.auth.models import User
import random
from django.db.models import Sum,Count
from django.views.generic import TemplateView
from .utils import get_plot
import numpy as np
def index(request):
    return render(request, "index.html")


def register(request):
    if request.method=='POST':
        form= RegistrationData(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"login.html")
    else:
        form=RegistrationData()
    return render(request,'register.html',{'form':form})


def login1(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username+""+password)
        user = authenticate(request,username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("home")
    return render(request,'login.html')

def home(request):
    uname=User.objects.get(username=request.user.get_username())
    transactions = Transaction.objects.filter(username=uname)
    total_credit  = Transaction.objects.filter(username=uname).aggregate(Sum('credit_amount'))
    total_debit = Transaction.objects.filter(username=uname).aggregate(Sum('debit_amount'))
    if total_credit['credit_amount__sum'] is not None and total_debit['debit_amount__sum'] is not None:
        balanc = total_credit['credit_amount__sum'] - total_debit['debit_amount__sum']
    else:
        if total_debit['debit_amount__sum'] is None and total_credit['credit_amount__sum'] is None:
            balanc=0
        elif total_credit['credit_amount__sum'] is None and total_debit['debit_amount__sum'] is not None:
            balanc=total_credit['credit_amount__sum']
        else:
            balanc=0-total_debit['debit_amount__sum']
             
    balance = "{:.2f}".format(balanc)
    no_credit=[]   
    no_debit=[]
    for trans in transactions:
        if trans.credit_amount>0:
            no_credit.append(int(trans.credit_amount))
        elif trans.debit_amount>0:
            no_debit.append(int(trans.debit_amount))
    
    tc=str(total_credit['credit_amount__sum'])
    td=str(total_debit['debit_amount__sum'])
    return render(request, "home.html",{'balance':balance,'totalcredit':tc,'totaldebit':td})

def time(request):
    import datetime
    return HttpResponse(str(datetime.datetime.now()))

def aboutus(request):
    return render(request, "aboutus.html")

def credits(request):
    transactions = Transaction.objects.filter(username=request.user.get_username())
    no_credit=[]
    no_debit=[]
    for trans in transactions:
        if trans.credit_amount>0:
            no_credit.append(trans)
        elif trans.debit_amount>0:
            no_debit.append(trans)
    creditscore=25*len(no_credit) - 10*len(no_debit)
    print(no_credit)
    return render(request, "credits.html",{'credit':no_credit,'debit':no_debit,'creditscore':creditscore})

def calendar(request):
    return render(request, "calendar.html")


def invoice(request):
    return render(request, "invoice.html")
def inbox(request):
    transactions = Transaction.objects.filter(username=request.user.get_username())
    no_credit=[]
    trans_cat_credit=[]
    trans_cat_debit=[]   
    no_debit=[]
    for trans in transactions:
        if trans.credit_amount>0 and trans.tran_category not in trans_cat_credit:
            no_credit.append(int(trans.credit_amount))
            trans_cat_credit.append(str(trans.tran_category))
        elif trans.tran_category in trans_cat_credit:  
            ind = trans_cat_credit.index(trans.tran_category)
            no_credit[ind] = int(no_credit[ind] + trans.credit_amount)
        elif trans.debit_amount>0 and trans.tran_category not in trans_cat_debit:
            no_debit.append(int(trans.debit_amount))
            trans_cat_debit.append(str(trans.tran_category))
        elif trans.tran_category in trans_cat_debit:
             ind = trans_cat_debit.index(trans.tran_category)
             no_debit[ind] = int(no_debit[ind] + trans.debit_amount)
    print(no_credit)
    print(no_debit)           
    p1=len(no_credit)
    p2=len(no_debit)
    trans_count=[p1,p2]
    p11= [p for p in range(1,len(no_credit)+1)]
    p22= [p21 for p21 in range(1,len(no_debit)+1)]
    chart=get_plot(p11,no_credit,p22,no_debit)  
    return render(request, "inbox.html",{'credit':no_credit,'debit':no_debit,'trans_count':trans_count,'trans_cat_credit':trans_cat_credit,'trans_cat_debit':trans_cat_debit,'chart':chart})

def tutorials(request):
    return render(request, "tutorials.html")

def forgotpwd(request):
    return render(request, "forgotpwd.html")

def profile(request):
    user=User.objects.get(username=request.user.get_username())
    return render(request,'profile.html',{'user':user})

def logout_view(request):
    logout(request)
    return redirect("index")

def encryption(request):
    from cryptography.fernet import Fernet

    message = "hey pavan"


    key = Fernet.generate_key()


    fernet = Fernet(key)

    encMessage = fernet.encrypt(message.encode())
    
    print("original string: ", message)
    print("encrypted string: ", encMessage)
    decMessage = fernet.decrypt(encMessage).decode()

    print("decrypted string: ", decMessage)
    return HttpResponse( encMessage)


def tipsandsug():
    tips=[' Learn the Financial Statergies first',
      'Learn Self-Control',
       ' Control Your Financial Future',
       ' Know Where Your Money Goes',
       'Start an Emergency Fund',
      'Start Saving for Retirement',
      'Get a Grip on Taxes',
      'Guard Your Health',
      'Pay Yourself First',
      'Protect Your Wealth',
      'Create a Financial Calendar',
      'Check Your Interest Rate',
      'Track Your Net Worth',
      'Set a Budget, Period',
      'Consider an All-Cash Diet',
      'Take a Daily Money Minute',
      "Get Paid What You're Worth and Spend Less Than You Earn",
      'Stick to a Budget',
      'Pay off Credit Card Debt',
      'Contribute to a Retirement Plan',
      'Have a Savings Plan',
      'Invest',
      'Maximize Your Employment Benefits',
      'Review Your Insurance Coverages',
      'Update Your Will',
      'Keep Good Records']
    random.shuffle(tips)
    num=random.randint(0,len(tips))
    p=tips[num]
    return p

def tipsandsuggestions(request):
    tip=tipsandsug()
    return render(request,'home.html',{'tip':tip})

def helpcenter(request):
    if request.method=='POST':
        request.POST._mutable = True
        request.POST['username']=request.user.get_username()
        form=HelpCenterData(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form=HelpCenterData()
    else:
        form=HelpCenterData()

    return render(request,'help.html',{'form':form})

def editprofile(request):
    if request.method=='POST':
        user=User.objects.get(username=request.user.get_username())
        form=UserProfileEdit(request.POST,instance=user)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            form.save()
            return redirect('logout')
        else:
            return redirect('editprofile')
    else:
        username=request.user.get_username()
        initial_dict = {
            "username" : username,
            "first_name":None,
            "last_name":None,
            "email":None,
            
        }
        form=UserProfileEdit(initial=initial_dict)
    return render(request,'editprofile.html',{'form':form})


def inserttrans(request):
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST['username']=request.user.get_username()
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('inbox')
    else:
        form = TransactionForm()
    return render(request, "inserttrans.html",{'form':form})


def passbook(request):
    uname=User.objects.get(username=request.user.get_username())
    transactions = Transaction.objects.filter(username=uname)
    total_credit  = Transaction.objects.filter(username=uname).aggregate(Sum('credit_amount'))
    total_debit = Transaction.objects.filter(username=uname).aggregate(Sum('debit_amount'))
    if total_credit['credit_amount__sum'] is not None and total_debit['debit_amount__sum'] is not None:
        balanc = total_credit['credit_amount__sum'] - total_debit['debit_amount__sum']
    else:
        if total_debit['debit_amount__sum'] is None and total_credit['credit_amount__sum'] is None:
            balanc=0
        elif total_credit['credit_amount__sum'] is None and total_debit['debit_amount__sum'] is not None:
            balanc=total_credit['credit_amount__sum']
        else:
            balanc=0-total_debit['debit_amount__sum']
    balance = "{:.2f}".format(balanc)
    return render(request, "invoice.html", {'transactions': transactions, 'balance': balance})


def deletetransaction(request,tid):
    uname=User.objects.get(username=request.user.get_username())
    Transaction.objects.filter(id=tid).delete()
    return redirect('invoice')

def updatetransaction(request,tid):
    request.session['tid']=tid
    return render(request,'updatetransactions.html',{'tid':tid})

def updatetransactiondata(request):
    if request.method=='POST': 
        tid=request.POST.get('tid')
        date=request.POST.get('tdate')
        category=request.POST.get('tcategory')
        credit=request.POST.get('tcredit')
        debit = request.POST.get('tdebit')
        desc=request.POST.get('tdesc')
        p=Transaction.objects.get(id=tid)
        p.tran_date=date
        p.tran_category=category
        p.credit_amount=credit
        p.debit_amount=debit
        p.description=desc
        p.save()
        return render(request,'invoice.html')
    else:
        return redirect('updatetransaction')
