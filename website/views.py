from flask import Blueprint, render_template, flash, session, request, redirect, url_for, jsonify
from .utils.cloudinary import CloudinaryFunc
from .utils.mongo import MongoFunc
from .utils.recaptcha import RecaptchaFunc
import json
import os

views = Blueprint('views', __name__)
auth = Blueprint('auth', __name__)

recaptcha_site_key = os.getenv('RECAPTCHA_SITE_KEY')

@views.route('/')
def home():
    return render_template('home.html', title="EcoPin")

@views.route('/about')
def about():
    return render_template('about.html', title="About | EcoPin")

@views.route('/sendreport', methods=['GET', 'POST'])
def sendreport():
    if request.method == 'POST':
        file = request.files['image']
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        description = request.form.get('description')
        description += f"\nCoordinates: {latitude}° N, {longitude}° E"

        recaptcha_response = request.form['g-recaptcha-response']

        if not RecaptchaFunc.validate_recaptcha(recaptcha_response):
            flash('reCAPTCHA validation failed. Please try again.', category='error')
            return redirect(url_for('views.sendreport'))
        else:
            data = CloudinaryFunc.upload_image(file)
            MongoFunc.insert_data('reports', {'email': session["email"], 'image_url': data["image_url"], 'asset_id': data["asset_id"], 'description': description})

            flash('Report sent successfully!', category='success')
            return redirect(url_for('views.sendreport'))
        
    if session.get('email', None) is None:
        flash('You must be logged in to view this page.', category='error')
        return redirect(url_for('auth.login'))

    return render_template('sendreport.html', title="Send Report | EcoPin", site_key=recaptcha_site_key)

@views.route('/reports')
def reports():
    if session.get('email', None) is None:
        flash('You must be logged in to view this page.', category='error')
        return redirect(url_for('auth.login'))
    else:
        user_data = MongoFunc.get_data('users', {'email': session["email"]})
        points = user_data['points']
        if user_data is not None:
            if user_data['type'] == 'admin':
                reports = MongoFunc.find_data('reports', {})
                return render_template('reports.html', title="Reports | EcoPin", reports=reports, points=points, user_type='admin')

        reports = MongoFunc.find_data('reports', {'email': session["email"]})
        return render_template('reports.html', title="Reports | EcoPin", reports=reports, points=points, user_type='user')

@views.route('/deletereport', methods=['POST'])
def deletereport():
    report_data = json.loads(request.data)
    asset_id = report_data['asset_id']

    report = MongoFunc.get_data('reports', {'asset_id': asset_id})
    if report:
        if report["email"] == session["email"]:
            MongoFunc.delete_data('reports', {'asset_id': asset_id})

    return jsonify({})

@views.route('/approvereport', methods=['POST'])
def approvereport():
    report_data = json.loads(request.data)
    asset_id = report_data['asset_id']

    report = MongoFunc.get_data('reports', {'asset_id': asset_id})
    if report:
        MongoFunc.add_points(report["email"], 10)
        MongoFunc.delete_data('reports', {'asset_id': asset_id})

    return jsonify({})