from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.http import JsonResponse
from accounts.models import Customer,NewsEvents,Banners, Payment, AboutUs, CharityManagement, AboutUsImage, Interest
from django.conf import settings
from django.db.models import Q
from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
User = get_user_model()
from django.views.generic import DetailView,UpdateView
from django.urls import reverse_lazy
from django.views import View
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from django.db.models import Max
from django.utils.timezone import make_aware
from datetime import datetime
import os
from django.utils import timezone


@login_required
def edit_payment(request):
    if request.method == "POST":
        payment_id = request.POST.get("payment_id")
        amount = request.POST.get("amount")
        payment_date = request.POST.get("payment_date")

        payment = get_object_or_404(Payment, id=payment_id)

        if payment_date:
            payment.payment_date = make_aware(datetime.fromisoformat(payment_date))
        payment.amount = amount
        payment.save()

        return redirect("payments_list") 

@login_required
def payments_list(request):
    # Step 1: Get the latest payment_date for each customer
    latest_dates = Payment.objects.filter(is_active=True).values("customer").annotate(
        latest_date=Max("payment_date")
    )

    # Step 2: Get the actual Payment records matching those dates
    latest_payments = Payment.objects.filter(
        is_active=True,
        payment_date__in=[item["latest_date"] for item in latest_dates]
    ).select_related("customer", "customer__user")

    return render(request, "super_admin/payments_list.html", {
        "payments": latest_payments
    })

