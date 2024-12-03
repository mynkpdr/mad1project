from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.models import *
from app.decorators import admin_required
from app.forms.user_forms import ProfileForm
from app.decorators import jwt_required
from app.forms.professional_forms import EditProfessionalAddressForm, EditProfessionalPersonalForm, EditProfessionalSecurityForm, EditProfessionalServiceForm
from app.forms.customer_forms import EditCustomerAddressForm, EditCustomerPersonalForm, EditCustomerSecurityForm
from app.forms.service_form import ServiceForm, CategoryForm
from app.forms.review_form import ReviewForm
from app.forms.service_request_form import ServiceRequestForm
from datetime import datetime
import requests
from werkzeug.exceptions import NotFound
import pytz
from datetime import datetime, timedelta
from app.config import BaseConfig
api_url = BaseConfig.API_URL
admin_routes = Blueprint('admin', __name__)

@admin_routes.route('/')
@admin_required
def index():
    return redirect(url_for('admin.dashboard'))

@admin_routes.route('/dashboard')
@admin_required
def dashboard():
    
    response  = requests.get(f'{api_url}/api/users', params=request.args.items(), headers={"token":session['token']})
    if response.status_code != 200:
        flash("An error occured while loading the data", 'danger')
        users = []
    else:
        users = response.json()
    
    details = db.session.query(Professional, ServiceRequest).join(
        ServiceRequest, Professional.id == ServiceRequest.professional_id).filter(
        (ServiceRequest.service_status == "CLOSED") |
        (ServiceRequest.service_status == "ASSIGNED") |
        (ServiceRequest.service_status == "REQUESTED")
        ).all()
    total_revenue = 0

    for detail in details:
        total_revenue += int(detail.ServiceRequest.total_cost)

    service_status_requested = ServiceRequest.query.filter_by(service_status=ServiceStatus.REQUESTED).all()
    service_status_assigned = ServiceRequest.query.filter_by(service_status=ServiceStatus.ASSIGNED).all()
    service_status_rejected = ServiceRequest.query.filter_by(service_status=ServiceStatus.REJECTED).all()
    service_status_closed = ServiceRequest.query.filter_by(service_status=ServiceStatus.CLOSED).order_by(ServiceRequest.date_updated).all()

    cutoff_date = datetime.now(pytz.timezone('Asia/Kolkata'))  - timedelta(days=30)
    revenue_last_month = ServiceRequest.query.filter(
        ServiceRequest.service_status == ServiceStatus.CLOSED,
        ServiceRequest.date_updated >= cutoff_date
    ).order_by(ServiceRequest.date_updated).all() 
    revenue_data = [{"x": revenue.date_updated.isoformat(), "y": revenue.total_cost} for revenue in revenue_last_month]
    unactiveprofessionals = Professional.query.filter_by(active=False).all()
    
    customers = Customer.query.all()
    professionals = Professional.query.all()
    service_requests = ServiceRequest.query.all()
    services = Service.query.all()
    return render_template('admin/dashboard.html',
                           revenue_data=revenue_data,
                           customers=customers,
                           professionals=professionals,
                           service_requests=service_requests,
                           services=services,
                           total_revenue = total_revenue,
                           service_status_requested=service_status_requested,
                           service_status_assigned=service_status_assigned,
                           service_status_rejected=service_status_rejected,
                           service_status_closed=service_status_closed,
                           users=users,
                           unactiveprofessionals=unactiveprofessionals)

@admin_routes.route('/customers')
@admin_required
def customers():
    
    response  = requests.get(f'{api_url}/api/customers', params=request.args.items(), headers={"token":session['token']})
    if response.status_code != 200:
        flash("An error occured while loading the data", 'danger')
        return render_template('admin/customers.html', customers=[])
    customers = response.json()
    return render_template('admin/customers.html', customers=customers)

