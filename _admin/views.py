# Imports the tools required from flask for the website application.
from flask import Blueprint, render_template, redirect, url_for

# Imports the Accounts Management module.
from accountManagement import is_admin, login_required

# Initializes the blueprint for the _admin, the administrators.
_admin = Blueprint('_admin', __name__, template_folder='_templates', static_folder='_static')

# Defines the _admin blueprint's root.

@_admin.route('/admin')
@login_required
def dashboard():
    # Checks if the current user is an admin.
    if is_admin():
            return render_template('dashboard.html')
    else:
        return redirect(url_for('_default.homepage'))

## DEFINE OTHER ROUTES