@login_required
def change_password_modal(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    user = customer.user   # assuming Customer has OneToOne/ForeignKey to User

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password and new_password == confirm_password:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully!")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        else:
            messages.error(request, "Passwords do not match!")

    return render(request, "super_admin/change_password_modal.html", {"customer": customer})

@login_required
def payment_modal(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    payments = customer.payments.filter(is_active=True).order_by("-payment_date")

    if request.method == "POST":
        amount = request.POST.get("amount")
        if amount:
            Payment.objects.create(
                customer=customer,
                amount=amount,
                payment_date=now()
            )
            # ✅ Mark customer as Approved
            customer.status = 1
            customer.save(update_fields=["status"])

            payments = customer.payments.filter(is_active=True).order_by("-payment_date")

    return render(request, "super_admin/payment_modal.html", {
        "customer": customer,
        "payments": payments,
    })

# Handle new payment submission
@login_required
def add_payment(request, pk):
    if request.method == "POST":
        customer = get_object_or_404(Customer, pk=pk)
        amount = request.POST.get("amount")

        # Create payment
        Payment.objects.create(
            customer=customer,
            payment_date=timezone.now(),
            amount=amount,
        )

        # ✅ Update customer status to Approved
        customer.status = 1  # 1 = Approved
        customer.save(update_fields=["status"])

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'super_admin/customer_detail.html'
    context_object_name = 'customer'

class CustomerUpdateView(View):
    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)

        # Update related User fields
        customer.user.first_name = request.POST.get("first_name")
        customer.user.last_name = request.POST.get("last_name")
        customer.user.email = request.POST.get("email")
        customer.user.save()

        # Update Customer fields
        customer.contact_no = request.POST.get("contact_no")
        customer.age = request.POST.get("age")
        customer.gender = request.POST.get("gender")
        customer.father_name = request.POST.get("father_name")
        customer.mother_name = request.POST.get("mother_name")
        customer.father_job = request.POST.get("father_job")
        customer.mother_job = request.POST.get("mother_job")
        customer.married_sisters = request.POST.get("married_sisters")
        customer.married_brothers = request.POST.get("married_brothers")
        customer.caste = request.POST.get("caste")
        customer.marital_status = request.POST.get("marital_status")
        customer.star = request.POST.get("star")
        customer.dosham = request.POST.get("dosham")
        customer.dob = request.POST.get("dob")
        customer.time_birth = request.POST.get("time_birth")
        customer.place_birth = request.POST.get("place_birth")
        customer.height = request.POST.get("height")
        customer.weight = request.POST.get("weight")
        customer.complexion = request.POST.get("complexion")
        customer.physical_condition = request.POST.get("physical_condition")
        customer.education = request.POST.get("education")
        customer.job = request.POST.get("job")
        customer.company = request.POST.get("company")
        customer.job_department = request.POST.get("job_department")
        customer.job_city = request.POST.get("job_city")
        customer.income = request.POST.get("income")
        customer.address = request.POST.get("address")
        customer.house_name = request.POST.get("house_name")
        customer.street = request.POST.get("street")
        customer.city = request.POST.get("city")
        customer.district = request.POST.get("district")
        customer.post = request.POST.get("post")
        customer.pin_code = request.POST.get("pin_code")
        customer.description = request.POST.get("description")

        # Handle profile image if uploaded
        if "profile_image" in request.FILES:
            customer.profile_image = request.FILES["profile_image"]

        customer.save()

        return redirect("customer_detail", pk=customer.pk)


@login_required
def edit_profile(request):
    try:
        customer_profile = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('customer_dashboard')  

    user = request.user

    if request.method == 'POST':
        # Get data directly from the POST request
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.username = request.POST.get('email', user.username) # Update username with email
        user.save()
        
        if 'profile_image' in request.FILES:
            customer_profile.profile_image = request.FILES['profile_image']

        # Update Customer model fields from the POST data
        customer_profile.father_name = request.POST.get('father_name', customer_profile.father_name)
        customer_profile.age = request.POST.get('age') or customer_profile.age
        customer_profile.gender = request.POST.get('gender', customer_profile.gender)
        customer_profile.contact_no = request.POST.get('contact_no', customer_profile.contact_no)
        customer_profile.star = request.POST.get('star', customer_profile.star)
        customer_profile.marital_status = request.POST.get('marital_status', customer_profile.marital_status)
        customer_profile.education = request.POST.get('education', customer_profile.education)
        customer_profile.dosham = request.POST.get('dosham', customer_profile.dosham)

        customer_profile.description  = request.POST.get('description', customer_profile.description )
        customer_profile.address = request.POST.get('address', customer_profile.address)
        customer_profile.married_sisters = request.POST.get('married_sisters', customer_profile.married_sisters)
        customer_profile.married_brothers = request.POST.get('married_brothers', customer_profile.married_brothers)
        
        customer_profile.mother_job = request.POST.get('mother_job', customer_profile.mother_job)
        customer_profile.father_job = request.POST.get('father_job', customer_profile.father_job)
        customer_profile.mother_name = request.POST.get('mother_name', customer_profile.mother_name)
        customer_profile.income = request.POST.get('income', customer_profile.income)
        customer_profile.job_city = request.POST.get('job_city', customer_profile.job_city)
        customer_profile.job_department = request.POST.get('job_department', customer_profile.job_department)
        customer_profile.company = request.POST.get('company', customer_profile.company)
        customer_profile.job = request.POST.get('job', customer_profile.job)
        customer_profile.caste = request.POST.get('caste', customer_profile.caste)
        customer_profile.marital_status = request.POST.get('marital_status', customer_profile.marital_status)
        customer_profile.physical_condition = request.POST.get('physical_condition', customer_profile.physical_condition)
        customer_profile.weight = request.POST.get('weight', customer_profile.weight)
        customer_profile.complexion = request.POST.get('complexion', customer_profile.complexion)
        customer_profile.height = request.POST.get('height', customer_profile.height)
        customer_profile.time_birth = request.POST.get('time_birth', customer_profile.time_birth)
        customer_profile.place_birth = request.POST.get('place_birth', customer_profile.place_birth)
        customer_profile.dob = request.POST.get('dob', customer_profile.dob)
        customer_profile.district = request.POST.get('district', customer_profile.district)
        customer_profile.city = request.POST.get('city', customer_profile.city)
        customer_profile.post = request.POST.get('post', customer_profile.post)
        customer_profile.pin_code = request.POST.get('pin_code', customer_profile.pin_code)
        customer_profile.street = request.POST.get('street', customer_profile.street)
        customer_profile.house_name = request.POST.get('house_name', customer_profile.house_name)

        customer_profile.save()
        
        messages.success(request, "Your profile has been updated successfully!")
        return redirect('edit_profile')

    context = {
        'customer_profile': customer_profile,
        'user': user,
    }
    return render(request, 'customer_dashboard/edit_profile.html', context)

@login_required
def send_interest(request):
    # This check ensures it's an AJAX POST request, which is a good practice.
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        receiver_id = request.POST.get('receiver_id')
        
        if not receiver_id:
            # Return a JSON error response
            return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)
            
        try:
            receiver_profile = get_object_or_404(Customer, id=receiver_id)
            sender_profile = request.user.customer_profile
            
            # Check if interest already exists
            if Interest.objects.filter(sender=sender_profile, receiver=receiver_profile).exists():
                return JsonResponse({'status': 'info', 'message': 'Interest already sent.'})
            
            # Create the interest record
            Interest.objects.create(sender=sender_profile, receiver=receiver_profile)
            
            # Return a JSON success response
            return JsonResponse({'status': 'success', 'message': 'Interest sent successfully!'})
            
        except Customer.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Profile not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    # If the request is not a POST or not an AJAX request, return a generic error.
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


