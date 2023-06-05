import json
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from .forms import ThreadForm
from .models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


class ThreadListView(generic.ListView):
    model = Thread
    context_object_name = 'threads'
    template_name = 'threads/lists.html'
    # paginate_by = 50

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThreadListView, self).dispatch( *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ThreadListView, self).get_context_data(**kwargs)
        context['title'] = "Threads"

        return context

    def get_queryset(self, *args, **kwargs):
        """Filter data"""
        threads = Thread.objects.order_by('block')

        return threads


class ThreadDetailView(generic.DetailView):
    """View details"""
    model = Thread
    context_object_name = 'thread'
    template_name = 'threads/show.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThreadDetailView, self).dispatch( *args, **kwargs) 

    def get_context_data(self, *args, **kwargs):
        context = super(ThreadDetailView, self).get_context_data(**kwargs)
        context['title'] = "Thread"

        sub_threads = SubThread.objects.filter(thread_id=self.kwargs['pk']).order_by('view_id')
        context['sub_threads'] = sub_threads
        return context


def list_threads(request):
    """Lists threads"""
    uuid = request.GET.get("uuid")

    """threads"""
    threads = Thread.objects.order_by('block')

    arr_data = []
    for val in threads:
        data = {
            'id': val.id,
            'title': val.title,
            'label': val.label,
            'message_type': val.message_type
        }
        arr_data.append(data)

    """response"""
    return JsonResponse(arr_data, safe=False)

def list_responses(request):
    """Lists responses"""
    uuid = request.GET.get("uuid")

    """responses"""
    responses = SubThread.objects.filter(thread_id=uuid).order_by('view_id')

    arr_data = []
    for val in responses:
        data = {
            'id': val.id,
            'view_id': val.view_id,
            'title': val.title,
            'description': val.description,
        }
        arr_data.append(data)

    """response"""
    return JsonResponse(arr_data, safe=False)


def edit_response(request):
    """ response details"""
    uuid = request.GET.get("uuid")

    """response"""
    response = SubThread.objects.filter(pk=uuid).first()

    arr_data = {
        'id': response.id,
        'view_id': response.view_id,
        'title': response.title,
        'title_en': response.title_en_us,
        'description': response.description,
        'description_en': response.description_en_us,
    }

    """response"""
    return JsonResponse(arr_data, safe=False)


def detail_response(request):
    """ response details"""
    uuid = request.GET.get("uuid")

    #response
    thread = Thread.objects.filter(pk=uuid).first()

    #render view
    return render(request, 'threads/linking.html', {'thread': thread})   


def create_response(request):
    """create new response"""
    if request.method == 'POST':
        post_data = json.loads(request.body)
        action = post_data['action']

        message = ""
        if action == 'create':
            new_sub                   = SubThread()
            new_sub.title             = post_data['title']
            new_sub.title_en_us       = post_data['title_en']
            new_sub.description       = post_data['description']
            new_sub.description_en_us = post_data['description_en']
            new_sub.view_id           = post_data['view_id']
            new_sub.thread_id         = post_data["thread_id"]
            new_sub.save()

            #response message
            message = "Response created"

        elif action == 'edit':
            response_id = post_data['response_id']
            sub_thread  = SubThread.objects.get(pk=response_id)
            sub_thread.title             = post_data['title']
            sub_thread.title_en_us       = post_data['title_en']
            sub_thread.description       = post_data['description']
            sub_thread.description_en_us = post_data['description_en']
            sub_thread.view_id           = post_data['view_id']
            sub_thread.save()

            #response message
            message = "Response updated"
        
        """return response"""
        return JsonResponse({"error": False, "success_msg": message} , safe=False)


def delete_response(request):
    """delete response"""
    uuid = request.GET.get("uuid")

    #response
    response = SubThread.objects.filter(pk=uuid)

    if response.count() > 0:
        response.delete()

        #delete linking if available
        ThreadLink.objects.filter(sub_thread_id=uuid).delete()

    """response"""
    return JsonResponse({"error": False, "success_msg": "Response deleted"}, safe=False)   


class ThreadCreateView(generic.CreateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThreadCreateView, self).dispatch( *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'form': ThreadForm()}
        return render(request, 'threads/create.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        if form.is_valid():
            dt_menu = form.save(commit=False)
            dt_menu.created_by = request.user
            dt_menu.save()

            messages.success(request, 'Thread created')
            return HttpResponseRedirect(reverse_lazy('threads:lists'))
        return render(request, 'threads/create.html', {'form': form})  


class ThreadUpdateView(generic.UpdateView):
    """View to update"""
    model = Thread
    context_object_name = 'thread'
    form_class = ThreadForm
    template_name = 'threads/edit.html'

    def form_valid(self, form):
        dt_menu = form.save(commit=False)
        dt_menu.updated_by = self.request.user
        dt_menu.save()

        messages.success(self.request, 'Thread updated')
        return HttpResponseRedirect(reverse_lazy('threads:lists')) 


class ThreadDeleteView(generic.DeleteView):
    """View to delete a """ 
    model = Thread
    template_name = "threads/confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Thread deleted")
        return reverse_lazy('threads:lists') 


class SubThreadDeleteView(generic.DeleteView):
    """View to delete a sub thread""" 
    model = SubThread
    template_name = "threads/confirm_delete.html"

    def get_success_url(self, ):
        messages.success(self.request, "Sub thread deleted")
        return reverse_lazy('threads:lists') 



