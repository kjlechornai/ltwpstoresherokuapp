from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.db.models import Q
from .forms import ReceiveModelForm, IssueModelForm, ItemModelForm
from .models import Item, Receive, Issue, Department

class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    paginate_by = 12

class ItemDetailView(DetailView):
    model = Item
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = context['object']
        cat = item.sub_category
        print(cat)
        context['related'] = Item.objects.filter(sub_category=cat)
        print(context['related'])
        return context
    

class ReceiveView(View):

    def get(self, request, *args, **kwargs):
        context = {'form':ReceiveModelForm()}
        return render(request, 'receive-form.html', context)

    def post(self, request, *args, **kwargs):
        form = ReceiveModelForm(request.POST)
        if form.is_valid():
            receive = form.save()  
        return redirect(reverse('item:receive'))

def is_valid_queryparam(param):
    return param != "" and param is not None

def display_received(request):
    departments = Department.objects.all()
    qs = Receive.objects.all().order_by('-receive_date')
    title = request.GET.get('title')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    department = request.GET.get('department')

    if is_valid_queryparam(title):
        # print(title)
        qs = qs.filter(item__name__icontains=title)

    if is_valid_queryparam(date_min):
        # print(date_min)
        qs = qs.filter(receive_date__gte=date_min)

    if is_valid_queryparam(date_max):
        # print(date_max)
        qs = qs.filter(receive_date__lt=date_max)

    if is_valid_queryparam(department):
        # print(department)
        qs = qs.filter(project__department__name__exact=department)
    
    context = {
        'receipts': qs,
        'departments':departments
    }
    return render(request, 'receive-list.html', context)

class IssueView(View):
    def get(self, request, *args, **kwargs):
        context = { 'form':IssueModelForm() }
        return render(request, 'issue-form.html', context)

    def post(self, request, *args, **kwargs):
        form = IssueModelForm(request.POST)
        if form.is_valid():
            # need to add some conditions
            # i. if item not in stock
            # ii. if not for the project
            issue = form.save()
        return redirect(reverse('item:issue'))

