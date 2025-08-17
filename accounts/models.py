from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# -----------------CHARITY MODEL---------------
class CharityManagement(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="charity/")
    is_active= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.title

# -----------------ABOUT US MODEL---------------
class AboutUs(models.Model):
    mission = models.TextField()
    affiliation = models.TextField()
    history = models.TextField()
    main_title = models.CharField(max_length=255, default="Administration Team")
    is_active= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.main_title

# -----------------ABOUT US IMAGE MODEL---------------
class AboutUsImage(models.Model):
    about_us = models.ForeignKey(
        AboutUs, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="about/")
    designation = models.CharField(max_length=255, blank=True, null=True)  
    is_active= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.designation or 'Image'} for {self.about_us.main_title}"


# ---------------NEWSEVENTS MODEL---------------
class NewsEvents(models.Model):
    STATUS_CHOICES = (
        (0, "Inactive"),
        (1, "Active"),
    )

    title = models.CharField(max_length=120)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    is_active= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.title


# ---------------BANNER MODEL---------------
class Banners(models.Model):
    STATUS_CHOICES = (
        (0, "Inactive"),
        (1, "Active"),
    )

    banner_image = models.ImageField(upload_to="banner/", max_length=255)
    banner_text1 = models.CharField(max_length=100, blank=True, null=True)
    banner_text2 = models.CharField(max_length=250, blank=True, null=True)
    banner_text3 = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    is_active= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.banner_text1 or f"Banner {self.id}"


   
# ---------------USER MODEL---------------
class User(AbstractUser):
    is_superadmin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# ---------------SUPER-ADMIN MODEL---------------
class SuperAdmin(models.Model):
    user = models.OneToOneField(User, related_name="super_admin", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# -----------------CUSTOMER MODEL---------------
class Customer(models.Model):
    user = models.OneToOneField(User, related_name="customer_profile", on_delete=models.CASCADE, blank=True, null=True)

    CASTE_CHOICES = (
        ("Mudaliar", "Mudaliar"),
        ("Chetty", "Chetty"),
        ("Devanga", "Devanga"),
        ("Ezhavas_Thiyas", "Ezhavas & Thiyas"),
        ("Thandan", "Thandan"),
    )

    MARITAL_STATUS_CHOICES = (
        ("Single", "Single"),
        ("Divorced", "Divorced"),
    )

    STAR_CHOICES = (
        ("Aswathi", "Aswathi"),
        ("Bharani", "Bharani"),
        ("Karthika", "Karthika"),
        ("Rohini", "Rohini"),
        ("Makayiram", "Makayiram"),
        ("Thiruvathira", "Thiruvathira"),
        ("Punartham", "Punartham"),
        ("Pooyam", "Pooyam"),
        ("Aayilyam", "Aayilyam"),
        ("Makam", "Makam"),
        ("Pooram", "Pooram"),
        ("Uthram", "Uthram"),
        ("Atham", "Atham"),
        ("Chittira", "Chittira"),
        ("Chothi", "Chothi"),
        ("Vishakam", "Vishakam"),
        ("Anizham", "Anizham"),
        ("Thiruketta", "Thiruketta"),
        ("Moolam", "Moolam"),
        ("Pooradam", "Pooradam"),
        ("Uthradam", "Uthradam"),
        ("Thiruvonam", "Thiruvonam"),
        ("Avittam", "Avittam"),
        ("Chathayam", "Chathayam"),
        ("Pooruruttathi", "Pooruruttathi"),
        ("Uthrattathi", "Uthrattathi"),
        ("Revathi", "Revathi"),
    )

    father_name = models.CharField(max_length=256, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=256, blank=True, null=True)
    contact_no = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/", null=True, blank=True)  
    id_proof = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    star = models.CharField(max_length=50, choices=STAR_CHOICES, blank=True, null=True)
    married_sisters = models.CharField(max_length=250, blank=True, null=True)
    married_brothers = models.CharField(max_length=250, blank=True, null=True)
    no_sisters = models.CharField(max_length=250, blank=True, null=True)
    no_brothers = models.CharField(max_length=250, blank=True, null=True)
    mother_job = models.CharField(max_length=250, blank=True, null=True)
    father_job = models.CharField(max_length=250, blank=True, null=True)
    mother_name = models.CharField(max_length=250, blank=True, null=True)
    landline_no = models.IntegerField(blank=True, null=True)
    year = models.CharField(max_length=250, blank=True, null=True)
    school = models.CharField(max_length=250, blank=True, null=True)
    education = models.CharField(max_length=250, blank=True, null=True)
    income = models.CharField(max_length=250, blank=True, null=True)
    job_city = models.CharField(max_length=250, blank=True, null=True)
    job_department = models.CharField(max_length=250, blank=True, null=True)
    company = models.CharField(max_length=250, blank=True, null=True)
    job = models.CharField(max_length=250, blank=True, null=True)
    caste = models.CharField(max_length=250, choices=CASTE_CHOICES, blank=True, null=True)
    marital_status = models.CharField(max_length=50, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    physical_condition = models.CharField(max_length=250, blank=True, null=True)
    weight = models.CharField(max_length=250, blank=True, null=True)
    complexion = models.CharField(max_length=250, blank=True, null=True)
    height = models.CharField(max_length=250, blank=True, null=True)
    time_birth = models.CharField(max_length=250, blank=True, null=True)
    place_birth = models.CharField(max_length=250, blank=True, null=True)
    dob = models.CharField(max_length=250, blank=True, null=True)
    district = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    post = models.CharField(max_length=250, blank=True, null=True)
    pin_code = models.CharField(max_length=250, blank=True, null=True)
    street = models.CharField(max_length=250, blank=True, null=True)
    house_name = models.CharField(max_length=250, blank=True, null=True)
    STATUS_CHOICES = (
        (0, "Pending"),   
        (1, "Approved"),  
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    is_active= models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    dosham = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username if self.user else "No User"


# -----------------PAYMENT MODEL---------------
class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="payments")
    payment_date = models.DateTimeField()
    amount = models.IntegerField()
    is_active= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.customer.user.username} - {self.amount}"


class Interest(models.Model):
    sender = models.ForeignKey(Customer, related_name='sent_interests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Customer, related_name='received_interests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('sender', 'receiver')
        
    def __str__(self):
        return f"{self.sender.user.username} is interested in {self.receiver.user.username}"