# Imports the tools required from flask_login for Permission Management.
from flask_principal import Identity, identity_changed, AnonymousIdentity

# Imports necessary modules to create the registered user blueprint.
from flask import Blueprint, Flask, flash, render_template, redirect, url_for, request, session

# Imports the tools required from flask_login for Login Management.
from flask_login import current_user, logout_user, login_required

# Imports the flask website application.
from WeiBayLLC import WeiBayLLC_App

# Initializes the blueprint for the _registered, the registered users.
_registered = Blueprint('_registered', __name__, template_folder='_templates', static_folder='_static')

# Secure File upload
from werkzeug.utils import secure_filename

from DBConnection import * 
import os
from PIL import Image

from Systems.productManagement import submit_listing,  img_grab

# Defines the _registered blueprint's root.
@_registered.route('/profile')
@login_required
def profile():
    return render_template('profile.html')  # fix

@_registered.route('/profile/<username>', methods=['GET', 'POST'])
def load_profile(username : str): # Page for loading user profile.
    return render_template('success.html', username=username)

@_registered.route('/logout')
@login_required
def logout(): # Page to process logging out.
    # Logs the user out.
    logout_user()

    # Removes the principal's session keys.
    session.pop('identity.name', None)
    session.pop('identity.auth_type', None)

    # Signals the principal for the identity change.
    identity_changed.send(WeiBayLLC_App, identity=AnonymousIdentity())

    # Redirect to the login page.
    return redirect(url_for('_default.home'))

## DEFINE OTHER ROUTES

# @_registered.route('/profile/new-product')
@_registered.route('/profile/listing_form')
@login_required
def user_listing():
    return render_template('prelist.html')  # fix

@_registered.route('/profile/process_listing', methods=['POST'])
@login_required
def listing_form(): #  Page for Listing Items as a Registered User.
    if request.method == 'POST':
        seller = current_user.user_id
        product_name = request.form.get('item-name')
        product_condition = request.form.get('item-condition')
        product_price = request.form.get('item-price')
        product_desc = request.form.get('item-description')
        product_qty = request.form.get('item-qty')
        image = request.files.getlist('item-image')
        
        # if not product_images:
        #     return 'No pic uploaded', 400
        
        UPLOAD_FOLDER = 'static/img/items/'
        WeiBayLLC_App.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        
        ALLOWED_EXTENSTIONS = set(['png','jpg','jpeg','gif'])
        
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSTIONS
        
        #product image path
        img_path = []
        for file in image:
            if file and allowed_file(file.filename):
                # img = Image.open(file)
                # image = img.resize((300,300))
                filename = secure_filename(file.filename)
                location = os.path.join(WeiBayLLC_App.config['UPLOAD_FOLDER'],filename)
                img_path.append(filename)
                file.save(location)
            else:
                return "FAILED"
        
        #Add the image_path to database For PENDINGAPPROVALPRODUCTS
        list_path = '|'.join(img_path) 
        submit_listing(seller,product_name, product_desc, product_condition, product_qty, product_price, list_path)
        return redirect(url_for('_registered.profile'))
    else:
        
        return redirect(url_for('_registered.profile'))
    

@_registered.route('/pictures')
def display_img():
        #! number in img_grab needs to be automated
        return render_template("index.html", images = img_grab(43))


    


    
