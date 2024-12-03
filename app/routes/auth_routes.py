from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User, Service
from app.forms.auth_form import LoginForm
from app.forms.auth_form import CustomerSignupForm, ProfessionalSignUpForm
from app.models import Category
import requests
from app.config import BaseConfig
api_url = BaseConfig.API_URL
auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            email=request.form['email']
            user = User.query.filter_by(email=email).first()
            response = requests.post(f'{api_url}/api/gettoken', json=request.form.to_dict())
            if response.status_code == 200:
                token = response.json()['token']
                session['token'] = token
                login_user(user)
                flash('Logged in as {}'.format(email), 'success')
                return redirect(url_for(f'{current_user.role.name.lower()}.dashboard'))
            elif response.status_code == 403:
                flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
                return render_template('auth/login.html', loginform=LoginForm()), 403
            else:
                flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
                return render_template('auth/login.html', loginform=LoginForm()), response.status_code
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
                return render_template('auth/login.html', loginform=LoginForm()), 400
    else:
        if current_user and current_user.is_authenticated:
            return redirect(url_for('main.index'))
        return render_template('auth/login.html', loginform=LoginForm()), 200

@auth_routes.route('/signup', methods=["GET", "POST"])
def signup():
    
    user_param=request.args.get("user")
    customerSignupForm = CustomerSignupForm()
    professionalSignupForm = ProfessionalSignUpForm()
    professionalSignupForm.service_name.choices = [(service.id, service.name) for service in Service.query.all()]
    professionalSignupForm.service_price.data = [(service.price) for service in Service.query.all()]
    professionalSignupForm.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if request.method == "POST":
        if user_param == "customer":
            if customerSignupForm.validate_on_submit():
                filename = None
                data = request.form.to_dict()
                data['pincode'] = int(data['pincode'])
                if professionalSignupForm.profile_image.data:
                    image = request.files['profile_image']
                    files = {'image': (image.filename, image.stream, image.content_type)}
                    imageresponse = requests.post(f'{api_url}/api/upload', files=files)
                    if imageresponse.status_code == 201:
                        filename = imageresponse.json().get('filename')
                        data['profile_image'] = filename
                    else:
                        flash(imageresponse.json().get('message'), 'danger')
                        return render_template('auth/signup.html', categories = Category.query.all(), services=Service.query.all(), customersignupform=customerSignupForm, professionalsignupform=professionalSignupForm), imageresponse.status_code

                response = requests.post(f'{api_url}/api/customers', json=data)
                if response.status_code == 201:
                    flash(response.json().get('message'), 'success')
                    return redirect(url_for('main.index'))
                else:
                    flash(response.json().get('message'), 'danger')
                    return render_template('auth/signup.html', categories = Category.query.all(), services=Service.query.all(), customersignupform=customerSignupForm, professionalsignupform=professionalSignupForm), response.status_code
            if customerSignupForm.errors:
                for field, errors in customerSignupForm.errors.items():
                    for error in errors:
                        flash(f"Error in {getattr(customerSignupForm, field).label.text}: {error}", 'danger')
                return render_template('auth/signup.html', categories = Category.query.all(), services=Service.query.all(), customersignupform=customerSignupForm, professionalsignupform=professionalSignupForm), 400
        elif user_param == "professional":
            if professionalSignupForm.validate_on_submit():
                data = request.form.to_dict()
                data['pincode'] = int(data['pincode'])
                data['service_id'] = int(data['service_id'])
                data['service_price'] = int(data['service_price'])
                filename = None
                if professionalSignupForm.documents.data:
                    document = request.files['documents']
                    files = {'document': (document.filename, document.stream, document.content_type)}
                    documentresponse = requests.post(f'{api_url}/api/upload', files=files)
                    if documentresponse.status_code == 201:
                        filename = documentresponse.json().get('filename')
                        data['documents'] = filename
                    else:
                        flash(documentresponse.json().get('message'), 'danger')
                        return render_template('auth/signup.html', categories = Category.query.all(), services=Service.query.all(), customersignupform=customerSignupForm, professionalsignupform=professionalSignupForm), documentresponse.status_code
                    
                profilefilename = None
                if professionalSignupForm.profile_image.data:
                    image = request.files['profile_image']
                    files = {'image': (image.filename, image.stream, image.content_type)}
                    imageresponse = requests.post(f'{api_url}/api/upload', files=files)
                    if imageresponse.status_code == 201:
                        profilefilename = imageresponse.json().get('filename')
                        data['profile_image'] = profilefilename
                    else:
                        flash(imageresponse.json().get('message'), 'danger')
                        return render_template('auth/signup.html', categories = Category.query.all(), services=Service.query.all(), customersignupform=customerSignupForm, professionalsignupform=professionalSignupForm), imageresponse.status_code
                response = requests.post(f'{api_url}/api/professionals', json=data)
                if response.status_code == 201:
                    flash(response.json().get('message'), 'success')
                    return redirect(url_for('main.index'))
                else:
                    flash(response.json().get('message'), 'danger')
                    return render_template('auth/signup.html', categories = Category.query.all(), services=Service.query.all(), customersignupform=customerSignupForm, professionalsignupform=professionalSignupForm), response.status_code
            if professionalSignupForm.errors:
                for field, errors in professionalSignupForm.errors.items():
                    for error in errors:
                        flash(f"Error in {getattr(professionalSignupForm, field).label.text}: {error}", 'danger')
                return render_template('auth/signup.html', categories = Category.query.all(), services=Service.query.all(), customersignupform=customerSignupForm, professionalsignupform=professionalSignupForm), 400
        else:
            flash('No registration for this user', 'warning')
            return redirect(url_for('auth.signup', user=user_param))
    else:
        if current_user and current_user.is_authenticated:
            flash("You are logged in!", 'danger')
            return redirect(url_for('main.index'))
        return render_template('auth/signup.html', categories = Category.query.all(), services=Service.query.all(), customersignupform=customerSignupForm, professionalsignupform=professionalSignupForm), 200

@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('token', None)
    session.pop('Authorization', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
