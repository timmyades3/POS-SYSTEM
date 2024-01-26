from pickle import FALSE
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from flask import jsonify
from posApp.models import Category, Products, Sales, salesItems
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json, sys
from datetime import date, datetime
from django.contrib.auth.models import User
from django.contrib import auth


# def register(request):
#     if request.method == "POST":
#         if request.user.is_authenticated:
#              return redirect("home-page")
#         form = Createuser(request.POST)
#         if form.is_valid():
#             form.save()
#             # Automatically log in the user after registration
#             username = form.cleaned_data.get("username")
#             raw_password = form.cleaned_data.get("password1")
#             user = authenticate(username=username, password=raw_password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse('start_fido2'))

#     else:
#         form = Createuser()
#     return render(request, "register.html", {"form": form})
    

# def login_user_in(request, username):
#     user=User.objects.get(username=username)
#     user.backend='django.contrib.auth.backends.ModelBackend'
#     auth.login(request, user)
#     if "next" in request.POST:
#         return redirect(request.POST.get("next"))
#     else:
#         return redirect('home-page')
    
# # ... other views


# # Update the login_user view to redirect authenticated users to the home page
# def login_user(request):
#     if request.user.is_authenticated:
#         return redirect("home-page")

#     logout(request)
#     resp = {"status": "failed", "msg": ""}
#     username = ""
#     password = ""
#     if request.POST:
#         username = request.POST["username"]
#         password = request.POST["password"]

#         user = authenticate(username=username, password=password)
#         if user is not None:
#             from mfa.helpers import has_mfa
#             res =  has_mfa(username = username,request=request) # has_mfa returns false or HttpResponseRedirect
#             if res:
#                 return res
#             return login_user_in(request,username=user.username)
#         else:
#             resp["msg"] = "Incorrect username or password"
#     return HttpResponse(json.dumps(resp), content_type="application/json")


# # # Login
# # def login_user(request):
# #     logout(request)
# #     resp = {"status":'failed','msg':''}
# #     username = ''
# #     password = ''
# #     if request.POST:
# #         username = request.POST['username']
# #         password = request.POST['password']

# #         user = authenticate(username=username, password=password)
# #         if user is not None:
# #             if user.is_active:
# #                 login(request, user)
# #                 resp['status']='success'
# #             else:
# #                 resp['msg'] = "Incorrect username or password"
# #         else:
# #             resp['msg'] = "Incorrect username or password"
# #     return HttpResponse(json.dumps(resp),content_type='application/json')


# # Logout
# def logoutuser(request):
#     logout(request)
#     return redirect("/")
# Create your views here.
@login_required
def home(request):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    categories = len(Category.objects.all())
    products = len(Products.objects.all())
    transaction = len(Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ))
    today_sales = Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ).all()
    total_sales = sum(today_sales.values_list('grand_total',flat=True))
    context = {
        'page_title':'Home',
        'categories' : categories,
        'products' : products,
        'transaction' : transaction,
        'total_sales' : total_sales,
    }
    return render(request, 'posApp/home.html',context)


def about(request):
    context = {
        'page_title':'About',
    }
    return render(request, 'posApp/about.html',context)

#Categories
@login_required
def category(request):
    category_list = Category.objects.all()
    # category_list = {}
    context = {
        'page_title':'Category List',
        'category':category_list,
    }
    return render(request, 'posApp/category.html',context)
@login_required
def manage_category(request):
    category = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            category = Category.objects.filter(id=id).first()
    
    context = {
        'category' : category
    }
    return render(request, 'posApp/manage_category.html',context)

