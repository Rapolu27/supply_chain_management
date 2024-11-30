from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Supplier, Product, PurchaseOrder, Inventory
from .forms import SupplierForm, ProductForm, PurchaseOrderForm
from scm_core.inventory_threshold import get_out_of_range_products, create_auto_purchase_orders
from scm_core import data_helper
from scm_core import reports_helper
from scm_core import validator
from scm_core.exception import SupplierException, ProductException, POException
import requests
from django.http import JsonResponse
from datetime import datetime,date,timedelta
import os

API_GATEWAY = os.getenv("SCM_API_GATEWAY","")+"/process-purchaseorders"

def home_view(request):
    if request.user.is_authenticated:
        return redirect('/postlogin') 
    return render(request, 'home/base.html')

def post_login_view(request):
    if not request.user.is_authenticated:
        return render(request, 'home/base.html')
    if is_scm_user(request.user):
        return redirect('user/dashboard')
    return redirect('/admin')

def is_scm_user(user):
    return user.groups.filter(name='SCM_USER').exists()

@login_required(login_url='user_login')
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier/list.html', {'suppliers': suppliers})

@login_required(login_url='user_login')
def supplier_create(request):
    try:
        if request.method == 'POST':
            form = SupplierForm(request.POST)
            if form.is_valid():
                supplier = form.save(commit=False)
                # validator.validate_active_supplier(supplier)
                validator.validate_supplier_name(supplier.name, Supplier)
                supplier.save()
                messages.success(request, 'Supplier added successfully!')
                return redirect('supplier_list')
        else:
            form = SupplierForm()
    except SupplierException as e:
        messages.error(request, str(e))
        form = SupplierForm()
    except Exception as e:
        print("supplier exception: ",e)
        messages.error(request, "Unable to create supplier")
        form = SupplierForm()
    return render(request, 'supplier/form.html', {'form': form})

@login_required(login_url='user_login')
def supplier_update(request, pk):
    try:
        supplier = get_object_or_404(Supplier, pk=pk)
        if request.method == 'POST':
            form = SupplierForm(request.POST, instance=supplier)
            if form.is_valid():
                supplier = form.save(commit= False)
                supplier.save()
                messages.success(request, 'Supplier updated successfully!')
                return redirect('supplier_list')
        else:
            form = SupplierForm(instance=supplier)
    except SupplierException as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, "Unable to update supplier details")
    return render(request, 'supplier/form.html', {'form': form})

@login_required(login_url='user_login')
def supplier_delete(request, pk):
    try:
        supplier = get_object_or_404(Supplier, pk=pk)
        if request.method == 'POST':
            supplier.delete()
            messages.success(request, 'Supplier deleted successfully!')
            return redirect('supplier_list')
    except SupplierException as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, "Unable to delete supplier")
    return render(request, 'supplier/delete.html', {'supplier': supplier})

@login_required(login_url='user_login')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/list.html', {'products': products})

@login_required(login_url='user_login')
def product_create(request):
    try:
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                product = form.save(commit=False)
                validator.validate_product(product, Product)
                product.save()
                messages.success(request, 'Product added successfully!')
                return redirect('product_list')
        else:
            form = ProductForm()
    except ProductException as e:
        print("product ex: ",e)
        messages.error(request, str(e))
    except Exception as e:
        print("product adding ex: ",e)
        messages.error(request, "Unable to create product")
    return render(request, 'product/form.html', {'form': form})

@login_required(login_url='user_login')
def product_update(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product updated successfully!')
                return redirect('product_list')
        else:
            form = ProductForm(instance=product)
    except ProductException as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, "Unable to update product")
    return render(request, 'product/form.html', {'form': form})

@login_required(login_url='user_login')
def product_delete(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            product.delete()
            messages.success(request, 'Product deleted successfully!')
            return redirect('product_list')
    except ProductException as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, "Unable to delete product")

    return render(request, 'product/delete.html', {'product': product})

@login_required(login_url='user_login')
def purchase_order_list(request):
    orders = PurchaseOrder.objects.all()
    return render(request, 'order/list.html', {'orders': orders})

def purchase_order_create(request):
    try:
        if request.method == 'POST':
            form = PurchaseOrderForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('purchase_order_list')
        else:
            form = PurchaseOrderForm()
    except POException as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, "unable to create purchase order")
    
    return render(request, 'order/form.html', {'form': form})
@login_required(login_url='user_login')
def purchase_order_update(request, pk):
    try:
        order = get_object_or_404(PurchaseOrder, pk=pk)
        if request.method == 'POST':
            form = PurchaseOrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect('purchase_order_list')
        else:
            form = PurchaseOrderForm(instance=order)
    except POException as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, "unable to update purchase order")
    return render(request, 'order/form.html', {'form': form})

@login_required(login_url='user_login')
def purchase_order_delete(request, pk):
    try:
        order = get_object_or_404(PurchaseOrder, pk=pk)
        if request.method == 'POST':
            order.delete()
            return redirect('purchase_order_list')
    except POException as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, "unable to delete purchase order")
    return render(request, 'order/delete.html', {'order': order})

@login_required(login_url='user_login')
def auto_generate_purchase_orders(request):
    out_of_range_products = None
    purchase_orders = None
    if request.method =='POST':
        inventory = Inventory.objects.all()
        out_of_range_products = get_out_of_range_products(inventory)
        data_helper.filter_already_scheduled_po(PurchaseOrder, out_of_range_products)
        suppliers = Supplier.objects.all()
        purchase_orders = create_auto_purchase_orders(out_of_range_products, suppliers)
        for po in purchase_orders:
            PurchaseOrder.objects.create(
                product_id=po["product_id"],
                supplier_id=po["supplier_id"],
                quantity=po["quantity"],
                status=po["status"],
                order_date=po["order_date"],
                delivery_date=datetime.now() + timedelta(days=1)
            )
    inventories = Inventory.objects.all()
    print('out_of_range_products: ', out_of_range_products, 'purchase_orders', purchase_orders)
    return render(request, "order/inventory.html", {
        "out_of_range_products": out_of_range_products,
        "purchase_orders": purchase_orders,
        "inventories":inventories
    })
@login_required(login_url='user_login')
def reports_view(request):
    # Determine the selected report type and filter type
    report_type = request.GET.get('report', 'purchase_orders')  # Default report is purchase orders
    filter_type = request.GET.get('filter', '1M')  # Default filter is 1M (1 Month)
    start_date = data_helper.get_date_for_filters(filter_type)
    context = {"selected_filter": filter_type, "report_type": report_type}
    if report_type == 'purchase_orders':
        purchase_orders = PurchaseOrder.objects.filter(order_date__gte=start_date)
        context["purchase_orders"] = purchase_orders
    elif report_type == 'supplier_ratings':
        reports_helper.calculate_supplier_units_and_ratings(Supplier, PurchaseOrder)
        supplier_ratings = Supplier.objects.all().order_by('-rating', '-total_units_supplied')
        context["supplier_ratings"] = supplier_ratings
    elif report_type == 'inventory_status':
        inventory = Inventory.objects.all()
        context["inventory"] = inventory

    return render(request, "reports/dashboard.html", context)

@login_required(login_url='user_login')
def grn_inward_view(request):
    today = date.today()
    print('today: ',today)
    purchase_orders = PurchaseOrder.objects.filter(
        status='Pending', delivery_date=today
    ).select_related('product')

    context = {
        'purchase_orders': purchase_orders,
        'today': today,
    }
    return render(request, 'product/grn_inward.html', context)
@login_required(login_url='user_login')
def trigger_grn_inward_view(request):
    response = requests.post(API_GATEWAY)
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