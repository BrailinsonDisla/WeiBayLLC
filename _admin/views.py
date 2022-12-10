# Imports the tools required from flask for the website application.
from flask import Blueprint, render_template

# Imports the Accounts Management module.


# Initializes the blueprint for the _admin, the administrators.
_admin = Blueprint('_admin', __name__, template_folder='_templates', static_folder='_static')

# Defines the _admin blueprint's root.
@_admin.route('/admin')
def dashboard():
    return render_template('dashboard.html')

## DEFINE OTHER ROUTES