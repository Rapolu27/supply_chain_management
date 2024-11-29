from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Supplier, Product, PurchaseOrder, Inventory
from .forms import SupplierForm, ProductForm, PurchaseOrderForm
from scm_core.inventory_threshold import get_out_of_range_products, create_auto_purchase_orders
from scm_core import data_helper
from scm_core import reports_helper
import requests
import json
from django.http import JsonResponse
from datetime import datetime,date,timedelta


# Create your views here.
def home_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('postlogin') 
    return render(request, 'home/base.html')

def post_login_view(request):
    if is_scm_user(request.user):
        return redirect('user/dashboard')
    return redirect('/user/dashboard')

def is_scm_user(user):
    return user.groups.filter(name='SCM_USER').exists()

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier/list.html', {'suppliers': suppliers})

def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier added successfully!')
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    
    return render(request, 'supplier/form.html', {'form': form})

def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully!')
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    
    return render(request, 'supplier/form.html', {'form': form})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully!')
        return redirect('supplier_list')
    
    return render(request, 'supplier/delete.html', {'supplier': supplier})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'product/form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'product/form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    
    return render(request, 'product/delete.html', {'product': product})


def purchase_order_list(request):
    orders = PurchaseOrder.objects.all()
    return render(request, 'order/list.html', {'orders': orders})

def purchase_order_create(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_order_list')
    else:
        form = PurchaseOrderForm()
    return render(request, 'order/form.html', {'form': form})

def purchase_order_update(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('purchase_order_list')
    else:
        form = PurchaseOrderForm(instance=order)
    return render(request, 'order/form.html', {'form': form})

def purchase_order_delete(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('purchase_order_list')
    return render(request, 'order/delete.html', {'order': order})


def auto_generate_purchase_orders(request):
    out_of_range_products = None
    purchase_orders = None
    if request.method =='POST':
        # Fetch all inventory items
        inventory = Inventory.objects.all()
        # Get products out of range
        out_of_range_products = get_out_of_range_products(inventory)
        data_helper.filter_already_scheduled_po(PurchaseOrder, out_of_range_products)
        # Fetch default supplier for the purchase orders (or let the user select a supplier)
        suppliers = Supplier.objects.all()  # Replace with supplier selection logic
        # Create purchase orders for products below min stock
        purchase_orders = create_auto_purchase_orders(out_of_range_products, suppliers)
        # Save purchase orders to the database
        for po in purchase_orders:
            PurchaseOrder.objects.create(
                product_id=po["product_id"],
                supplier_id=po["supplier_id"],
                quantity=po["quantity"],
                status=po["status"],
                order_date=po["order_date"],
                delivery_date=datetime.now() + timedelta(days=1)
            )
    print('out_of_range_products: ', out_of_range_products, 'purchase_orders', purchase_orders)
    return render(request, "order/inventory.html", {
        "out_of_range_products": out_of_range_products,
        "purchase_orders": purchase_orders,
    })

def reports_view(request):
    # Determine the selected report type and filter type
    report_type = request.GET.get('report', 'purchase_orders')  # Default report is purchase orders
    filter_type = request.GET.get('filter', '1M')  # Default filter is 1M (1 Month)
    start_date = data_helper.get_date_for_filters(filter_type)
    context = {"selected_filter": filter_type, "report_type": report_type}
    # Fetch data based on report type
    if report_type == 'purchase_orders':
        purchase_orders = PurchaseOrder.objects.filter(order_date__gte=start_date)
        context["purchase_orders"] = purchase_orders
    elif report_type == 'supplier_ratings':
        reports_helper.calculate_supplier_units_and_ratings(Supplier, PurchaseOrder)
        supplier_ratings = Supplier.objects.all().order_by('-rating', '-total_units_supplied')
        # supplier_ratings = Supplier.objects.annotate(avg_rating=Avg('rating')).order_by('-avg_rating')
        context["supplier_ratings"] = supplier_ratings
    elif report_type == 'inventory_status':
        inventory = Inventory.objects.all()
        context["inventory"] = inventory

    return render(request, "reports/dashboard.html", context)


def grn_inward_view(request):
    today = date.today()

    # Fetch all purchase orders for today with status 'pending'
    purchase_orders = PurchaseOrder.objects.filter(
        status='pending', delivery_date=today
    ).select_related('product')

    context = {
        'purchase_orders': purchase_orders,
        'today': today,
    }
    return render(request, 'product/grn_inward.html', context)

def trigger_grn_inward_view(request):
    url = "https://s01swrn1lk.execute-api.ap-south-1.amazonaws.com/Staging/process-purchaseorders"
    response = requests.post(url)
    print('response: ', response)
    if response.status_code == 200:
        return JsonResponse({
                'status': 'success',
                'message': 'Lambda function executed successfully.',
                'data': response.json(),
            })
    else:
        print("Failed:", response.status_code, response.text)
    return JsonResponse({
                'status': 'error',
                'message': response.text,
    })