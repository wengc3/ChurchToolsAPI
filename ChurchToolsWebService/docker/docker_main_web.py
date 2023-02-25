from os import environ

from ChurchToolsWebService import *

if __name__ == '__main__':
    domain = environ.get('domain')
    app.domain = domain

    app.run(debug=True, host='0.0.0.0')
