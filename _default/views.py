# Imports the tools required from flask for the website application.
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Imports the Accounts Management module.
from accountManagement import submitRUApplication, authenticate, anonymous

# Imports user-defined exceptions.
from UD_Exceptions import *

# Import ReportsManagement.
from reportsManagement import submitReport

# Initializes the blueprint for _default.
_default = Blueprint('_default', __name__, template_folder='_templates', static_folder='_static')



@_default.route('/')
def homepage(): # Homepage for the website application.
    return render_template('homepage.html')

@_default.route('/login')
def login(): # Page for login.
    # Checks if the current user is anonymous.
    if anonymous():
        return render_template('login.html')
    else:
        flash('LoggedIn')
        return redirect(url_for('_default.homepage'))

@_default.route('/process_login', methods=['GET', 'POST'])
def process_login(): # Page for login processing.
    if request.method == "POST":
        # Gets the email from the form.
        email = request.form.get('email')

        # Gets the username from the email.
        username = email.split('@')[0]

        # Gets the password from the form.
        pswd = request.form.get('password')

        try:
            # Submits authentication request.
            authenticated = authenticate(username, pswd)

            # Checks if the authentication was successful.
            if authenticated:
                # TODO: FIX
                return redirect(url_for('_registered.load_profile', username=request.form.get('email')))

        # DB-AUTHENTICATION-RELATED EXCEPTIONS.
        except IncorrectPassword:
            flash('IncorrectPassword')
        except PendingApproval:
            flash('PendingApproval')
        except BannedUser:
            flash('BannedUser')
        except UserDNE:
            flash('UserDNE')

        # Redirect (reload) the page.
        return redirect(url_for('_default.login'))
    else:
        if anonymous():
            return redirect(url_for('_default.login'))
        else:
            flash('LoggedIn')
            return redirect(url_for('_default.homepage'))

@_default.route('/apply')
def apply(): # Page for RU Application.
    # Checks if the current user is anonymous.
    if anonymous():
        return render_template('apply.html')
    else:
        flash('LoggedIn')
        return redirect(url_for('_default.homepage'))

@_default.route('/process_application', methods=['GET', 'POST'])
def process_application(): # Page for application processing.
    if request.method == "POST":
        # Gets the first name from the form.
        f_name = request.form.get('f_name')

        # Gets the last name from the form.
        l_name = request.form.get('l_name')

        # Gets the email from the form.
        email = request.form.get('email')

        # Gets the password from the form.
        pswd = request.form.get('password')

        # Gets the password confirmation from the form.
        confirm_pswd = request.form.get('confirm_password')

        try:
            # Submits the application.
            submitRUApplication(f_name, l_name, email, pswd, confirm_pswd)

            # Store the applicant's first name.
            flash(f_name)

            # Store the applicant's last name.
            flash(l_name)

            # Store the applicant's email.
            flash(email)

            # Redirect to the application submitted page.
            return redirect(url_for('_default.application_submitted'), code = 307)

        # FORM-RELATED EXCEPTIONS.
        except InvalidFirstName:
            flash('InvalidFirstName')
        except InvalidLastName:
            flash('InvalidLastName')
        except InvalidEmail:
            flash('InvalidEmail')
        except InvalidPassword:
            flash('InvalidPassword')
        except PasswordMismatch:
            flash('PasswordMismatch')

        # DB-SYSTEM-RELATED EXCEPTIONS.
        except PendingApplicant:
            flash('PendingApplicant')
        # TODO: HANDLE FOR DENIED USERS.
        except AlreadyRegistered:
            flash('AlreadyRegistered')
        except BannedApplicant:
            flash('BannedApplicant')

        # Redirect (reload) the page.
        return redirect(url_for('_default.apply'))
    else:
        # Checks if the current user is anonymous.
        if anonymous():
            return redirect(url_for('_default.apply'))
        else:
            return redirect(url_for('_default.homepage'))

@_default.route('/application_submitted', methods=['GET', 'POST'])
def application_submitted(): # Page for submitted application.
    if request.method == "POST":
        # Checks if the current user is anonymous.
        if anonymous():
            return render_template('application_submitted.html')
    else:
        return redirect(url_for('_default.homepage'))

## DEFINE OTHER ROUTES

@_default.route('/home')
def home():
    return render_template('home.html')

@_default.route('/product')
def product():
    return render_template('product.html')

@_default.route('/product/report')
def report():
    return render_template('report_item.html')


#! Need to Complete Report Form
@_default.route('/report_form')
def report_form():
    return render_template('report.html')

#! Check the submitReports to make sure it inclued prod_id, seller_id, and/or reporter_id
#! reportsManagement.py Commented out things in submitReport
@_default.route('/process_report', methods=['POST'])
def process_report():
    if request.method == 'POST':
        subject = request.form.get('ireport-reason')
        details = request.form.get('details')
        
        try:
            invalid_values = [None, '']

            # Checks if the reason field is invalid.
            if details in invalid_values:
                # Raise an InvalidReason exception.
                raise InvalidReason
            
            # TODO Make sure to include prod_id, seller_id, 
            #If the current user is anonymous then the reporter_id is None.
            if anonymous():
                submitReport(prod_id=None, seller_id=None, reporter_id=None, subject= subject, reason=details)
            else: 
                # TODO Make sure to include prod_id, seller_id, and reporter_id
                submitReport(prod_id=1, seller_id=None, reporter_id=None, subject= subject, reason=details)

            # TODO Pass Report to the Database
            return redirect(url_for('_default.homepage'))

        except InvalidReason:
            flash('InvalidReason')
        return redirect(url_for('_default.report_form'))
    else:
        if anonymous():
            return redirect(url_for('_default.homepage'))
        else:
            return redirect(url_for('_default.homepage'))
