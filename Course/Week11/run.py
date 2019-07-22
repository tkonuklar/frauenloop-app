from project import app, Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL= '/swagger'
API_DOC_URL='/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_DOC_URL,
    config={
     'app_name':'Frauenloop App'   
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT,url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug = True)


