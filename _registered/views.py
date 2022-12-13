# Imports the tools required from flask_login for Permission Management.
from flask_principal import Identity, identity_changed, AnonymousIdentity

# Imports necessary modules to create the registered user blueprint.
from flask import Blueprint, render_template, redirect, url_for, session

# Imports the tools required from flask_login for Login Management.
from flask_login import current_user, logout_user, login_required

# Imports the flask website application.
from WeiBayLLC import WeiBayLLC_App

# Initializes the blueprint for the _registered, the registered users.
_registered = Blueprint('_registered', __name__, template_folder='_templates', static_folder='_static')

# Defines the _registered blueprint's root.
@_registered.route('/profile')
@login_required
def profile():
    return render_template('profile.html')  # fix

@_registered.route('/profile', methods=['GET', 'POST'])
def load_profile(): # Page for loading user profile.
    return 'Welcome ';

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

9736873064