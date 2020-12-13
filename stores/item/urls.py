from django.urls import path
from .views import (
    search, HomeView, ReceiveView, ItemDetailView, IssueView, display_received, display_issued,  
    ItemCreateView, plumbing, technical, hse, electrical, stationery, tires,
    ohl_project, camps_project, substation_project, vehicles_project, hse_project, communication_line_project,
    general_technical_items, civil_works_projects, winds_of_change,
    technical_department, civil_department, camps_department, workshop_department, stores_department,
    admin_department, cl_department, woc_department, hse_department, it_department, security_department
)
app_name = 'item'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('detail/<slug>', ItemDetailView.as_view(), name='detail'),
    path('item-add/', ItemCreateView.as_view(), name='item-add'),
    path('receive/', ReceiveView.as_view(), name='receive'),
    path('receive-list', display_received, name='receive-list'), 
    path('issue/', IssueView.as_view(), name='issue'),
    path('issue-list', display_issued, name='issue-list'),
    path('search/', search, name='search'),
    # categories
    path('plumbing/', plumbing, name='plumbing'),
    path('technical/', technical, name='technical'),
    path('electrical/', electrical, name='electrical'),
    path('hse/', hse, name='hse'),
    path('stationery/', stationery, name='stationery'),
    path('tires/', tires, name='tires'),
    # projects
    path('ohl-project/', ohl_project, name='ohl-project'),
    path('camps-project/', camps_project, name='camps-project'),
    path('substation-project/', substation_project, name='substation-project'),
    path('vehicle-tyre-project/', vehicles_project, name='vehicle-tyre-project'),
    path('ppe-uniform-project/', hse_project, name='ppe-uniform-project'),
    path('comm-line-project/', communication_line_project, name='comm-line-project'),
    path('general-technical-items/', general_technical_items, name='general-technical-items'),    
    path('civil-works-project/', civil_works_projects, name='civil-project'),
    path('woc-projects/', winds_of_change, name='woc-project'),
    # departments
    path('technical-department/', technical_department, name='technical-department'),
    path('civil-department/', civil_department, name='civil-department'),
    path('camps-department/', camps_department, name='camps-department'),
    path('workshop-department/', workshop_department, name='workshop-department'),
    path('stores-department/', stores_department, name='stores-department'),
    path('admin-department/', admin_department, name='admin-department'),
    path('cl-department/', cl_department, name='cl-department'),
    path('woc-department/', woc_department, name='woc-department'),
    path('hse-department/', hse_department, name='hse-department'),
    path('security-department/', security_department, name='security-department'),
    path('it-department/', it_department, name='it-department'),
]