class ThreadLinkListView(generic.ListView):
    """Thread Links Crud Operation"""
    model = ThreadLink
    context_object_name = 'thread_links'
    template_name = 'thread_links/lists.html'
    # paginate_by = 50

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThreadLinkListView, self).dispatch( *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ThreadLinkListView, self).get_context_data(**kwargs)
        context['title'] = "Thread Links"
        context['threads'] = Thread.objects.order_by('block')

        thread_links = ThreadLink.objects.order_by("thread__block").all()
        context['thread_links'] = thread_links

        return context

    def post(self, request):
        """create/updating thread link data"""
        thread_id = request.POST.get('thread_id')
        link_id = request.POST.get('link_id')

        sub_thread_id = None
        if request.POST.get('sub_thread_id') != '':
            sub_thread_id = request.POST.get('sub_thread_id')

        """update or create menu link"""
        thread_link, created = ThreadLink.objects.update_or_create(
            thread_id=thread_id, sub_thread_id=sub_thread_id, 
            defaults={"link_id" : link_id})
        
        #message
        messages.success(request, 'Thread tree created/update!')

        #redirect
        return HttpResponseRedirect(reverse_lazy('threads:links'))


def current_links(request):
    """Current Links"""
    uuid = request.GET.get("uuid")

    thread_links = ThreadLink.objects.filter(thread_id=uuid).order_by('sub_thread__view_id')


    arr_data = []
    for val in thread_links:
        if val.linking_type == 'THREAD_THREAD' or val.linking_type == 'RESPONSE_THREAD':
            title = val.link.title
        elif val.linking_type == 'RESPONSE_API':
            title = val.api_url    

        #create set
        data = {
            'id': val.id,
            'view_id': val.sub_thread.view_id if val.sub_thread else "A",
            'customer_type': val.customer_type,
            'title': val.sub_thread.title if val.sub_thread else "Any Text",
            'link': f"{title}",
        }
        arr_data.append(data)

    """response"""
    return JsonResponse(arr_data, safe=False)


def link_thread2thread(request):
    """Linking Thread 2 Thread"""  
    if request.method == 'POST':
        post_data = json.loads(request.body)
        thread_id = post_data['thread_id'] 
        customer_type = post_data['customer_type'] 
        link_id = post_data['link_id']  

        """update or create menu link"""
        thread_link, created = ThreadLink.objects.update_or_create(
            thread_id=thread_id, customer_type=customer_type,
            defaults={"link_id": link_id, "linking_type": "THREAD_THREAD"})

    """response"""
    return JsonResponse({"error": False, "success_msg": "Thread 2 Thread linked"}, safe=False) 


def link_response2thread(request):
    """Linking Response 2 Thread"""  
    if request.method == 'POST':
        post_data = json.loads(request.body)
        thread_id = post_data['thread_id']  
        response_id = post_data['response_id'] 
        customer_type = post_data['customer_type']
        link_id = post_data['link_id']  

        """update or create menu link"""
        thread_link, created = ThreadLink.objects.update_or_create(
            thread_id=thread_id, sub_thread_id=response_id, customer_type=customer_type, 
            defaults={"link_id" : link_id, "linking_type": "RESPONSE_THREAD"})

    """response"""
    return JsonResponse({"error": False, "success_msg": "Response 2 Thread linked"}, safe=False)  


def link_response2API(request):
    """Linking Response 2 API"""  
    if request.method == 'POST':
        post_data = json.loads(request.body)
        thread_id = post_data['thread_id'] 
        response_id = post_data['response_id']  
        customer_type = post_data['customer_type']
        api_type = post_data['api_type']  
        api_url = post_data['api_url']  

        """update or create thread link"""
        thread_link, created = ThreadLink.objects.update_or_create(
            thread_id=thread_id, sub_thread_id=response_id, customer_type=customer_type, 
            defaults={"api_type": api_type, 'api_url': api_url, "linking_type": "RESPONSE_API"})

    """response"""
    return JsonResponse({"error": False, "success_msg": "Response 2 API linked"}, safe=False)  
        
        

def delete_link(request):
    """delete response"""
    uuid = request.GET.get("uuid")

    #link
    thread_link = ThreadLink.objects.filter(pk=uuid)

    if thread_link.count() > 0:
        thread_link.delete()

    """response"""
    return JsonResponse({"error": False, "success_msg": "Thread link deleted"}, safe=False)   

class ThreadLinkDeleteView(generic.DeleteView):
    """Delete a thread link""" 
    model = ThreadLink
    template_name = "thread_links/confirm_delete.html"

    def get_success_url(self):
        """message"""
        messages.success(self.request, "Thread link deleted successfully")
        return reverse_lazy('threads:links') 


def get_threads(request, *args, **kwargs):
    if request.method == 'GET':
        threads = Thread.objects.all().order_by('step')

        return render(None, 'threads/select.html', {'threads': threads})


def get_sub_threads(request, *args, **kwargs):
    if request.method == 'GET':
        thread_id = kwargs['thread_id']
        sub_threads = SubThread.objects.filter(thread_id=thread_id).order_by('view_id')

        return render(None, 'threads/select2.html', {'sub_threads': sub_threads})


"""privacy policy"""
def privacy_policy(request):
    """render view"""
    return render(request, "threads/privacy_policy.html", {})











