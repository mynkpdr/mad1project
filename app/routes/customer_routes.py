from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.decorators import customer_required
import requests
from app.models import Service, db, Professional, Review, Category, Customer
from app.forms.customer_forms import EditCustomerAddressForm, EditCustomerPersonalForm, EditCustomerSecurityForm
from werkzeug.exceptions import NotFound
from app.forms.service_request_form import ServiceRequestForm
from app.forms.review_form import ReviewForm
from app.config import BaseConfig
from app.decorators import jwt_required
api_url = BaseConfig.API_URL

customer_routes = Blueprint('customer', __name__)

@customer_routes.route('/dashboard')
@customer_required
@jwt_required
def dashboard(c_user):
    
    response1  = requests.get(f'{api_url}/api/customer/{c_user.customer_data.id}/summary', headers={"token":session['token']})
    if response1.status_code != 200:
        flash("An error occured while loading the data", 'danger')
        return render_template('customer/dashboard.html', data=[])

    response2  = requests.get(f'{api_url}/api/service_requests', headers={"token":session['token']})
    if response2.status_code != 200:
        flash("An error occured while loading the data", 'danger')
        return render_template('customer/dashboard.html', data=[])
    
    summary = response1.json()['data']
    service_requests = response2.json()['data']

    requested_service_requests_count = summary['customer']['requested_service_requests_count']
    assigned_service_requests_count = summary['customer']['assigned_service_requests_count']
    current_service_requests_count = summary['customer']['current_service_requests_count']
    rejected_service_requests_count = summary['customer']['rejected_service_requests_count']
    closed_service_requests_count = summary['customer']['closed_service_requests_count']
    spending_data = summary['customer']['spending_data']
    return render_template('customer/dashboard.html',
                           data=response1.json()['data']['customer'],
                           rejected_service_requests_count=rejected_service_requests_count,
                           closed_service_requests_count=closed_service_requests_count,
                           current_service_requests_count=current_service_requests_count,
                           assigned_service_requests_count=assigned_service_requests_count,
                           requested_service_requests_count=requested_service_requests_count,
                           spending_data=spending_data,
                           service_requests=service_requests
                           )

@customer_routes.route('/dashboard/profile', methods=["GET", "POST"])
@customer_required
@jwt_required
def profile(c_user):
    user = Customer.query.filter_by(id=c_user.customer_data.id).first().user
    id = user.customer_data.id
    formx = request.args.get('formx')
    form_personal = EditCustomerPersonalForm(obj=user)
    form_address = EditCustomerAddressForm(obj=user)
    form_security = EditCustomerSecurityForm(obj=user)
    
    edit = request.args.get('edit')
   
    if request.method == "POST":
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
                            return redirect(url_for('customer.profile', edit=True))
                response = requests.put(f'{api_url}/api/customer/{id}', json=data, headers={"token":session['token']})
                flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
                return redirect(request.referrer or url_for('customer.profile'))
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
                return redirect(url_for('customer.profile', edit=True))
    elif request.method == "GET":
        response  = requests.get(f'{api_url}/api/customer/{id}', headers={"token":session['token']})
        if response.status_code != 200:
            raise NotFound("Customer not found") 
        customer = response.json()['data']['customer']
        if edit:
            return render_template('customer/profile.html', customer=customer, edit=edit, form_personal=form_personal, form_address=form_address, form_security=form_security)
        return render_template('customer/profile.html', customer=customer)

@customer_routes.route('/services')
def services():
    if request.method == "GET":
        
        response  = requests.get(f'{api_url}/api/services', params=request.args.items())
        if response.status_code != 200:
            flash("An error occured while loading the data", 'danger')
            return render_template('customer/services.html', services=[])
        services = response.json()
        return render_template('customer/services.html', services=services)
    return render_template('customer/services.html')

@customer_routes.route('/service/<int:id>')
@customer_required
def service(id):
    service = Service.query.get(id)
    if not service:
        raise NotFound
    service_name = service.name

    if request.method == "GET":
        
        response  = requests.get(f'{api_url}/api/service/{id}', params=request.args.items())
        if response.status_code != 200:
            flash("An error occured while loading the data", 'danger')
            return render_template('customer/service.html', services=[])
        services = response.json()
        distance_km = 3214
        data = {
            'distance_km': distance_km,
        }
        response2 =  requests.post(f'{api_url}/api/service/{id}/nearby_professionals', json=data, headers={"token":session['token']})
        if response2.status_code != 200:
            return render_template('customer/service.html', services=services)
        
        distances = response2.json()['data']
        
        for prof_details in services['data']['professionals']:
            for prof_dist in distances:
                if prof_dist['id'] == prof_details['id']:
                    prof_details['distance'] = prof_dist['distance']
        return render_template('customer/service.html', services=services)
    return render_template('customer/service.html')

