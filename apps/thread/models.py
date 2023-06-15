from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Thread(models.Model):
    """Thread Model"""
    ACTION_URL_OPTIONS = (
        ('REGISTRATION', 'REGISTRATION'),
        ('VERIFICATION', 'VERIFICATION'),
        ('PUSH', 'PUSH'),
        ('PULL', 'PULL'),
    )

    MESSAGE_TYPE_OPTIONS = (
        ('TEXT', 'TEXT'),
        ('DOCUMENT', 'DOCUMENT'),
        ('IMAGE', 'IMAGE'),
        ('AUDIO', 'AUDIO'),
        ('VIDEO', 'VIDEO'),
        ('CONTACT', 'CONTACT'),
        ('LOCATION', 'LOCATION'),
        ('LIST MESSAGE', 'LIST MESSAGE'),
        ('REPLY BUTTON', 'REPLY BUTTON'),
    )

    VALIDATION_RULES_OPTIONS = (
        ('REQUIRED', 'REQUIRED'),
        ('NUMERIC', 'NUMERIC'),
        ('EMAIL', 'EMAIL'),
        ('PHONE', 'PHONE'),
        ('NIN', 'NIN'),
        ('DL', 'DRIVER LICENCE'),
        ('DL_NIN', 'DRIVER LICENCE or NIN'),
        ('VEHICLE_NUMBER', 'VEHICLE NUMBER'),
        ('DATE', 'DATE'),
        ('TIME', 'TIME'),
        ('API', 'API'),
    )

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    block          = models.FloatField(default=0)
    title          = models.TextField(blank=False, null=False)
    db_flag        = models.CharField(max_length=50, blank=False, null=False)
    label          = models.CharField(max_length=50, blank=True, null=True)
    validation     = models.CharField(max_length=200, choices=VALIDATION_RULES_OPTIONS,  blank=True, null=True)
    validation_url = models.CharField(max_length=200, blank=True, null=True)
    action         = models.CharField(max_length=20, choices=ACTION_URL_OPTIONS, blank=True, null=True)
    action_url     = models.CharField(max_length=200, blank=True, null=True)
    payload        = models.TextField(blank=True, null=True)
    message_type   = models.CharField(max_length=20, choices=MESSAGE_TYPE_OPTIONS, blank=False, null=False, default="TEXT")
    main_thread    = models.BooleanField(default=False)      
    created_at     = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at     = models.DateTimeField(auto_now=True) 
    created_by     = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    updated_by     = models.ForeignKey(User, related_name="updated_by", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'lb_threads'
        verbose_name_plural = 'Thread'

    def __str__(self):
        return self.title
    

class SubThread(models.Model):
    """Sub Thread Model"""
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread       = models.ForeignKey(Thread, on_delete=models.CASCADE)
    view_id      = models.CharField(max_length=10, blank=False, null=False)
    created_at   = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at   = models.DateTimeField(auto_now=True) 
    title        = models.TextField(blank=False, null=False)
    description  = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'lb_sub_threads'
        verbose_name_plural = 'Sub Threads'

    def __str__(self):
        return self.title 
    

class ThreadLink(models.Model):
    """Thread Link Model"""
    LINKING_OPTIONS = (
        ('THREAD_THREAD', 'Thread 2 Thread'),
        ('RESPONSE_THREAD', 'Response 2 Thread'),
        ('RESPONSE_API', 'Response 2 API'),
    )

    REGISTRATION_OPTIONS = (
        ('ANY', 'Any User'),
        ('REGISTERED', 'Registered'),
        ('NOT_REGISTERED', 'Not Registered'),
    )

    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread        = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread')
    linking_type  = models.CharField(max_length=100, choices=LINKING_OPTIONS, default="THREAD_THREAD")
    customer_type = models.CharField(max_length=100, choices=REGISTRATION_OPTIONS, default="ANY")
    sub_thread    = models.ForeignKey(SubThread, on_delete=models.SET_NULL, blank=True, null=True)
    link          = models.ForeignKey(Thread, on_delete=models.SET_NULL, related_name='link', blank=True, null=True)
    api_type      = models.CharField(max_length=100, null=True, blank=True)
    api_url       = models.CharField(max_length=250, null=True, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at    = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'lb_thread_links'
        verbose_name_plural = 'Thread Links' 


class ThreadSession(models.Model):
    """Thread Session Model"""
    CHANNEL_OPTIONS = (
        ('WHATSAPP', 'Whatsapp'),
    )

    id          =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code        =  models.CharField(max_length=100, blank=True, null=True)
    phone       =  models.CharField(max_length=20, blank=True, null=True)
    channel     =  models.CharField(max_length=50, choices=CHANNEL_OPTIONS, blank=False, null=False, default='WHATSAPP')  
    thread      =  models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True)
    flag        =  models.CharField(max_length=100, blank=True, null=True)
    values      =  models.TextField(blank=True, null=True)
    facebook_id =  models.TextField(blank=True, null=True)
    active      =  models.IntegerField(blank=False, null=False, default=0)
    created_at  =  models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at  =  models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'lb_thread_sessions'
        verbose_name_plural = 'Thread Sessions' 


class Customer(models.Model): 
    ID_TYPE_OPTIONS = (
        ('NIN', 'NIN'),
        ('DL', 'DRIVER LICENCE'),
        ('VID', 'VOTE ID'),
    )

    STATUS_OPTIONS = (
        ('PENDING', 'PENDING'),
        ('COMPLETED', 'COMPLETED'),
        ('VALID', 'VALID'),
        ('INVALID', 'INVALID'),
    )
  
    phone             = models.CharField(max_length=20, blank=False, null=False, unique = True)
    phone2             = models.CharField(max_length=20, blank=True, null=True)
    id_type           = models.CharField(max_length=50, choices=ID_TYPE_OPTIONS, blank=True, null=True)
    id_number         = models.CharField(max_length=50, blank=True, null=True) 
    status            = models.CharField(max_length=20, choices=STATUS_OPTIONS,default='PENDING', blank=True, null=True)
    created_at        = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at        = models.DateTimeField(auto_now=True)  

    class Meta:
        db_table     = 'lb_customers'
        managed      = True
        verbose_name = 'Customer'
        verbose_name_plural = 'Customer'

    def __str__(self):
        return str(self.phone)
    

class CustomerLanguage(models.Model): 
    LANGUAGE_OPTIONS = (
        ('SW', 'Swahili'),
        ('EN', 'English'),
    )
  
    phone             = models.CharField(max_length=20, blank=False, null=False, unique = True)
    language          = models.CharField(max_length=20, choices=LANGUAGE_OPTIONS,default='SW', blank=True, null=True)
    created_at        = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at        = models.DateTimeField(auto_now=True)  

    class Meta:
        db_table     = 'lb_customer_languages'
        managed      = True
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return str(self.phone)
    