@admin_routes.route('/customer/<int:id>', methods=["GET", "POST", "DELETE"])
@admin_required
def customer(id):
    user = Customer.query.filter_by(id=id).first().user
    formx = request.args.get('formx')
    form_personal = EditCustomerPersonalForm(obj=user)
    form_address = EditCustomerAddressForm(obj=user)
    form_security = EditCustomerSecurityForm(obj=user)
    
    edit = request.args.get('edit')
    block = request.args.get('block')
    if request.form.get('_method') == "DELETE":
        response = requests.delete(f'{api_url}/api/customer/{id}', headers={"token":session['token']})
        flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
        return redirect(url_for("admin.customers"))
    
    if request.method == "POST":
        if block == "True":
            response = requests.post(f'{api_url}/api/customer/{id}/block', json={"block":True}, headers={"token":session['token']})
            flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
            return redirect(request.referrer or url_for('admin.customer', id=id))
        elif block == "False":
            response = requests.post(f'{api_url}/api/customer/{id}/block', json={"block":False}, headers={"token":session['token']})
            flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
            return redirect(request.referrer or url_for('admin.customer', id=id))
        if request.form.get('_method') == "PUT":
            if formx == 'form_personal' and form_personal.validate() or formx == 'form_address' and form_address.validate() or formx == 'form_security' and form_security.validate():
                data = request.form.to_dict()
                if "pincode" in data:
                    data['pincode'] = int(data['pincode']) 
                if "lat" in data:
                    data['latitude'] = data['lat']
                if "lng" in data:
                    data['longitude'] = data['lng']
                # Prepare the image upload         
                if formx == 'form_personal' and form_personal.profile_image.data:
                    profile_image = request.files['profile_image']
                    filename = None
                    if profile_image:
                        files = {'image': (profile_image.filename, profile_image.stream, profile_image.content_type)}
                        imageresponse = requests.post(f'{api_url}/api/upload', files=files, headers={"token":session['token']})
                        if imageresponse.status_code == 201:
                            data['profile_image'] = imageresponse.json().get('filename')
                        else:
                            flash(imageresponse.json().get('message'), 'danger')
                            return redirect(url_for('admin.customer', id=id, edit=True))
                response = requests.put(f'{api_url}/api/customer/{id}', json=data, headers={"token":session['token']})
                flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
                return redirect(request.referrer or url_for('admin.customer', id=id))
            else:
                if formx == 'form_personal' and form_personal.errors:
                    for field, errors in form_personal.errors.items():
                        for error in errors:
                            flash(f"Error in {getattr(form_personal, field).label.text}: {error}", 'danger')
                elif formx == 'form_address' and form_address.errors:
                    for field, errors in form_address.errors.items():
                        for error in errors:
                            flash(f"Error in {getattr(form_address, field).label.text}: {error}", 'danger')
                elif formx == 'form_security' and form_security.errors:
                    for field, errors in form_security.errors.items():
                        for error in errors:
                            flash(f"Error in {getattr(form_security, field).label.text}: {error}", 'danger')
                return redirect(url_for('admin.customer', id=id, edit=True))
    elif request.method == "GET":
        response  = requests.get(f'{api_url}/api/customer/{id}', headers={"token":session['token']})
        if response.status_code != 200:
            raise NotFound("Customer not found") 
        customer = response.json()['data']['customer']
        if edit:
            return render_template('admin/customer.html', customer=customer, edit=edit, form_personal=form_personal, form_address=form_address, form_security=form_security)
        return render_template('admin/customer.html', customer=customer)

@admin_routes.route('/professionals')
@admin_required
def professionals():
    
    response  = requests.get(f'{api_url}/api/professionals', params=request.args.items(), headers={"token":session['token']})
    if response.status_code != 200:
        flash("An error occured while loading the data", 'danger')
        return render_template('admin/professionals.html', professionals=[])
    professionals = response.json()
    return render_template('admin/professionals.html', professionals=professionals)