@customer_routes.route('/service/<int:service_id>/professional/<int:professional_id>')
@customer_required
def service_professional(service_id, professional_id):
    
    response  = requests.get(f'{api_url}/api/professional/{professional_id}/profile', headers={"token":session['token']})
    if response.status_code != 200:
        raise NotFound("Professional not found") 
    professional = response.json()['data']['professional']
    recent_reviews = professional['recent_reviews']
    total_reviews = professional['total_reviews']
    professional_service = professional['professional_service']
    return render_template('customer/professional.html', professional=professional, total_reviews=total_reviews, professional_service=professional_service, recent_reviews=recent_reviews)

@customer_routes.route('/nearby')
@customer_required
def nearby():
    return render_template('customer/nearby_professional.html', services=Service.query.all())
    
@customer_routes.route('service/<int:service_id>/professional/<int:professional_id>/service_request', methods=["GET", "POST"])
@customer_required
@jwt_required
def service_request(c_user, service_id, professional_id):
    
    form = ServiceRequestForm()
    data =  db.session.query(Professional, Service).join(Professional, Professional.service_id == Service.id).filter(Service.id==service_id).filter(Professional.id==professional_id).first()
    if not data:
        raise NotFound
    professional, service = data
    category = Category.query.filter_by(id=service.category_id).first().name
    
    form.service_id.choices = [(service.id, service.name)]
    form.customer_id.choices = [(c_user.customer_data.id, c_user.name)]
    form.professional_id.choices = [(professional.id, f"{professional.user.name} (Rs. {professional.service_price} / hr)", {"data-price": int(professional.service_price)})]
    form.category_id.choices = [(service.category_id, category)]
    if request.method == "GET":
        response  = requests.get(f'{api_url}/api/service/{service_id}', params=request.args.items())
        if response.status_code != 200:
            flash("An error occured while loading the service data", 'danger')
            return render_template('customer/service_request.html', form=form, services=[])
        servicex = response.json()
        return render_template('customer/service_request.html', form=form, service=servicex['data'])
    else:
        if form.validate_on_submit():
            customer_id = c_user.customer_data.id
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
                return redirect(url_for('main.index'))
            flash('Service Request creation failed: ' + response.json().get('message', 'Unknown error'), 'danger')      
            return redirect(url_for('customer.service_request', service_id=service_id, professional_id=professional_id))
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
                return redirect(url_for('customer.service_requests', service_id=service_id, professional_id=professional_id))  
            flash("Check and enter the details again", "danger")
            return redirect(url_for('customer.service_request', service_id=service_id, professional_id=professional_id))

@customer_routes.route('/service_request/<int:id>', methods=["GET", "POST"])
@customer_required
def service_request_view(id):
    
    if request.method == "GET":
        response  = requests.get(f'{api_url}/api/service_request/{id}', headers={"token":session['token']})
        if response.status_code != 200:
            flash("An error occured while loading the data", 'danger')
            return render_template('customer/service_request_view.html', service_request=[])
        data = response.json()['data']
        return render_template('customer/service_request_view.html', service_request=data, reviewForm=ReviewForm())
    elif request.form.get('_method') == "PUT":
        response = requests.put(f'{api_url}/api/service_request/{id}', json=request.form.to_dict(), headers={"token":session['token']})
        flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
        return redirect(url_for('customer.service_request_view', id=id))

@customer_routes.route('/reviews', methods=["POST"])
@customer_required
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
            return redirect(url_for('admin.services'))
        flash(('Review creation failed'), 'danger')
        return redirect(request.referrer or '/')
        
@customer_routes.route('/review/<int:id>', methods=["POST"])
@customer_required
def review(id):
    
    if request.form.get('_method') == "DELETE":
        response = requests.delete(f'{api_url}/api/review/{id}', headers={"token":session['token']})
        if response.status_code == 200:
            flash("Review Deleted successfully", "success")
        else:
            flash("Couldn't delete review", "danger")
        return redirect(request.referrer or '/')


@customer_routes.route('/notifications/<int:notification_id>/read', methods=['POST'])
@customer_required
def mark_notification_as_read(notification_id):
    
    response = requests.post(f'{api_url}/api/notification/{notification_id}/read', headers={"token":session['token']})
    if response.status_code == 200:
        return '', 204  # No content response
    else:
        flash("An error occured", 'danger')
        return redirect(url_for('main.index'))

@customer_routes.route('/notifications')
@customer_required
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
