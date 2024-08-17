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



# create a youbue video in website 


# def youtube_video_view(request):
#     video_id = ["d-IwBrLt2aI?si=6qjmlnB6wU5maLwV" ,"zieItsS9Zvs?si=mJDNSV2UNZtvAMqD"] # Example video ID
#     return render(request, 'user/youtube_video.html', {'video_id': video_id})
from django.shortcuts import render, get_object_or_404


#video_ids = ["d-IwBrLt2aI?si=6qjmlnB6wU5maLwV" ,"zieItsS9Zvs?si=mJDNSV2UNZtvAMqD"]

def youtube_video_view(request, video_index=0):
    # List of video IDs (without query parameters)
    video_ids = ["d-IwBrLt2aI", "zieItsS9Zvs","aiMtb5g6970"]

    # Ensure the video_index is within the valid range
    video_index = int(video_index)
    if video_index < 0:
        video_index = 0
    elif video_index >= len(video_ids):
        video_index = len(video_ids) - 1

    # Get the current video ID
    current_video_id = video_ids[video_index]

    # Determine if there are previous or next videos
    has_previous = video_index > 0
    has_next = video_index < len(video_ids) - 1

    context = {
        'video_id': current_video_id,
        'video_index': video_index,
        'has_previous': has_previous,
        'has_next': has_next,
    }

    return render(request, 'user/youtube_video.html', context)



def datepicker(request):
    return render(request,'user/datepick.html')




from django.shortcuts import render, redirect
from .forms import CustomForm
from .models import CustomData

def custom_view(request):
    if request.method == 'POST':
        form = CustomForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            CustomData.objects.create(
                text_box_1=form.cleaned_data['text_box_1'],
                text_box_2=form.cleaned_data['text_box_2'],
                dropdown_1=form.cleaned_data['dropdown_1'],
                dropdown_2=form.cleaned_data['dropdown_2'],
            )
            
            # Redirect to a new URL or render a success message
            return redirect('success_page')
    else:
        form = CustomForm()

    return render(request, 'user/custom_template.html', {'form': form})


def success_view(request):
    return render(request, 'user/success.html')



from django.shortcuts import render, redirect
from .forms import ProductFeedbackForm
from .models import ProductFeedback

def feedback_view(request):
    if request.method == 'POST':
        form = ProductFeedbackForm(request.POST)
        if form.is_valid():
            ProductFeedback.objects.create(
                product_name=form.cleaned_data['product_name'],
                customer_name=form.cleaned_data['customer_name'],
                rating=form.cleaned_data['rating'],
                feedback=form.cleaned_data['feedback'],
                purchase_date=form.cleaned_data['purchase_date'],
            )
            return redirect('success_page_')
    else:
        form = ProductFeedbackForm()

    return render(request, 'user/feedback_form.html', {'form': form})

def success_view_(request):
    return render(request, 'user/success_.html')



from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
            return redirect('file_list')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def file_list(request):
    from django.conf import settings
    from django.core.files.storage import FileSystemStorage
    
    fs = FileSystemStorage()
    files = fs.listdir('')[1]  # List all files in the media root
    file_urls = [fs.url(file) for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]  # Filter image files
    
    return render(request, 'file_list.html', {'file_urls': file_urls})