@admin_routes.route('/professional/<int:id>', methods=["GET", "POST", "DELETE"])
@admin_required
def professional(id):
    user = Professional.query.filter_by(id=id).first().user
    formx = request.args.get('formx')
    form_personal = EditProfessionalPersonalForm(obj=user)
    form_service = EditProfessionalServiceForm(obj=user)
    form_address = EditProfessionalAddressForm(obj=user)
    form_security = EditProfessionalSecurityForm(obj=user)
    
    edit = request.args.get('edit')
    approve = request.args.get('approve')
    block = request.args.get('block')
    if request.method == "POST":
        if approve and approve.lower() == "true":
            response = requests.post(f'{api_url}/api/professional/{id}/active', json={"active":True}, headers={"token":session['token']})
            flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
            return redirect(request.referrer or url_for('admin.professional', id=id))
        elif approve and approve.lower() == "false":
            response = requests.post(f'{api_url}/api/professional/{id}/active', json={"active":False}, headers={"token":session['token']})
            flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
            return redirect(request.referrer or url_for('admin.professional', id=id))
        elif block and block.lower() == "true":
            response = requests.post(f'{api_url}/api/professional/{id}/block', json={"block":True}, headers={"token":session['token']})
            flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
            return redirect(request.referrer or url_for('admin.professional', id=id))
        elif block and block.lower() == "false":
            response = requests.post(f'{api_url}/api/professional/{id}/block', json={"block":False}, headers={"token":session['token']})
            flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
            return redirect(request.referrer or url_for('admin.professional', id=id))
        if request.form.get('_method') == "DELETE":
            response = requests.delete(f'{api_url}/api/professional/{id}', headers={"token":session['token']})
            flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
            return redirect(url_for("admin.professionals"))
        if request.form.get('_method') == "PUT":
            if formx == 'form_personal' and form_personal.validate() or formx == 'form_service' and form_service.validate() or formx == 'form_address' and form_address.validate() or formx == 'form_security' and form_security.validate():
                data = request.form.to_dict()
                if "pincode" in data:
                    data['pincode'] = int(data['pincode']) 
                if "service_price" in data:
                    data['service_price'] = int(data['service_price']) 
                if "experience" in data:
                    data['experience'] = int(data['experience']) 
                if "lat" in data:
                    data['latitude'] = data['lat']
                if "lng" in data:
                    data['longitude'] = data['lng']
                # Prepare the image upload         
                if formx == 'form_personal' and form_personal.profile_image.data:
                    profile_image = request.files['profile_image']
                    filename = None
                    if profile_image:
                        files = {'image': (profile_image.filename, profile_image.stream, profile_image.content_type)}
                        imageresponse = requests.post(f'{api_url}/api/upload', files=files, headers={"token":session['token']})
                        if imageresponse.status_code == 201:
                            data['profile_image'] = imageresponse.json().get('filename')
                        else:
                            flash(imageresponse.json().get('message'), 'danger')
                            return redirect(url_for('admin.professional', id=id, edit=True))
                response = requests.put(f'{api_url}/api/professional/{id}', json=data, headers={"token":session['token']})
                flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
                return redirect(request.referrer or url_for('admin.professional', id=id))
            else:
                if formx == 'form_personal' and form_personal.errors:
                    for field, errors in form_personal.errors.items():
                        for error in errors:
                            flash(f"Error in {getattr(form_personal, field).label.text}: {error}", 'danger')
                elif formx == 'form_service' and form_service.errors:
                    for field, errors in form_service.errors.items():
                        for error in errors:
                            flash(f"Error in {getattr(form_service, field).label.text}: {error}", 'danger')
                elif formx == 'form_address' and form_address.errors:
                    for field, errors in form_address.errors.items():
                        for error in errors:
                            flash(f"Error in {getattr(form_address, field).label.text}: {error}", 'danger')
                elif formx == 'form_security' and form_security.errors:
                    for field, errors in form_security.errors.items():
                        for error in errors:
                            flash(f"Error in {getattr(form_security, field).label.text}: {error}", 'danger')
                return redirect(url_for('admin.professional', id=id, edit=True))

    elif request.method == "GET":
        response  = requests.get(f'{api_url}/api/professional/{id}', headers={"token":session['token']})
        if response.status_code != 200:
            raise NotFound("Professional not found") 
        professional = response.json()['data']['professional']
        if edit:
            return render_template('admin/professional.html', professional=professional, edit=edit, form_personal=form_personal, form_address=form_address, form_service=form_service, form_security=form_security)
        recent_service_requests = professional['recent_service_requests']
        recent_reviews = professional['recent_reviews']
        total_reviews = professional['total_reviews']
        professional_service = professional['professional_service']
        return render_template('admin/professional.html', professional=professional, recent_service_requests=recent_service_requests, total_reviews=total_reviews, professional_service=professional_service, recent_reviews=recent_reviews)

