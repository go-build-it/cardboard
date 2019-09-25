import pulumi
from putils import opts, find_zone
from deplumi import Package, AwsgiHandler

config = pulumi.Config('cardboard')
basedomain = config.require("domain")

apiserv = Package(
    'Api',
    sourcedir='apiserv',
    resources={
    },
    **opts()
)

api_domain = f'api.{basedomain}'

AwsgiHandler(
    'ApiService',
    domain=api_domain,
    package=apiserv,
    func='__lambda__:main',
    timeout=6,  # seconds
    environment={
        'variables': {
            'github_client_id': config.get('github-client-id'),  # OAuth Client ID
            'github_client_secret': config.get('github-client-secret'),  # OAuth Client Secret
            'github_app_id': config.get('github-app-id'),  # Numeric App ID
            'github_private_key': config.get('github-private-key'),  # Signs JWTs for API authn
            'github_webhook_secret': config.get('github-webhook-secret'),  # github->app hook verify
        },
    },
    **opts()
)

pulumi.export('webhook_url',  f"https://{api_domain}/postreceive")
