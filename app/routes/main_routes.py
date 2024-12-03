from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
from app.forms.contact_form import ContactForm
import requests
from app.config import BaseConfig
from app.decorators import jwt_required
api_url = BaseConfig.API_URL
main_routes = Blueprint('main', __name__)

@main_routes.route("/")
@jwt_required
def index(c_user):
    if c_user:
        if c_user.role.name == "ADMIN":
            return redirect(url_for('admin.dashboard'))
        if c_user.role.name == "PROFESSIONAL":
            return redirect(url_for('professional.dashboard'))
        return render_template('main/index.html') 
    return render_template('main/index.html')

@main_routes.route('/about')
def about():
    return render_template('main/about.html') 

@main_routes.route('/contact', methods = ["GET", "POST"])
def contact():
    form = ContactForm()
    
    if request.method == "POST" and form.validate_on_submit():
        contact_data = {
            'name': form.name.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'message': form.message.data,
        }

        response = requests.post(f'{api_url}/api/contacts', json=contact_data)

        if response.status_code == 201:
            flash('Message sent successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash(response.json().get('message'), 'success' if response.json().get('success') else 'danger')
    return render_template('main/contact.html', form=form)

@main_routes.route('/terms')
def terms():
    return render_template('main/terms.html') 


@main_routes.route('/view-document/<filename>')
def view_document(filename):
    # Check if the file is a PDF or an image based on its extension
    if filename.lower().endswith('.pdf'):
        return render_template('main/document_viewer.html', filename=filename)
    else:
        return send_from_directory('static/uploads/professional_documents', filename)