@admin_routes.route('/services', methods=["GET", "POST"])
@admin_required
def services():
    
    form = ServiceForm()

    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if request.method == "GET":
        
        response  = requests.get(f'{api_url}/api/services', params=request.args.items())
        if response.status_code != 200:
            flash("An error occured while loading the data", 'danger')
            return render_template('admin/services.html', services=[], form=form)
        services = response.json()
        return render_template('admin/services.html', services=services, form=form)
    else: 
        if form.validate_on_submit():
            # Prepare the image upload
            filename = None
            if form.image.data:
                image = request.files['image']
                files = {'service': (image.filename, image.stream, image.content_type)}
                imageresponse = requests.post(f'{api_url}/api/upload', files=files, headers={"token":session['token']})
                if imageresponse.status_code == 201:
                    filename = imageresponse.json().get('filename')
                else:
                    flash(imageresponse.json().get('message'), 'danger')
                    return redirect(url_for('admin.services'))

            service_data = {
                'name': form.name.data,
                'price': int(form.price.data),
                'description': form.description.data,
                'category_id': int(form.category.data),
                'image': filename  # Only include if the image was successfully uploaded
            }

            response = requests.post(f'{api_url}/api/services', json=service_data, headers={"token":session['token']})

            if response.status_code == 201:
                flash('Service created successfully!', 'success')
                return redirect(url_for('admin.services'))
            else:
                flash('Service creation failed: ' + response.json().get('message', 'Unknown error'), 'danger')
                return redirect(url_for('admin.services'))
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
            return redirect(url_for('admin.services'))


@admin_routes.route('/service/<int:id>', methods=["GET", "PUT", "DELETE", "POST"])
@admin_required
def service(id):
    
    service = Service.query.filter_by(id=id).first()
    form = ServiceForm(obj=service)
    form.category.choices = [(category.id, category.name) for category in Category.query.all()] 
    if request.method == "GET":
        response  = requests.get(f'{api_url}/api/service/{id}', headers={"token":session['token']})
        if response.status_code != 200:
            if response.status_code == 404:
                raise NotFound
            flash("An error occured while loading the data", 'danger')
            return render_template('admin/service.html', service=[])

        data = response.json()['data']
        edit = request.args.get('edit')
        if edit:
            return render_template('admin/service.html', edit=edit, service=data, form=form)
        else:
            return render_template('admin/service.html', service=data)    
    elif request.method == "POST":
        if request.form.get('_method') == "DELETE":
            response = requests.delete(f'{api_url}/api/service/{id}', headers={"token":session['token']})
            flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
            return redirect(url_for("admin.services"))
        
        elif request.form.get('_method') == "PUT":
            if form.validate_on_submit():
                data = request.form.to_dict()
                data['category_id'] = int(data['category'])
                data['price'] = int(data['price'])
                if form.image.data:
                    image = request.files['image']

                    files = {'service': (image.filename, image.stream, image.content_type)}
                    imageresponse = requests.post(f'{api_url}/api/upload', files=files, headers={"token":session['token']})
                    if imageresponse.status_code == 201:
                        data['image'] = imageresponse.json().get('filename')
                    else:
                        flash(imageresponse.json().get('message'), 'danger')
                        return redirect(url_for('admin.service', id=id, edit=True))
                response = requests.put(f'{api_url}/api/service/{id}', json=data, headers={"token":session['token']})
                flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
                return redirect(url_for('admin.services'))
            else:
                if form.errors:
                    for field, errors in form.errors.items():
                        for error in errors:
                            flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
                    return redirect(url_for('admin.service', id=id, edit=True))
                flash("An error occured", "danger")
                return redirect(url_for('admin.services'))
        else:
            flash("An error occured", "danger")
            return redirect(url_for('admin.services'))
        
    else:
        flash("An error occured", "danger")
        return redirect(url_for('admin.services'))