# -----------------MATCHING PROFILE VIEW---------------
@login_required
def matching_profiles(request):
    logged_in_customer = Customer.objects.get(user=request.user)
    user_caste = logged_in_customer.caste
    user_gender = logged_in_customer.gender
    
    if user_gender == 'Male':
        opposite_gender = 'Female'
    elif user_gender == 'Female':
        opposite_gender = 'Male'
    else:
        opposite_gender = None
        
    matching_profiles = []
    
    if opposite_gender:
        matching_profiles = Customer.objects.filter(
            Q(caste=user_caste) & Q(gender=opposite_gender)
        ).exclude(user=request.user)
    
    # Get a list of IDs for all customers the logged-in user has sent interest to
    sent_interest_ids = Interest.objects.filter(sender=logged_in_customer).values_list('receiver__id', flat=True)
        
    context = {
        'matching_profiles': matching_profiles,
        'logged_in_customer': logged_in_customer,
        'sent_interest_ids': sent_interest_ids,  # Pass the list of IDs to the template
    }
    return render(request, 'customer_dashboard/matching_profiles.html', context)

# -----------------ABOUT US ADD VIEW---------------
def about_us_add(request):
    if request.method == "POST":
        main_title = request.POST.get("main_title")
        mission = request.POST.get("mission")
        affiliation = request.POST.get("affiliation")
        history = request.POST.get("history")
        is_active = bool(int(request.POST.get("is_active", 1)))

        about = AboutUs.objects.create(
            main_title=main_title,
            mission=mission,
            affiliation=affiliation,
            history=history,
            is_active=is_active
        )

        images = request.FILES.getlist("images[]")
        designations = request.POST.getlist("designations[]")

        for img_file, desig in zip(images, designations):
            AboutUsImage.objects.create(
                about_us=about,
                image=img_file,
                designation=desig,
                is_active=True
            )

        return redirect("about-us-list")  # replace with your list page name

    return redirect("about-us-list")

# -----------------ABOUT US LIST VIEW---------------   
def about_us_list(request):
    # Fetch all active AboutUs entries with only active images
    about_entries = AboutUs.objects.filter(is_active=True).prefetch_related(
        Prefetch(
            "images",
            queryset=AboutUsImage.objects.filter(is_active=True),
            to_attr="active_images"
        )
    )

    return render(
        request,
        "super_admin/about_us.html",
        {"about_entries": about_entries},
    )

# -----------------ABOUT US DELETE VIEW---------------   


def about_us_image_delete(request, pk):
    if request.method == "POST":
        image = get_object_or_404(AboutUsImage, pk=pk)
        image.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

# -----------------BANNER LIST VIEW---------------
def banner_list_view(request):
    banners = Banners.objects.filter(is_active=True).order_by("-id")
    return render(request, "super_admin/banner.html", {"banners": banners})

# -----------------BANNER ADD VIEW---------------
def banner_add_view(request):
    if request.method == "POST":
        banner_image = request.FILES.get("banner_image")
        banner_text1 = request.POST.get("banner_text1")
        banner_text2 = request.POST.get("banner_text2")
        banner_text3 = request.POST.get("banner_text3")
        status = request.POST.get("status") or 1

        Banners.objects.create(
            banner_image=banner_image,
            banner_text1=banner_text1,
            banner_text2=banner_text2,
            banner_text3=banner_text3,
            status=status
        )
        messages.success(request, "Banner added successfully!")
        return redirect("banner-list")    

# -----------------BANNER EDIT VIEW---------------
def banner_edit(request, pk):
    banner = get_object_or_404(Banners, pk=pk)
    if request.method == "POST":
        banner.banner_text1 = request.POST.get("banner_text1")
        banner.banner_text2 = request.POST.get("banner_text2")
        banner.banner_text3 = request.POST.get("banner_text3")
        banner.status = request.POST.get("status")
        if request.FILES.get("banner_image"):
            banner.banner_image = request.FILES.get("banner_image")
        banner.save()
        return redirect("banner-list")  # redirect to the banner table page

    return redirect("banner-list")

