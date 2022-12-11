# Imports the tools required from flask for the website application.
from flask import Blueprint, render_template, redirect, url_for

# Imports the Accounts Management module.
from accountManagement import admin_perm, login_required

# Initializes the blueprint for the _admin, the administrators.
_admin = Blueprint('_admin', __name__, template_folder='_templates', static_folder='_static')

# Defines the _admin blueprint's root.

@_admin.route('/admin')
@login_required
def dashboard():
    # Checks if the current user is an admin.
    if anonymousIdentity():
        return redirect(url_for('_default.homepage'))
    return render_template('dashboard.html')

## DEFINE OTHER ROUTES