def display_issued(request):
    departments = Department.objects.all()
    qs = Issue.objects.all().order_by('-issue_date')
    title = request.GET.get('title')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    department = request.GET.get('department')

    if is_valid_queryparam(title):
        qs = qs.filter(item__name__icontains=title)

    if is_valid_queryparam(date_min):
        qs = qs.filter(issue_date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(issue_date__lt=date_max)

    if is_valid_queryparam(department):
        qs = qs.filter(project__department__name__exact=department)


    context = {
        'issuance': qs,
        'departments': departments
    }
    return render(request, 'issue-list.html', context)

class ItemCreateView(CreateView):
    template_name = 'item-create.html'
    form_class = ItemModelForm

def search(request):
    qs = Item.objects.all()
    title_contains = request.GET.get('title-contains')
    if title_contains != ' ' and title_contains is not None:
        qs = qs.filter(Q(name__icontains=title_contains) | Q(item_sage_id__icontains=title_contains)).distinct()
    
    # paginator = Paginator(qs, 12)  # Show 12 contacts per page
    # page = request.GET.get('page', 1)
    # try:
    #     qs = paginator.page(page)
    # except PageNotAnInteger:
    #     qs = paginator.page(1)
    # except EmptyPage:
    #     qs = paginator.page(paginator.num_pages)
    context = {
        'queryset': qs,
        'query': title_contains
    }
    return render(request, "search.html", context)


def plumbing(request):
    category_name = 'plumbing'
    qs = Item.objects.filter(category__name__exact=category_name)
    context = {
        'queryset': qs,
        'query': category_name
    }
    return render(request, "category/plumbing.html", context)

def technical(request):
    category_name = 'technical'
    qs = Item.objects.filter(category__name__exact=category_name)
    context = {
        'queryset': qs,
        'query': category_name
    }
    return render(request, "category/technical.html", context)

def hse(request):
    category_name = 'hse'
    qs = Item.objects.filter(category__name__exact=category_name)
    context = {
        'queryset': qs,
        'query': category_name
    }
    return render(request, "category/hse.html", context)

def electrical(request):
    category_name = 'electrical'
    qs = Item.objects.filter(category__name__exact=category_name)
    context = {
        'queryset': qs,
        'query': category_name
    }
    return render(request, "category/electrical.html", context)


def stationery(request):
    category_name = 'stationery'
    qs = Item.objects.filter(category__name__exact=category_name)
    context = {
        'queryset': qs,
        'query': category_name
    }
    return render(request, "category/stationery.html", context)

def tires(request):
    category_name = 'tires'
    qs = Item.objects.filter(category__name__exact=category_name)
    context = {
        'queryset': qs,
        'query': category_name
    }
    return render(request, "category/tires.html", context)

def ohl_project(request):
    project_name = 'ohl maintenance'
    pitems = Item.objects.filter(receive__project__name__exact=project_name).distinct()
    context = {
        'queryset': pitems,
        'project':project_name
    }
    return render(request, "project/ohl.html", context)

def camps_project(request):
    project_name = 'camps maintenance'
    pitems = Item.objects.filter(receive__project__name__exact=project_name).distinct()
    context = {
        'queryset': pitems,
        'project':project_name
    }
    return render(request, "project/camps.html", context)

def substation_project(request):
    project_name = 'substation maintenance'
    pitems = Item.objects.filter(receive__project__name__exact=project_name).distinct()
    context = {
        'queryset': pitems,
        'project':project_name
    }
    return render(request, "project/substation.html", context)

def vehicles_project(request):
    project_name = 'vehicles tyre maintenance'
    pitems = Item.objects.filter(receive__project__name__exact=project_name).distinct()
    context = {
        'queryset': pitems,
        'project':project_name
    }
    return render(request, "project/vehicle.html", context)

def hse_project(request):
    project_name = 'PPE and uniforms'
    pitems = Item.objects.filter(receive__project__name__exact=project_name).distinct()
    context = {
        'queryset': pitems,
        'project':project_name
    }
    return render(request, "project/ppe.html", context)

def communication_line_project(request):
    project_name = 'comms line maintenance'
    pitems = Item.objects.filter(receive__project__name__exact=project_name).distinct()
    context = {
        'queryset': pitems,
        'project':project_name
    }
    return render(request, "project/comms.html", context)

def general_technical_items(request):
    project_name = 'general technical maintenance'
    pitems = Item.objects.filter(receive__project__name__exact=project_name).distinct()
    context = {
        'queryset': pitems,
        'project':project_name
    }
    return render(request, "project/gen-technical.html", context)

def civil_works_projects(request):
    project_name = 'civil works'
    pitems = Item.objects.filter(receive__project__name__exact=project_name).distinct()
    context = {
        'queryset': pitems,
        'project':project_name
    }
    return render(request, "project/civil.html", context)

def winds_of_change(request):
    project_name = 'winds of change'
    pitems = Item.objects.filter(receive__project__name__exact=project_name).distinct()
    context = {
        'queryset': pitems,
        'project':project_name
    }
    return render(request, "project/woc.html", context)

def technical_department(request):
    dpt_name = 'technical'
    dept_items = Item.objects.filter(receive__project__department__name__exact=dpt_name).distinct()
    context = {
        'queryset': dept_items,
        'project':dpt_name
    }
    return render(request, "department/technical.html", context)

def civil_department(request):
    dpt_name = 'civil'
    dept_items = Item.objects.filter(receive__project__department__name__exact=dpt_name).distinct()
    context = {
        'queryset': dept_items,
        'project':dpt_name
    }
    return render(request, "department/civil.html", context)

def camps_department(request):
    dpt_name = 'camps & village'
    dept_items = Item.objects.filter(receive__project__department__name__exact=dpt_name).distinct()
    context = {
        'queryset': dept_items,
        'project':dpt_name
    }
    return render(request, "department/village.html", context)

def workshop_department(request):
    dpt_name = 'workshop'
    dept_items = Item.objects.filter(receive__project__department__name__exact=dpt_name).distinct()
    context = {
        'queryset': dept_items,
        'project':dpt_name
    }
    return render(request, "department/workshop.html", context)

def stores_department(request):
    dpt_name = 'stores'
    dept_items = Item.objects.filter(receive__project__department__name__exact=dpt_name).distinct()
    context = {
        'queryset': dept_items,
        'project':dpt_name
    }
    return render(request, "department/stores.html", context)

def admin_department(request):
    dpt_name = 'admin'
    dept_items = Item.objects.filter(receive__project__department__name__exact=dpt_name).distinct()
    context = {
        'queryset': dept_items,
        'project':dpt_name
    }
    return render(request, "department/admin.html", context)

def cl_department(request):
    dpt_name = 'community liaison'
    dept_items = Item.objects.filter(receive__project__department__name__exact=dpt_name).distinct()
    context = {
        'queryset': dept_items,
        'project':dpt_name
    }
    return render(request, "department/clo.html", context)

def technical_department(request):
    dpt_name = 'technical'
    dept_items = Item.objects.filter(receive__project__department__name__exact=dpt_name).distinct()
    context = {
        'queryset': dept_items,
        'project':dpt_name
    }
    return render(request, "department/technical.html", context)

def woc_department(request):
    dpt_name = 'woc'
    dept_items = Item.objects.filter(receive__project__department__name__exact=dpt_name).distinct()
    context = {
        'queryset': dept_items,
        'project':dpt_name
    }
    return render(request, "department/woc.html", context)

def security_department(request):
    dpt_name = 'security'
    dept_items = Item.objects.filter(receive__project__department__name__exact=dpt_name).distinct()
    context = {
        'queryset': dept_items,
        'project':dpt_name
    }
    return render(request, "department/security.html", context)

def hse_department(request):
    dpt_name = 'hse'
    dept_items = Item.objects.filter(receive__project__department__name__exact=dpt_name).distinct()
    context = {
        'queryset': dept_items,
        'project':dpt_name
    }
    return render(request, "department/hse.html", context)

def it_department(request):
    dpt_name = 'it'
    dept_items = Item.objects.filter(receive__project__department__name__exact=dpt_name).distinct()
    context = {
        'queryset': dept_items,
        'project':dpt_name
    }
    return render(request, "department/it.html", context)