# -----------------BANNER DELETE VIEW---------------
def banner_delete(request, pk):
    banner = get_object_or_404(Banners, pk=pk)
    banner.is_active = False  # soft delete
    banner.save()
    return redirect('banner-list') 

# -----------------CONTACT VIEW---------------
def contact(request):
    return render(request, "accounts/contact.html")

# -----------------PRIVACY POLICY VIEW---------------    
def privacy_policy(request):
    return render(request, "accounts/privacy_policy.html")

# -----------------TERMS VIEW---------------
def terms(request):
    return render(request, "accounts/terms.html")


def charity_view(request):
    """
    Display all charity items.
    """
    charities = CharityManagement.objects.all()  # Get all charity entries
    return render(request, "accounts/charity.html", {"charities": charities})

def about(request):
    about_us = AboutUs.objects.first()  
    images = about_us.images.all() if about_us else []  

    context = {
        "about_us": about_us,
        "images": images,
    }

    return render(request, "accounts/about.html", context)

def home(request):
    latest_banner = Banners.objects.filter(status=1).order_by("-id").first()
    latest_news = NewsEvents.objects.filter(status=1).order_by("-id")[:3]  # latest 3 news

    return render(
        request,
        "accounts/index.html",
        {
            "banner": latest_banner,
            "news_articles": latest_news,
        },
    )



@login_required
def customer_list(request):
    customers = Customer.objects.select_related('user').all()  # fetch related user
    return render(request, 'super_admin/customers.html', {'customers': customers})



@login_required
def customer_dashboard(request):
    # Ensure the logged-in user is a customer
    if not hasattr(request.user, "customer_profile"):
        return redirect("login")  # redirect non-customers to login or error page

    customer = request.user.customer_profile  # get Customer object
    return render(request, "customer_dashboard/dashboard.html", {"customer": customer})


def customer_login(request):
    if request.method == "POST":
        identifier = request.POST.get("email_or_mobile")
        password = request.POST.get("password")

        # The authenticate function will now check all configured backends
        user = authenticate(request, identifier=identifier, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.email}!")
            return redirect("customer_dashboard")
        else:
            messages.error(request, "Invalid email/phone or password.")

    return render(request, "customer/login.html")

def register_customer(request):
    if request.method == "POST":
        # Get form values
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        mobile = request.POST.get("mobile", "").strip()
        
        # Get first_name and last_name from the form
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()

        # Required field validation
        if not email or not password or not mobile or not first_name:
            messages.error(request, "Email, password, first name, and mobile are required.")
            return redirect("register_customer")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register_customer")

        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect("register_customer")

        try:
            last_customer = Customer.objects.latest('id')
            # Check if id_proof is not None and is a valid number string
            if last_customer.id_proof and last_customer.id_proof.isdigit():
                next_id_proof = int(last_customer.id_proof) + 1
            else:
                next_id_proof = 1
        except Customer.DoesNotExist:
            next_id_proof = 1   

        # Create User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            is_active=True,
            # Pass the first and last name here
            first_name=first_name,
            last_name=last_name
        )

        # Create Customer profile
        Customer.objects.create(
            user=user,
            father_name=request.POST.get("father_name"),
            age=request.POST.get("age") or None,
            gender=request.POST.get("gender"),
            contact_no=mobile,
            description=request.POST.get("expectation"),
            profile_image=request.FILES.get("profile_image"),
            id_proof=str(next_id_proof),
            address=request.POST.get("current_address"),
            star=request.POST.get("customer_star") or None,
            married_sisters=request.POST.get("married_sisters"),
            married_brothers=request.POST.get("married_brothers"),
            no_sisters=request.POST.get("num_sisters"),
            no_brothers=request.POST.get("num_brothers"),
            mother_job=request.POST.get("mother_job"),
            father_job=request.POST.get("father_job"),
            mother_name=request.POST.get("mother_name"),
            landline_no=request.POST.get("landline_no") or None,
            year=request.POST.get("year"),
            school=request.POST.get("school"),
            education=request.POST.get("education"),
            income=request.POST.get("monthly_income"),
            job_city=request.POST.get("job_city"),
            job_department=request.POST.get("job_sector"),
            company=request.POST.get("company"),
            job=request.POST.get("job"),
            caste=request.POST.get("caste"),
            marital_status=request.POST.get("marital_status"),
            physical_condition=request.POST.get("physical_condition"),
            weight=request.POST.get("weight"),
            complexion=request.POST.get("complexion"),
            height=request.POST.get("height"),
            time_birth=request.POST.get("birth_time"),
            place_birth=request.POST.get("birth_place"),
            dob=request.POST.get("dob"),
            district=request.POST.get("district"),
            city=request.POST.get("city"),
            post=request.POST.get("post"),
            pin_code=request.POST.get("pincode"),
            street=request.POST.get("street"),
            house_name=request.POST.get("house_name"),
            dosham=request.POST.get("dosham"),
            status=0,  # default pending
            is_active=True,
            created=None,
            updated=None
        )

        messages.success(request, "Customer registered successfully!")
        return redirect("register_customer")

    
    context = {
        "CASTE_CHOICES": Customer.CASTE_CHOICES,
        "MARITAL_STATUS_CHOICES": Customer.MARITAL_STATUS_CHOICES,
        "STAR_CHOICES": Customer.STAR_CHOICES,
    }
    return render(request, "customer/register.html", context) 


