# Imports the tools required from flask for the website application.
from flask import Flask

# Imports the SHA-256 hash function from hashlib.
from hashlib import sha256

# Creates the WeiBayLLC Flask Application.
WeiBayLLC_App = Flask(__name__)

# Defines a string digest for the application's secret key.
sec_key = sha256('!223$TMCBA'.encode('utf-8')).hexdigest()

# Configures the application's secret key.
WeiBayLLC_App.config['SECRET_KEY'] = sec_key

# Imports the blueprint object for _admin.
from _admin.views import _admin

# Registers the _admin blueprint.
WeiBayLLC_App.register_blueprint(_admin)

# Imports the blueprint object for _default.
from _default.views import _default

# Registers the _default blueprint.
WeiBayLLC_App.register_blueprint(_default)

# Imports the blueprint object for _registered.
from _registered.views import _registered

# Registers the _registered blueprint.
WeiBayLLC_App.register_blueprint(_registered)

# Runs the WeiBayLLC website application.
if __name__ == '__main__':
    WeiBayLLC_App.run()