@login_required
def save_category(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_category = Category.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
        else:
            save_category = Category(name=data['name'], description = data['description'],status = data['status'])
            save_category.save()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_category(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Category.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Products
@login_required
def products(request):
    product_list = Products.objects.all()
    context = {
        'page_title':'Product List',
        'products':product_list,
    }
    return render(request, 'posApp/products.html',context)
@login_required
def manage_products(request):
    product = {}
    categories = Category.objects.filter(status = 1).all()
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()
    
    context = {
        'product' : product,
        'categories' : categories
    }
    return render(request, 'posApp/manage_product.html',context)
def test(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'posApp/test.html',context)
@login_required
def save_product(request):
    data =  request.POST
    resp = {'status':'failed'}
    id= ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0 :
        resp['msg'] = "Product Code Already Exists in the database"
    else:
        category = Category.objects.filter(id = data['category_id']).first()
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                save_product = Products.objects.filter(id = data['id']).update(code=data['code'], category_id=category, name=data['name'], description = data['description'], price = float(data['price']),status = data['status'])
            else:
                save_product = Products(code=data['code'], category_id=category, name=data['name'], description = data['description'], price = float(data['price']),status = data['status'])
                save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Product Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_product(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Products.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Product Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")
@login_required
def pos(request):
    products = Products.objects.filter(status = 1)
    product_json = []
    for product in products:
        product_json.append({'id':product.id, 'name':product.name, 'price':float(product.price)})
    context = {
        'page_title' : "Point of Sale",
        'products' : products,
        'product_json' : json.dumps(product_json)
    }
    # return HttpResponse('')
    return render(request, 'posApp/pos.html',context)

@login_required
def checkout_modal(request):
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total' : grand_total,
    }
    return render(request, 'posApp/checkout.html',context)

@login_required
def save_pos(request):
    resp = {'status':'failed','msg':''}
    data = request.POST
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = Sales.objects.filter(code = str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)

    try:
        sales = Sales(code=code, sub_total = data['sub_total'], tax = data['tax'], tax_amount = data['tax_amount'], grand_total = data['grand_total'], tendered_amount = data['tendered_amount'], amount_change = data['amount_change']).save()
        sale_id = Sales.objects.last().pk
        i = 0
        for prod in data.getlist('product_id[]'):
            product_id = prod 
            sale = Sales.objects.filter(id=sale_id).first()
            product = Products.objects.filter(id=product_id).first()
            qty = data.getlist('qty[]')[i] 
            price = data.getlist('price[]')[i] 
            total = float(qty) * float(price)
            print({'sale_id' : sale, 'product_id' : product, 'qty' : qty, 'price' : price, 'total' : total})
            salesItems(sale_id = sale, product_id = product, qty = qty, price = price, total = total).save()
            i += int(1)
        resp['status'] = 'success'
        resp['sale_id'] = sale_id
        messages.success(request, "Sale Record has been saved.")
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp),content_type="application/json")

@login_required
def salesList(request):
    sales = Sales.objects.all()
    sale_data = []
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale,field.name)
        data['items'] = salesItems.objects.filter(sale_id = sale).all()
        data['item_count'] = len(data['items'])
        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']),'.2f')
        # print(data)
        sale_data.append(data)
    # print(sale_data)
    context = {
        'page_title':'Sales Transactions',
        'sale_data':sale_data,
    }
    # return HttpResponse('')
    return render(request, 'posApp/sales.html',context)

@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id = id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales,field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = salesItems.objects.filter(sale_id = sales).all()
    context = {
        "transaction" : transaction,
        "salesItems" : ItemList
    }

    return render(request, 'posApp/receipt.html',context)
    # return HttpResponse('')

