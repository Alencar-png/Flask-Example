from flask import Blueprint, send_from_directory, render_template_string
import os

docs_bp = Blueprint("docs", __name__)

@docs_bp.route("/openapi.yaml")
def openapi_yaml():
    docs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs')
    return send_from_directory(docs_path, "swagger.yaml", mimetype="text/yaml")

@docs_bp.route("/apidocs")
def apidocs():
    html_template = """
    <!DOCTYPE html>
    <html lang="pt-BR">
      <head>
        <meta charset="UTF-8">
        <title>Documentacao da API</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
      </head>
      <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-standalone-preset.js"></script>
        <script>
          const ui = SwaggerUIBundle({
            url: "/openapi.yaml",
            dom_id: '#swagger-ui',
            presets: [SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset],
            layout: "StandaloneLayout"
          });
        </script>
      </body>
    </html>
    """
    return render_template_string(html_template)
