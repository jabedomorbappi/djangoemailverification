from .forms import UserRegisterForm
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import UserLoginForm


User = get_user_model()



# send email with verification link
def verify_email(request):
    if request.method == "POST":
        if not request.user.email_is_verified:
            current_site = get_current_site(request)
            user = request.user
            email = user.email
            subject = "Verify Email"
            message = render_to_string('user/verify_email_message.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email_message = EmailMessage(subject, message, to=[email])
            email_message.content_subtype = 'html'
            email_message.send()
            return redirect('verify-email-done')
        else:
            return redirect('signup')
    return render(request, 'user/verify_email.html')



def verify_email_done(request):
    return render(request, 'user/verify_email_done.html')


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('verify-email-complete')   
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'user/verify_email_confirm.html')


def verify_email_complete(request):
    return render(request, 'user/verify_email_complete.html')


# def signup_view(request):
#     if request.method == "POST":
#         next = request.GET.get('next')
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             password = form.cleaned_data.get('password')
#             user.set_password(password)
#             user.save()
#             new_user = authenticate(email=user.email, password=password)
#             login(request, new_user)
#             if next:
#                 return redirect(next)
#             else:
#                 return redirect('verify-email')
#     else:
#         form = UserRegisterForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'user/signup.html', context) 

def signup_view(request):
    if request.method=="POST":
        next=request.GET.get('next')
        form=UserRegisterForm(request.POST) 
        if form.is_valid():
            user=form.save(commit=False)
            password=form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user=authenticate(email=user.email,password=password)
            login(request,new_user)
            
            if next:
                return redirect(next)
            else:
                return redirect('verify-email')
            
    else:
        form=UserRegisterForm()
    context={
        'form':form

    }         
    return render(request,'user/signup.html',context)

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.email_is_verified:
                    auth_login(request, user)
                    messages.success(request, 'Successfully logged in.')
                    return redirect(request.GET.get('next', 'home'))
                else:
                    messages.warning(request, 'Your email is not verified. Please verify your email.')
                    return redirect('verify-email')
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('login')
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'admin/login.html', context)


def home (request):
    return render(request,"user/home.html")