@login_required
def delete_sale(request):
    resp = {'status':'failed', 'msg':''}
    id = request.POST.get('id')
    try:
        delete = Sales.objects.filter(id = id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Sale Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')

# # Create your views here.
# @login_required
# def home(request):
#     login_url = "/login/"
#     redirect_field_name = "login"
#     now = datetime.now()
#     current_year = now.strftime("%Y")
#     current_month = now.strftime("%m")
#     current_day = now.strftime("%d")
#     categories = len(Category.objects.filter(user=request.user))
#     products = len(Products.objects.filter(user=request.user))
#     transaction = len(
#         Sales.objects.filter(
#             user=request.user,
#             date_added__year=current_year,
#             date_added__month=current_month,
#             date_added__day=current_day,
#         )
#     )
#     today_sales = Sales.objects.filter(
#         user=request.user,
#         date_added__year=current_year,
#         date_added__month=current_month,
#         date_added__day=current_day,
#     ).all()
#     total_sales = sum(today_sales.values_list("grand_total", flat=True))
#     context = {
#         "page_title": "Home",
#         "categories": categories,
#         "products": products,
#         "transaction": transaction,
#         "total_sales": total_sales,
#     }
#     return render(request, "posApp/home.html", context)


# def about(request):
#     context = {
#         "page_title": "About",
#     }
#     return render(request, "posApp/about.html", context)


# # Categories
# @login_required
# def category(request):
#     category_list = Category.objects.filter(user=request.user)
#     # category_list = {}
#     context = {
#         "page_title": "Category List",
#         "category": category_list,
#     }
#     return render(request, "posApp/category.html", context)


# @login_required
# def manage_category(request):
#     category = {}
#     if request.method == "GET":
#         data = request.GET
#         id = ""
#         if "id" in data:
#             id = data["id"]
#         if id.isnumeric() and int(id) > 0:
#             category = Category.objects.filter(user=request.user, id=id).first()

#     context = {"category": category}
#     return render(request, "posApp/manage_category.html", context)


# @login_required
# def save_category(request):
#     data = request.POST
#     resp = {"status": "failed"}
#     try:
#         if (data["id"]).isnumeric() and int(data["id"]) > 0:
#             save_category = Category.objects.filter(id=data["id"]).update(
#                 name=data["name"],
#                 description=data["description"],
#                 status=data["status"],
#             )
#         else:
#             save_category = Category(
#                 user=request.user,
#                 name=data["name"],
#                 description=data["description"],
#                 status=data["status"],
#             )
#             save_category.save()
#         resp["status"] = "success"
#         messages.success(request, "Category Successfully saved.")
#     except:
#         resp["status"] = "failed"
#     return HttpResponse(json.dumps(resp), content_type="application/json")
# @login_required
# def delete_category(request):
#     data = request.POST
#     resp = {"status": ""}
#     try:
#         Category.objects.filter(user=request.user, id=data["id"]).delete()
#         resp["status"] = "success"
#         messages.success(request, "Category Successfully deleted.")
#     except:
#         resp["status"] = "failed"
#     return HttpResponse(json.dumps(resp), content_type="application/json")


# # Products
# @login_required
# def products(request):
#     product_list = Products.objects.filter(user=request.user)
#     context = {
#         "page_title": "Product List",
#         "products": product_list,
#     }
#     return render(request, "posApp/products.html", context)


# @login_required
# def manage_products(request):
#     product = {}
#     categories = Category.objects.filter(user=request.user, status=1).all()
#     if request.method == "GET":
#         data = request.GET
#         id = ""
#         if "id" in data:
#             id = data["id"]
#         if id.isnumeric() and int(id) > 0:
#             product = Products.objects.filter(user=request.user, id=id).first()

#     context = {"product": product, "categories": categories}
#     return render(request, "posApp/manage_product.html", context)


# def test(request):
#     categories = Category.objects.filter(user=request.user)
#     context = {"categories": categories}
#     return render(request, "posApp/test.html", context)


# @login_required
# def save_product(request):
#     data = request.POST
#     resp = {"status": "failed"}
#     id = ""
#     if "id" in data:
#         id = data["id"]
#     if id.isnumeric() and int(id) > 0:
#         check = (
#             Products.objects.exclude(id=id)
#             .filter(code=data["code"], user=request.user)
#             .all()
#         )
#     else:
#         check = Products.objects.filter(code=data["code"], user=request.user).all()
#     if len(check) > 0:
#         resp["msg"] = "Product Code Already Exists in the database"
#     else:
#         category = Category.objects.filter(
#             id=data["category_id"], user=request.user
#         ).first()
#         try:
#             if (data["id"]).isnumeric() and int(data["id"]) > 0:
#                 save_product = Products.objects.filter(
#                     id=data["id"], user=request.user
#                 ).update(
#                     code=data["code"],
#                     category_id=category,
#                     name=data["name"],
#                     description=data["description"],
#                     price=float(data["price"]),
#                     status=data["status"],
#                 )
#             else:
#                 save_product = Products(
#                     user=request.user,
#                     code=data["code"],
#                     category_id=category,
#                     name=data["name"],
#                     description=data["description"],
#                     price=float(data["price"]),
#                     status=data["status"],
#                 )
#                 save_product.save()
#             resp["status"] = "success"
#             messages.success(request, "Product Successfully saved.")
#         except:
#             resp["status"] = "failed"
#     return HttpResponse(json.dumps(resp), content_type="application/json")


# @login_required
# def delete_product(request):
#     data = request.POST
#     resp = {"status": ""}
#     try:
#         Products.objects.filter(id=data["id"], user=request.user).delete()
#         resp["status"] = "success"
#         messages.success(request, "Product Successfully deleted.")
#     except:
#         resp["status"] = "failed"
#     return HttpResponse(json.dumps(resp), content_type="application/json")


# @login_required
# def pos(request):
#     products = Products.objects.filter(status=1, user=request.user)
#     product_json = []
#     for product in products:
#         product_json.append(
#             {"id": product.id, "name": product.name, "price": float(product.price)}
#         )
#     context = {
#         "page_title": "Point of Sale",
#         "products": products,
#         "product_json": json.dumps(product_json),
#     }
#     # return HttpResponse('')
#     return render(request, "posApp/pos.html", context)


# @login_required
# def checkout_modal(request):
#     grand_total = 0
#     if "grand_total" in request.GET:
#         grand_total = request.GET["grand_total"]
#     context = {
#         "grand_total": grand_total,
#     }
#     return render(request, "posApp/checkout.html", context)


# @login_required
# def save_pos(request):
#     resp = {"status": "failed", "msg": ""}
#     data = request.POST
#     user = request.user  # Get the currently logged-in user

#     pref = datetime.now().year + datetime.now().year
#     i = 1
#     while True:
#         code = "{:0>5}".format(i)
#         i += int(1)
#         check = Sales.objects.filter(user=user, code=str(pref) + str(code)).exists()
#         if not check:
#             break
#     code = str(pref) + str(code)

#     try:
#         sale = Sales(
#             code=code,
#             sub_total=data["sub_total"],
#             tax=data["tax"],
#             tax_amount=data["tax_amount"],
#             grand_total=data["grand_total"],
#             tendered_amount=data["tendered_amount"],
#             amount_change=data["amount_change"],
#             user=user,
#         )
#         sale.save()

#         sale_id = sale.pk

#         i = 0
#         for prod in data.getlist("product_id[]"):
#             product_id = prod
#             product = Products.objects.get(id=product_id)
#             qty = data.getlist("qty[]")[i]
#             price = data.getlist("price[]")[i]
#             total = float(qty) * float(price)

#             sales_item = salesItems(
#                 sale_id=sale,
#                 product_id=product,
#                 qty=qty,
#                 price=price,
#                 total=total,
#                 user=user,
#             )
#             sales_item.save()
#             i += int(1)

#         resp["status"] = "success"
#         resp["sale_id"] = sale_id
#         messages.success(request, "Sale Record has been saved.")
#     except Exception as e:
#         # Log the exception or handle it appropriately
#         resp["msg"] = "An error occurred while saving the POS record."
#         print("Unexpected error:", e)

#     return HttpResponse(json.dumps(resp), content_type="application/json")


# @login_required
# def salesList(request):
#     sales = Sales.objects.filter(user=request.user)
#     sale_data = []

#     for sale in sales:
#         data = {}
#         for field in sale._meta.get_fields(include_parents=False):
#             if field.related_model is None:
#                 data[field.name] = getattr(sale, field.name)

#         data["items"] = salesItems.objects.filter(sale_id=sale, user=request.user).all()
#         data["item_count"] = len(data["items"])

#         if "tax_amount" in data:
#             data["tax_amount"] = format(float(data["tax_amount"]), ".2f")

#         sale_data.append(data)

#     context = {
#         "page_title": "Sales Transactions",
#         "sale_data": sale_data,
#     }

#     return render(request, "posApp/sales.html", context)


# @login_required
# def receipt(request):
#     id = request.GET.get("id")
#     sales = Sales.objects.filter(user=request.user, id=id).first()
#     transaction = {}
#     for field in Sales._meta.get_fields():
#         if field.related_model is None:
#             transaction[field.name] = getattr(sales, field.name)
#     if "tax_amount" in transaction:
#         transaction["tax_amount"] = format(float(transaction["tax_amount"]))
#     ItemList = salesItems.objects.filter(user=request.user, sale_id=sales).all()
#     context = {"transaction": transaction, "salesItems": ItemList}

#     return render(request, "posApp/receipt.html", context)
#     # return HttpResponse('')


# @login_required
# def delete_sale(request):
#     resp = {"status": "failed", "msg": ""}
#     id = request.POST.get("id")
#     try:
#         delete = Sales.objects.filter(user=request.user, id=id).delete()
#         resp["status"] = "success"
#         messages.success(request, "Sale Record has been deleted.")
#     except:
#         resp["msg"] = "An error occured"
#         print("Unexpected error:", sys.exc_info()[0])
#     return HttpResponse(json.dumps(resp), content_type="application/json")