@admin_routes.route('/categories', methods=["GET", "POST"])
@admin_required
def categories():
    
    form = CategoryForm()
    if request.method == "GET":
        
        response  = requests.get(f'{api_url}/api/categories', params=request.args.items())
        if response.status_code != 200:
            flash("An error occured while loading the data", 'danger')
            return render_template('admin/categories.html', categories=[], form=form)
        categories = response.json()
        return render_template('admin/categories.html', categories=categories, form=form)
    else: 
        if form.validate_on_submit():
            # Prepare the image upload
            category_data = {
                'name': form.name.data,
            }

            response = requests.post(f'{api_url}/api/categories', json=category_data, headers={"token":session['token']})

            if response.status_code == 201:
                flash('Category created successfully!', 'success')
                return redirect(url_for('admin.categories'))
            else:
                flash('Category creation failed: ' + response.json().get('message', 'Unknown error'), 'danger')
                return redirect(url_for('admin.categories'))
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
                return redirect(url_for('admin.categories'))
            flash("An error occured", "danger")
            return redirect(url_for('admin.categories'))

@admin_routes.route('/category/<int:id>', methods=["GET", "PUT", "DELETE", "POST"])
@admin_required
def category(id):
    
    category = Category.query.filter_by(id=id).first()
    form = CategoryForm(obj=category)
    if request.method == "GET":
        response  = requests.get(f'{api_url}/api/category/{id}', headers={"token":session['token']})
        if response.status_code != 200:
            if response.status_code == 404:
                raise NotFound
            flash("An error occured while loading the data", 'danger')
            return render_template('admin/category.html', category=[])

        data = response.json()['data']
        edit = request.args.get('edit')
        if edit:
            return render_template('admin/category.html', edit=edit, category=data, form=form)
        else:
            return render_template('admin/category.html', category=data)    

    elif request.method =="POST":
        if request.form.get('_method') == "DELETE":
            response = requests.delete(f'{api_url}/api/category/{id}', headers={"token":session['token']})
            flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
            return redirect(url_for("admin.categories"))
        
        elif request.form.get('_method') == "PUT" and form.validate_on_submit():
            response = requests.put(f'{api_url}/api/category/{id}', json=request.form.to_dict(), headers={"token":session['token']})
            flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
            return redirect(url_for('admin.categories'))
        else:
            flash("An error occured", "danger")
            return redirect(url_for('admin.categories'))
    else:
        flash("An error occured", "danger")
        return redirect(url_for('admin.categories'))

@admin_routes.route('/service_requests', methods=["GET", "POST"])
@admin_required
def service_requests():
    
    form = ServiceRequestForm()
    # Populate choices for select fields
    form.service_id.choices = [(service.id, service.name) for service in Service.query.all()]
    form.customer_id.choices = [(customer.id, customer.user.name) for customer in Customer.query.all()]
    form.professional_id.choices = [(professional.id, f"{professional.user.name} (Rs. {professional.service_price} / hr)", {"data-price": int(professional.service_price)}) for professional in Professional.query.all()]
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
    if request.method == "GET":
        
        response  = requests.get(f'{api_url}/api/service_requests', params=request.args.items(), headers={"token":session['token']})
        if response.status_code != 200:
            flash("An error occured while loading the data", 'danger')
            return render_template('admin/service_requests.html', service_requests=[], form=form)
        service_requests = response.json()
        return render_template('admin/service_requests.html', service_requests=service_requests, form=form)
    else:
        if form.validate_on_submit():
            service_id = int(request.form['service_id'])
            customer_id = int(request.form['customer_id'])
            professional_id = int(request.form['professional_id'])
            start_date = request.form['start_date']
            total_days = int(request.form['total_days'])
            hours_per_day = int(request.form['hours_per_day'])
            remarks = request.form['remarks']

            service_request_data = {
                'service_id':service_id,
                'customer_id':customer_id,
                'professional_id':professional_id,
                'start_date':str(start_date),
                'total_days':total_days,
                'hours_per_day':hours_per_day,
                'remarks':remarks
                
            }

            response = requests.post(f'{api_url}/api/service_requests', json=service_request_data, headers={"token":session['token']})

            if response.status_code == 201:
                flash('Service Request created successfully!', 'success')
                return redirect(url_for('admin.service_requests'))
            else:
                flash('Service Request creation failed: ' + response.json().get('message', 'Unknown error'), 'danger')
                return redirect(url_for('admin.service_requests'))
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
                return redirect(url_for('admin.service_requests'))
            flash("An error occured", "danger")
            return redirect(url_for('admin.service_requests'))
 
