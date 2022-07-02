import connexion
import os
from explorer import config
from connexion.resolver import RestyResolver


def daemon():
    options = {"swagger_ui": True}
    app = connexion.FlaskApp('Explorer-k8s-metrics-API', server='tornado', options=options)
    here = os.path.abspath(os.path.dirname(__file__))
    app.add_api('%s/config/swagger.yaml' % here, resolver=RestyResolver('explorer.controller'))
    app.run(port=config.PORT, debug=True)
