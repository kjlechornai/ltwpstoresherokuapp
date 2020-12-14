from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.utils import timezone
from .models import Order, OrderItem, OrderPurpose, OrderIssued
from .forms import CheckoutForm, OrderIssueForm
from item.models import Item, Issue
import random
import string

# def create_ref_code():
#     return ''.join(random.choice(string.ascii_lowercase + string.digits,  k=20))

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, create = OrderItem.objects.get_or_create(
        user = request.user,
        item = item,
        ordered = False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order_item.item.get_total_balance > 0:
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, 'This item quantity was updated', fail_silently=True)
                return redirect('cart:order-summary')
            else:
                order.items.add(order_item)
                messages.info(request, 'This item was added to your order list', fail_silently=True)
                return redirect('cart:order-summary')
        else:
            messages.info(request, 'This item is not in stock', fail_silently=True)
            return redirect('/')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'This item was added to your order list',fail_silently=True)
        return redirect('cart:order-summary')
    
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(user=request.user, ordered=False, item=item)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, 'This item was removed from your order list', fail_silently=True)
            return redirect('cart:order-summary')
        else:
            messages.info(request, 'This item was not in your order list', fail_silently=True)
            return redirect('item:detail', slug=slug)
    else:
        messages.info(request, 'You do not have an active order', fail_silently=True)
        return redirect('item:detail', slug=slug)
   
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.", fail_silently=True)
            return redirect("cart:order-summary")
        else:
            messages.info(request, "This item was not in your cart", fail_silently=True)
            return redirect("item:detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order", fail_silently=True)
        return redirect("item:detail", slug=slug)   

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,                
            }
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("cart:checkout")

    def post(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm(self.request.POST or None)
            if form.is_valid():
                # add some conditions 
                order_purpse = OrderPurpose()
                order_purpse.purpose = form.cleaned_data['purpose']
                order_purpse.project_name = form.cleaned_data['project_name']
                order_purpse.collected_by = form.cleaned_data['collected_by']
                order_purpse.department = form.cleaned_data['department']
                order_purpse.user = self.request.user
                order_purpse.save()

                order.order_purpose = order_purpse
                
                order.save()
                messages.info(self.request, 'your order list has been send, collect items from store')
                # Mail
                mail_subject = 'test'
                mail_message = 'kindly process the attached requisition'
                mail_sender = 'kjlechornai@gmail.com' #self.request.user.email
                recipients = ['kjlechornai@gmail.com']
                send_mail(
                    mail_subject,
                    mail_message,
                    mail_sender,
                    recipients,
                    fail_silently=True
                )
                return redirect('/')
            messages.warning(self.request, 'Order list not send, fill all the required fields')
            return redirect('cart:checkout')         
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order, add items to your cart")
            return redirect("/")

class StoreIssueView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter(ordered=False).order_by('ordered_date')
            form = OrderIssueForm()
            context = {
                'form': form,
                'order': order[0],                
            }
            return render(self.request, "order-fulfillment.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "There are no active order")
            return redirect("/")

    def post(self, *args, **kwargs):
        try:
            order = Order.objects.filter(ordered=False).order_by('ordered_date')[0]
            form = OrderIssueForm(self.request.POST or None)
            if form.is_valid():
                # add some conditions 
                order_issued = OrderIssued()
                order_issued.issuer = form.cleaned_data['issuer']
                order_issued.location = form.cleaned_data['location']
                order_issued.save()                

                order.order_issued = order_issued
                order.ordered = True
                # order.ref_code = create_ref_code()

                order_items = order.items.all()
                order_items.update(ordered=True)  
                
                for item in order_items:
                    issue = Issue()
                    issue.item = item.item # item 
                    issue.quantity = item.quantity # quantity 
                    issue.purpose = order.order_purpose.purpose # purpose 
                    issue.issued_to = order.order_purpose.collected_by # issued_to 
                    issue.issue_type = 'online' # issue_type 
                    issue.project = order.order_purpose.project_name # project 
                    item.save()
                    issue.save()
             
                order.save()
                messages.info(self.request, 'You have issued successful')

                # def sender_mail(order_issued):
                #     if order_issued.issuer == 'kizito':
                #         mail_sender = 'kizito.lechornai@ltwp.co.ke'
                #     elif order_issued.issuer == 'celestine':
                #         mail_sender = 'celestine.galgitele@ltwp.co.ke'
                #     elif order_issued.issuer == 'jesire':
                #         mail_sender = 'jesire.leparsanti@ltwp.co.ke'
                #     return mail_sender

                # mail_subject = 'test'
                # mail_message = 'the requested items have been collected'
                # mail_recipients = [order.user.email, 'kizito.lechornai@ltwp.co.ke']
                # send_mail(
                #     mail_subject,
                #     mail_message,
                #     mail_sender,
                #     mail_recipients,
                #     fail_silently=False
                # )
                return redirect('/')
            messages.warning(self.request, 'Order not issued, fill all the required fields')
            return redirect('cart:order-fulfillment')         
        except ObjectDoesNotExist:
            messages.info(self.request, "There are no active order")
            return redirect("/")

        
