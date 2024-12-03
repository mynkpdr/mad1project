from flask import Blueprint, render_template, session
import requests
from app.decorators import professional_required
from werkzeug.exceptions import NotFound
from app.models import User, db
from app.forms.professional_forms import EditProfessionalPersonalForm, EditProfessionalAddressForm, EditProfessionalSecurityForm, EditProfessionalServiceForm
from flask import request, flash, redirect, url_for
from app.decorators import jwt_required
from app.config import BaseConfig
api_url = BaseConfig.API_URL

professional_routes = Blueprint('professional', __name__)


@professional_routes.route('/dashboard')
@jwt_required
@professional_required
def dashboard(c_user):
    
    response1  = requests.get(f'{api_url}/api/professional/{c_user.professional_data.id}/summary', headers={"token":session['token']})
    if response1.status_code != 200:
        flash("An error occured while loading the data", 'danger')
        return render_template('professional/dashboard.html', data=[])
    
    response2  = requests.get(f'{api_url}/api/service_requests', params=request.args.to_dict(), headers={"token":session['token']})
    if response2.status_code != 200:
        flash("An error occured while loading the data", 'danger')
        return render_template('professional/dashboard.html', data=[])
    
    summary = response1.json()['data']
    service_requests = response2.json()

    requested_service_requests_count = summary['professional']['requested_service_requests_count']
    assigned_service_requests_count = summary['professional']['assigned_service_requests_count']
    closed_service_requests_count = summary['professional']['closed_service_requests_count']
    rejected_service_requests_count = summary['professional']['rejected_service_requests_count']
    current_service_requests_count = summary['professional']['current_service_requests_count']

    revenue_data = summary['professional']['revenue_data']
    review_counts = summary['professional']['review_counts']
    average_review = summary['professional']['rating']
    total_reviews = summary['professional']['total_reviews']
    total_earnings = summary['professional']['total_earnings']
    current_service_requests_count = summary['professional']['current_service_requests_count']

    return render_template('professional/dashboard.html',
                           requested_service_requests_count = requested_service_requests_count,
                           assigned_service_requests_count = assigned_service_requests_count,
                           closed_service_requests_count = closed_service_requests_count,
                           rejected_service_requests_count = rejected_service_requests_count,
                           current_service_requests_count = current_service_requests_count,
                           review_counts = review_counts,
                           average_review = average_review,
                           revenue_data=revenue_data,
                           total_earnings = total_earnings,
                           service_requests = service_requests,
                           total_reviews = total_reviews
                           )

@professional_routes.route('/profile', methods=["GET", "POST"])
@professional_required
@jwt_required
def profile(c_user):
    user = User.query.filter_by(id=c_user.id).first()
    formx = request.args.get('formx')
    form_personal = EditProfessionalPersonalForm(obj=user)
    form_service = EditProfessionalServiceForm(obj=user)
    form_address = EditProfessionalAddressForm(obj=user)
    form_security = EditProfessionalSecurityForm(obj=user)
    edit = request.args.get('edit')
    if request.method == "POST":
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
                            return redirect(url_for('professional.profile', edit=True))
                response = requests.put(f'{api_url}/api/professional/{user.professional_data.id}', json=data, headers={"token":session['token']})
                flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
                return redirect(request.referrer or url_for('professional.profile'))
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
                return redirect(url_for('professional.profile', edit=True))
        else:
            raise Exception("An Error Occured")

    else:
        if edit:
            return render_template('professional/profile.html', edit=edit, form_personal=form_personal, form_address=form_address, form_service=form_service, form_security=form_security)
        response  = requests.get(f'{api_url}/api/professional/{c_user.professional_data.id}', headers={"token":session['token']})
        if response.status_code != 200:
            raise NotFound("Professional not found") 
        professional = response.json()['data']['professional']
        recent_service_requests = professional['recent_service_requests']
        recent_reviews = professional['recent_reviews']
        total_reviews = professional['total_reviews']
        professional_service = professional['professional_service']
        return render_template('professional/profile.html', professional=professional, recent_service_requests=recent_service_requests, total_reviews=total_reviews, professional_service=professional_service, recent_reviews=recent_reviews)

@professional_routes.route('/service_requests')
@professional_required
def service_requests():
    

    response  = requests.get(f'{api_url}/api/service_requests', params=request.args.to_dict(), headers={"token":session['token']})
    if response.status_code != 200:
        flash("An error occured while loading the data", 'danger')
        return render_template('professional/dashboard.html', data=[])
    
    service_requests = response.json()
    return render_template('professional/service_requests.html', service_requests=service_requests)

@professional_routes.route('/reviews')
@professional_required
def reviews():
    

    response  = requests.get(f'{api_url}/api/reviews', params=request.args.to_dict(), headers={"token":session['token']})
    if response.status_code != 200:
        flash("An error occured while loading the data", 'danger')
        return render_template('professional/reviews.html', data=[])
    
    reviews = response.json()
    return render_template('professional/reviews.html', reviews=reviews)


@professional_routes.route('/customer/<int:id>')
@professional_required
def customer(id):
    
    response  = requests.get(f'{api_url}/api/customer/{id}/profile', headers={"token":session['token']})
    if response.status_code != 200:
        raise NotFound("Customer not found") 
    customer = response.json()['data']['customer']
    recent_reviews = customer['recent_reviews']
    return render_template('professional/customer.html', customer=customer, recent_reviews=recent_reviews)

@professional_routes.route('/service_request/<int:id>', methods=["GET", "POST"])
@professional_required
def service_request(id):
    

    if request.method == "POST":
        if request.form.get('_method') == "PUT":
            response = requests.put(f'{api_url}/api/service_request/{id}', json=request.form.to_dict(), headers={"token":session['token']})
        else:
            response = requests.put(f'{api_url}/api/service_request/{id}', json=request.args.to_dict(), headers={"token":session['token']})
        flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
        return redirect(url_for('professional.service_request', id=id))
    else:
        response  = requests.get(f'{api_url}/api/service_request/{id}', headers={"token":session['token']})
        if response.status_code != 200:
            flash("An error occured while loading the data", 'danger')
            return render_template('professional/service_request.html', service_request=[])
        data = response.json()['data']
        return render_template('professional/service_request.html', service_request=data)

@professional_routes.route('/notifications/<int:notification_id>/read', methods=['POST'])
@professional_required
def mark_notification_as_read(notification_id):
    
    response = requests.post(f'{api_url}/api/notification/{notification_id}/read', headers={"token":session['token']})
    if response.status_code == 200:
        return '', 204  # No content response
    else:
        flash("An error occured", 'danger')
        return redirect(url_for('main.index'))

@professional_routes.route('/notifications')
@professional_required
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