def news_delete(request, pk):
    news = get_object_or_404(NewsEvents, id=pk)
    
    # Delete the image file if it exists
    if news.image:
        image_path = news.image.path
        if os.path.isfile(image_path):
            os.remove(image_path)
    
    # Delete the database record
    news.delete()
    
    return redirect('news_list')

def news_update(request):
    if request.method == "POST":
        news_id = request.POST.get("news_id")
        news = NewsEvents.objects.get(id=news_id)
        news.title = request.POST.get("title")
        news.content = request.POST.get("content")
        news.status = request.POST.get("status", 1)

        if request.FILES.get("image"):
            news.image = request.FILES.get("image")
        news.save()
        return redirect('news_list')
    return redirect('news_list')

def news_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        status = request.POST.get("status", 1)
        image = request.FILES.get("image")

        NewsEvents.objects.create(
            title=title,
            content=content,
            status=status,
            image=image
        )
        return redirect('news_list')  # reload page after adding
    return redirect('news_list')

def news_list(request):
    news_list = NewsEvents.objects.all().order_by('-id')  # latest first
    return render(request, 'super_admin/news.html', {'news_list': news_list})

# ------------SUPERADMIN LOGOUT------------
def custom_admin_logout(request):
    logout(request)
    return redirect("super_admin_login")

# ------------SUPERADMIN LOGIN------------
def custom_admin_login(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        return redirect("super_admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember = request.POST.get("remember")

        user = authenticate(request, username=username, password=password)
        print("AUTH RESULT:", user)
        if user is not None:
            login(request, user)
            
            if not remember:
                request.session.set_expiry(0)

            if user.is_superadmin:
                return redirect("super_admin_dashboard")
            else:
                return redirect("super_admin_dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("super_admin_login")
    
    return render(request, "super_admin/login.html")


# ------------SUPERADMIN DASHBOARD------------
@login_required(login_url="super_admin_login")
def custom_admin_dashboard(request):
    total_customers = Customer.objects.count()

    # Fetch Total Published News
    published_news = NewsEvents.objects.filter(status=1).count()

    # Fetch Active Banners
    active_banners = Banners.objects.filter(status=1).count()

    # Fetch Total Revenue
    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_customers': total_customers,
        'published_news': published_news,
        'active_banners': active_banners,
        'total_revenue': total_revenue,
    }
    return render(request, "super_admin/dashboard.html", context)  


# ------------CHARITY MANAGEMENT------------
def charity_management(request):
    if request.method == "POST":
        charity_id = request.POST.get("charity_id")
        title = request.POST.get("title")
        is_active = True if request.POST.get("is_active") else False
        image = request.FILES.get("image")

        if charity_id:  # UPDATE existing
            charity = get_object_or_404(CharityManagement, id=charity_id)
            charity.title = title
            charity.is_active = is_active
            if image:  # replace only if a new image is uploaded
                charity.image = image
            charity.save()
        else:  # CREATE new
            CharityManagement.objects.create(
                title=title,
                is_active=is_active,
                image=image
            )

        return redirect("charity_management")  # reload same page to reflect changes

    charities = CharityManagement.objects.all().order_by("-id")
    return render(request, "super_admin/charity.html", {"charities": charities})


def charity_delete(request, pk):
    charity = get_object_or_404(CharityManagement, pk=pk)
    charity.delete()
    return redirect("charity_management")