@admin_routes.route('/service_request/<int:id>', methods=["GET", "POST", "PUT", "DELETE"])
@admin_required
def service_request(id):
    
    service_request = ServiceRequest.query.get(id)
    reviewForm = ReviewForm()
    if request.method == "GET":
        response  = requests.get(f'{api_url}/api/service_request/{id}', headers={"token":session['token']})
        if response.status_code != 200:
            if response.status_code == 404:
                raise NotFound
            flash("An error occured while loading the data", 'danger')
            return render_template('admin/service_request.html', service_request=[], reviewForm=reviewForm)

        data = response.json()['data']
        edit = request.args.get('edit')
        if edit:
            return render_template('admin/service_request.html', form =ServiceRequestForm(obj=service_request), edit=edit, service_request=data)
        else:
            return render_template('admin/service_request.html', service_request=data, reviewForm=reviewForm)
        
    elif request.method == "POST":
        if request.form.get('_method') == "DELETE":
            response = requests.delete(f'{api_url}/api/service_request/{id}', headers={"token":session['token']})
            flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
            return redirect(url_for("admin.service_requests"))
        elif request.form.get('_method') == "PUT":
            data = request.form.to_dict()
            if "service_id" in data:
                data['service_id'] = int(data['service_id'])
            if "customer_id" in data:
                data['customer_id'] = int(data['customer_id'])
            if "professional_id" in data:
                data['professional_id'] = int(data['professional_id'])
            if "service_request_id" in data:
                data['service_request_id'] = int(data['service_request_id'])
            if "total_days" in data:
                data['total_days'] = int(data['total_days'])
            if "hours_per_day" in data:
                data['hours_per_day'] = int(data['hours_per_day'])
            response = requests.put(f'{api_url}/api/service_request/{id}', json=data, headers={"token":session['token']})
            flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
            return redirect(url_for('admin.service_request', id=id))
        else:
            return render_template('admin/service_request.html', service_request=service_request)
    
    else:
        return render_template('admin/service_request.html', service_request=service_request)

@admin_routes.route('/reviews', methods=["POST"])
def reviews():
    form = ReviewForm()
    if request.method == "POST" and form.validate_on_submit():
        
        review_data = {
            'professional_id': int(form.professional_id.data),
            'customer_id': int(form.customer_id.data),
            'service_request_id': int(form.service_request_id.data),
            'description': form.description.data,
            'value': int(form.value.data),
        }

        response = requests.post(f'{api_url}/api/reviews', json=review_data, headers={"token":session['token']})
        if response.status_code == 201:
            flash('Review created successfully!', 'success')
        else:
            flash(response.json().get('message'), 'danger')
        return redirect(request.referrer or '/')
    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
            return redirect(url_for('admin.reviews'))
        flash("An error occured", "danger")
        return redirect(url_for('admin.reviews'))

@admin_routes.route('/review/<int:id>', methods=["POST"])
def review(id):
    
    if request.method == "POST":
        if request.form.get('_method') == "DELETE":
            response = requests.delete(f'{api_url}/api/review/{id}', headers={"token":session['token']})
            if response.status_code == 200:
                flash("Review Deleted successfully", "success")
            else:
                flash("Couldn't delete review", "danger")
            return redirect(request.referrer or '/')

@admin_routes.route('/messages')
@admin_required
def messages():
    
    response  = requests.get(f'{api_url}/api/contacts', params=request.args.items(), headers={"token":session['token']})
    if response.status_code != 200:
        flash("An error occured while loading the data", 'danger')
        return render_template('admin/messages.html', messages=[])
    messages = response.json()
    return render_template('admin/messages.html', messages=messages)


