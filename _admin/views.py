# Imports the tools required from flask for the website application.
from flask import Blueprint, render_template

# Imports the tools required from flask_login for Login Management.
from flask_login import login_required

# Initializes the blueprint for the _admin, the administrators.
_admin = Blueprint('_admin', __name__, template_folder='_templates', static_folder='_static')

# Defines the _admin blueprint's root.
@_admin.route('/admin')
@login_required
def dashboard():
    print("\n\n\n\nIssue here1?\n\n\n\n")
    return render_template('dashboard.html')

## DEFINE OTHER ROUTES