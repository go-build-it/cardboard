import gqlmod
gqlmod.enable_gql_import()

import awsgi
import app


def main(event, context):
    return awsgi.response(app.app, event, context, base64_content_types={})