@admin_routes.route('/message/<int:id>', methods=["GET", "POST", "DELETE"])
@admin_required
def message(id):
    
    if request.form.get('_method') == "DELETE":
        response = requests.delete(f'{api_url}/api/contact/{id}', headers={"token":session['token']})
        flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
        return redirect(url_for("admin.messages"))
    else:
        response  = requests.get(f'{api_url}/api/contact/{id}', headers={"token":session['token']})
        if response.status_code != 200:
            if response.status_code == 404:
                raise NotFound
            flash("An error occured while loading the data", 'danger')
            return render_template('admin/message.html', message=[])

        data = response.json()['data']
        return render_template('admin/message.html', message=data)
    
@admin_routes.route('/profile', methods=["GET", "POST"])
@admin_required
@jwt_required
def profile(c_user):
    user = User.query.filter_by(id=c_user.id).first()
    form = ProfileForm(obj=user)
    if request.method == "POST":
        if form.validate():
            name = request.form['name']
            username = request.form['username']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            pincode = request.form['pincode']
            about = request.form['about']
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            # Validate unique username/email
            if User.query.filter_by(username=username).first() and username != c_user.username:
                flash('Username already exists', 'error')
                return redirect(url_for('profile'))
            
            if User.query.filter_by(email=email).first() and email != c_user.email:
                flash('Email already exists', 'error')
                return redirect(url_for('profile'))

            profilefilename = None
            if form.profile_image.data:
                
                image = request.files['profile_image']
                files = {'image': (image.filename, image.stream, image.content_type)}
                imageresponse = requests.post(f'{api_url}/api/upload', files=files)
                if imageresponse.status_code == 201:
                    profilefilename = imageresponse.json().get('filename')
                    c_user.profile_image = profilefilename
                else:
                    flash(imageresponse.json().get('message'), 'danger')
                    return redirect(url_for('admin.profile', edit=True))

            c_user.name = name
            c_user.username = username
            c_user.email = email
            c_user.phone = phone
            c_user.address = address
            c_user.pincode = pincode
            c_user.about = about
            # Check if the current password is correct
            if user and user.check_password(user.email, current_password):
                # Update the password
                user.set_password(new_password)  
            elif new_password == '' and current_password == '':
                pass
            else:
                flash('Current password is incorrect.', 'danger')
                return redirect(url_for('admin.profile', edit=True))
            try:
                db.session.commit()
                flash('Profile updated successfully', 'success')
                return redirect(url_for('admin.profile'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while updating your profile', 'danger')
                return redirect(url_for('admin.profile', edit=True))    
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
                return redirect(url_for('admin.profile', edit=True))
            flash("An error occured", "danger")
            return redirect(url_for('admin.profile'))    
    edit = request.args.get('edit')
    if edit:
        return render_template('admin/profile.html', edit=edit, profileform=ProfileForm(obj=c_user))
    else:
        return render_template('admin/profile.html')


@admin_routes.route('/notifications/<int:notification_id>/read', methods=['POST'])
@admin_required
def mark_notification_as_read(notification_id):
    
    response = requests.post(f'{api_url}/api/notification/{notification_id}/read', headers={"token":session['token']})
    if response.status_code == 200:
        return '', 204  # No content response
    else:
        flash("An error occured", 'danger')
        return redirect(url_for('main.index'))

@admin_routes.route('/notifications')
@admin_required
def notification():
    link = request.args.get('notification_link', '/')
    notification_id = request.args.get('notification_id')
    if notification_id:
        
        response = requests.post(f'{api_url}/api/notification/{notification_id}/read', headers={"token":session['token']})
        if response.status_code == 200:
            return redirect(link)
        else:
            flash("An error occured", 'danger')
            return redirect(url_for('main.index'))
    else:
        flash("An error occured", 'danger')
        return redirect(url_for('main.index'))


@admin_routes.route('/search')
def advancesearch():
    
    q = request.args.get('q')
    t = request.args.get('t')
    if request.method == "GET":
        response  = requests.get(f'{api_url}/api/search', params=request.args.items(), headers={"token":session['token']})
        if response.status_code == 200:
            result = response.json()
            return render_template('admin/advancesearch.html', result=result, q=q, t=t)
        elif response.status_code == 400:
            return render_template('admin/advancesearch.html', result=[])

    return render_template('admin/advancesearch.html')