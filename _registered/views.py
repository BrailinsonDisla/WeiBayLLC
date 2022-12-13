# Imports the tools required from flask_login for Permission Management.
from flask_principal import Identity, identity_changed, AnonymousIdentity

# Imports necessary modules to create the registered user blueprint.
from flask import Blueprint, render_template, redirect, url_for, request, session

# Imports the tools required from flask_login for Login Management.
from flask_login import current_user, logout_user, login_required

# Imports the flask website application.
from WeiBayLLC import WeiBayLLC_App

# Initializes the blueprint for the _registered, the registered users.
_registered = Blueprint('_registered', __name__, template_folder='_templates', static_folder='_static')

# Secure File upload
from werkzeug.utils import secure_filename

from DBConnection import * 

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
    return redirect(url_for('_default.homepage'))

## DEFINE OTHER ROUTES

## <<<<<<< talike3
## @_registered.route('/profile/new-product')
## def new_product():
##   return render_template('prelist.html')

@_registered.route('/profile/listing_form')
@login_required
def user_listing():
    return render_template('prelist.html')  # fix

@_registered.route('/listing_form', methods=['GET', 'POST'])
def listing_form(): #  Page for Listing Items as a Registered User.
    if request.method == 'POST':
        product_name = request.form.get('item-name')
        product_condition = request.form.get('item-condition')
        product_price = request.form.get('item-price')
        product_desc = request.form.get('item-description')
        product_images = request.files['item-image']
        
        if not product_images:
            return 'No pic uploaded', 400
        
        filename = secure_filename(product_images.filename)
        mimetype = product_images.mimetype
        
        dbCursor.execute("INSERT INTO PendingApprovalProducts VALUES()"(product_images.read(),filename, mimetype))
        
            
        # for product_images_data in product_images:
        #     product_images_data = product_images.read()
        #     binary_data = 
        print("item-name: %s\n"
            "item-condition %s\n"
            "item-price %s\n"
            "item-description: %s\n"
            "item-image: %s\n" % (product_name,product_condition,product_price, product_desc,product_images))
        return redirect(url_for('_registered.profile'))
 
