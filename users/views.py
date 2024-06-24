from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import F
from games.models import Bet
from.models import Profile
import africastalking
import math, random
from django.contrib import messages
from .forms import OTPVerificationForm


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # Set user as inactive until email confirmation
#             user.save()

#             # Generate activation token
#             token = default_token_generator.make_token(user)

#             # Build activation URL
#             current_site = get_current_site(request)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             activation_url = f'http://{current_site.domain}/activate/{uid}/{token}/'

#             # Render activation email template
#             activation_email = render(request, 'users/activation_email.html', {'activation_link': activation_url})

#             # Send confirmation email
#             email_subject = 'Account Activation'
#             email_message = activation_email.content.decode('utf-8')  # Convert rendered template to string
#             send_mail(email_subject, '', settings.EMAIL_HOST_USER, [user.email], html_message=email_message)

#             messages.success(request, 'Please check your email to activate your account.')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})


# def activate_account(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, 'Your account has been activated. You can now log in.')
#         return redirect('login')
#     else:
#         messages.error(request, 'Invalid activation link.')
#         return redirect('register')

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your account has been created! You can now log in.')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})


# Initialize the Africa's Talking SDK
username = "USERNAME"
api_key = "AFRICASTALKING_API_KEY"
africastalking.initialize(username, api_key)
sms = africastalking.SMS

def generate_otp():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')  
            username = user.username

            otp = generate_otp()
            print(otp)

            # Save phone number to Profile model
           # Save phone number and OTP to Profile model
            profile = Profile.objects.create(user=user, phone_number=phone_number, otp=otp)

            # Send OTP via SMS
            message = f"Your OTP for signup is {otp}"
            response = sms.send(message, [phone_number])
            print(response)  # Print the response for debugging purposes

            # Inform the user to check their SMS for OTP
            messages.info(request, 'An OTP has been sent to your phone number. Please verify your account.')

            # Redirect to OTP verification page
            return redirect('otp_verify', user_id=user.id)

            # # Send SMS
            # message = f"Hello {username}, You have successfully created an account with 47bets.com. Bet responsibly. Only 18yrs+ are eligible for betting with us."
            # try:
            #     response = sms.send(message, [phone_number])
            #     print(response)
            # except Exception as e:
            #     print(f"Error sending SMS: {e}")

            # messages.success(request, 'Your account has been created! You can now log in.')
            # return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def otp_verify(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            if otp == profile.otp:
                profile.otp = ''  # Clear the OTP after successful verification
                profile.save()
                messages.success(request, 'Your account has been verified! You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()

    return render(request, 'users/otp_verify.html', {'form': form})

@login_required
def profile(request):
    current_datetime = timezone.now()
    user_bets = Bet.objects.filter(user=request.user).annotate(
        bet_result=F('result'),
        doubled_bet_amount=F('bet_amount') * 2
    )

    context = {
        'user_bets': user_bets,
        'current_datetime': current_datetime,
    }

    return render(request, 'users/profile.html', context)


# def home(request):
#     return render(request, 'users/home.html')

