from django.shortcuts import render, redirect
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
# from games.models import Bet


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

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


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


def home(request):
    return render(request, 'users/home.html')

