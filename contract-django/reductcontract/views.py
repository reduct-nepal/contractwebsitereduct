from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .create import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import *
from django.conf import settings
from django.contrib.auth.models import User
import datetime


from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse('<h1>This is the start</h1>')

def register(request):
    if request.method == "POST":
        user_form=UserForm(request.POST)
        crediantial=request.POST['crediantials']
        if not crediantial == 'Anurodhregisteraky':
            return render(request,'reductcontract/crediantials.html',{})
        else:
            if user_form.is_valid():
                user=user_form.save(commit=False)
                user.is_active=False
                user.save()
                current_site=get_current_site(request)
                mail_subject='Activate your  account.'
                message = render_to_string('reductcontract/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                })
                to_email = user_form.cleaned_data.get('email')
                email = EmailMessage(
                mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration.A mail has been sent to your email address with the conformation link')

    else:
        user_form=UserForm()

    context={
        'user_form':user_form
    }
    return render(request,'reductcontract/register.html',context)



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('profile')
        else:
            return HttpResponse('<h1>The user doesnot exist,please register</h1>')
    else:
        return render(request,'reductcontract/login.html',{})

def logout(request):
    django_logout(request)
    return redirect('login')





def hotel_image_view(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = HotelForm()

    return render(request, 'reductcontract/hotel_image_form.html', {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')


def display_hotel_images(request):
    if request.method == 'GET':
        # getting all the objects of hotel.
        Hotels = Hotel.objects.all()
        return render(request,'reductcontract/display_hotel_images.html',{'hotel_images': Hotels})


def addcontract(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method=='POST':
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            role = request.POST['country']
            contract_duration = request.POST['period']
            start_date = request.POST['startdate']
            finish_date = request.POST['finishdate']
            on_board = request.POST['onboard']
            address = request.POST['address']
            email = request.POST['email']
            phone_number = request.POST['phone']
            clause=request.POST['clause']
            user_id = request.POST['user_id']
            query = contractor()
            query.first_name = first_name
            query.last_name = last_name
            query.role = role
            query.contract_duration = contract_duration
            query.start_date = start_date
            query.finish_date = finish_date
            query.on_board=on_board
            query.clause=clause
            query.address = address
            query.email = email
            obj=contractor.objects.filter(email=email)
            myp=contractor.objects.filter(phone_number=phone_number)
            query.phone_number = phone_number
            query.user_id = user_id
            if obj.exists():
                return HttpResponse('The email already exists')
            if myp.exists():
                return HttpResponse('The phone already exists')
            if not obj.exists() and not myp.exists():
                query.save()
                sendmail =EmailMessage(
                   'Congratulation,Your contract is registered',
                   'Your contract is registered as {} and starting from {} and ending at{},Best of luck'.format(role,start_date,finish_date),
                   settings.EMAIL_HOST_USER,
                   [email],
                )
                sendmail.fail_silently = False
                sendmail.send()

                return redirect('showcontract')

        else:

            return render(request,'reductcontract/addcontract.html',{})

def showcontract(request):
    obj=contractor.objects.all()
    paginator=Paginator(obj,5)
    for i in obj:
        if i.finish_date >= datetime.date.today():
            i.status='Active'
        else:
            i.status='Expired'
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    if request.method =='POST':
        query=request.POST['aky']
        if query:
            find=contractor.objects.filter(Q(first_name__icontains=query)|Q(user__username__icontains=query)|Q(last_name__icontains=query)|Q(contract_duration__icontains=query)|Q(role__icontains=query)|Q(phone_number__icontains=query)|Q(email__icontains=query)|Q(address__icontains=query))
            paginator=Paginator(find,4)
            page_number=request.GET.get('page')
            page_obj=paginator.get_page(page_number)
            if find:
                return render(request,'reductcontract/search.html',{'sr':page_obj})
            else:
                return HttpResponse('No result found')

    context={
        'obj':page_obj,

    }
    return render(request,'reductcontract/showcontract.html',context)



def clause(request,iod):
    obj=contractor.objects.get(id=iod)
    context={
        'obj':obj
    }
    return render(request,'reductcontract/clause.html',context)








def contractupdate(request,iod):
    if request.user.is_authenticated:
        obj = contractor.objects.get(id=iod)
        if not obj.user==request.user:
            return HttpResponse('<h1>You are not authorized to update it only {} can update </h1>'.format(obj.user))
        else:
            context={
            'obj':obj
            }
            if request.method == 'POST':
                first_name = request.POST['firstname']
                last_name = request.POST['lastname']
                role = request.POST['country']
                contract_duration = request.POST['period']
                start_date = request.POST['startdate']
                finish_date = request.POST['finishdate']
                on_board = request.POST['onboard']
                address = request.POST['address']
                email = request.POST['email']
                phone_number = request.POST['phone']
                clause=request.POST['clause']
                query = contractor(id=iod)
                query.first_name = first_name
                query.last_name = last_name
                query.role = role
                query.contract_duration = contract_duration
                query.start_date = start_date
                query.finish_date = finish_date
                query.on_board=on_board
                query.address = address
                query.email = email
                query.phone_number = phone_number
                query.clause=clause
                query.user_id = obj.user.id
                check=contractor.objects.exclude(id = iod)
                obj = check.filter(email=email)
                myp = check.filter(phone_number=phone_number)
                if obj.exists():
                    return HttpResponse('The email you updated to is already associated with other contractor ')
                if myp.exists():
                    return HttpResponse('The phone number you updated to is already associated with other contractor')
                if not obj.exists() and not myp.exists():
                    query.save()
                    sendmail=EmailMessage(
                    'Your Contract is updated',
                    'Your new contract is of role as {} with the period of {} starting at {} and ending at {}'.format(role,contract_duration,start_date,finish_date),
                     settings.EMAIL_HOST_USER,
                    [email],

                    )
                    sendmail.fail_silently=False
                    sendmail.send()

                    return redirect('showcontract')

            else:
                 return render(request,'reductcontract/contractupdate.html',context)

    else:
        return HttpResponse('<h1>You need to login first</h1>')



def contractrenew(request,iod):
    if request.user.is_authenticated:
        obj=contractor.objects.get(id=iod)
        if not obj.user == request.user:
            return HttpResponse('<h1>Sorry you cannot renew the contract as it is not created by you ,only {} can renew it</h1>'.format(obj.user))
        else:
            context={
                'obj':obj,
            }
            if request.method=='POST':
                contract_duration = request.POST['period']
                start_date=request.POST['startdate']
                finish_date=request.POST['finishdate']
                query = contractor(id=iod)
                query.contract_duration = contract_duration
                query.start_date=start_date
                query.finish_date=finish_date
                query.role=obj.role
                query.first_name=obj.first_name
                query.last_name=obj.last_name
                query.address=obj.address
                query.email=obj.email
                query.phone_number=obj.phone_number
                query.user_id=obj.user.id
                query.save()
                sendmail = EmailMessage(
                    'Your Contract is Renewed',
                    'Your new contract is of role as {} with the period of {} starting at {} and ending at {}'.format(
                        obj.role, contract_duration, start_date, finish_date),
                    settings.EMAIL_HOST_USER,
                    [obj.email],

                )
                sendmail.fail_silently = False
                sendmail.send()

                return redirect('showcontract')

            else:
                return render(request,'reductcontract/contractrenew.html',context)
    else:
        return HttpResponse('<h1>You need to login first </h1>')


def contractdelete(request,iod):
    if request.user.is_authenticated:
        obj=contractor.objects.get(id=iod)
        context={
            'obj':obj
        }
        if not request.user == obj.user:
            return HttpResponse('<h1>You cannot delete it as it was not registered by you,only {} can delete it</h1>'.format(obj.user))
        else:
            if request.method=='POST':
                sendmail = EmailMessage(
                    'Your Contract is deleted}',
                    'Your contract with Reduct Nepal Pvt Limited as a {} ,which started at {} is deleted,'.format(obj.role,obj.start_date),
                    settings.EMAIL_HOST_USER,
                    [obj.email],

                )
                sendmail.fail_silently = False
                sendmail.send()
                obj.delete()
                return redirect('showcontract')
            else:
                return render(request,'reductcontract/contractdelete.html',context)
    else:
        return HttpResponse('<h1>You need to login first</h1>')




def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        obj=contractor.objects.filter(user=request.user.id)

        for i in obj:
            if i.finish_date >= datetime.date.today():
                i.status='Active'
            else:
                i.status='Expired'

        if request.method == 'POST':
            form=UserUpdateForm(request.POST,instance=request.user)
            profile=ProfileUpdateForm(request.POST or None,request.FILES or None,instance=request.user.profile)
            if form.is_valid() and profile.is_valid():
                form.save()
                profile.save()
                return redirect('profile')
        else:
            form=UserUpdateForm(instance=request.user)
            profile=ProfileUpdateForm(instance=request.user.profile)

        context={
            'form':form,
            'profile':profile,
            'obj':obj

        }
        return render(request,'reductcontract/profile.html',context)


