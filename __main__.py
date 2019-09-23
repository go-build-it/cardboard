import pulumi
from putils import opts
from deplumi import Package, AwsgiHandler
from pulumi_aws import route53

config = pulumi.Config('cardboard')

zone = route53.get_zone(name='dingbots.dev')

apiserv = Package(
    'Api',
    sourcedir='apiserv',
    resources={
    },
    **opts()
)

api_domain = f'api.{config.require("domain")}'

AwsgiHandler(
    'ApiService',
    domain=api_domain,
    zone=zone,
    package=apiserv,
    func='__lambda__:main',
    timeout=6,  # seconds
    environment={
        'variables': {
            'github_client_id': config.get('github-client-id'),  # OAuth Client ID
            'github_client_secret': config.get('github-client-secret'),  # OAuth Client Secret
            'github_app_id': config.get('github-app-id'),  # Numeric App ID
            'github_private_key': config.get('github-private-key'),  # Signs JWTs for API authn
            'github_hook_secret': config.get('github-hook-secret'),  # github->app hook verify
        },
    },
    **opts()
)

pulumi.export('webhook_url',  f"https://{api_domain}/postreceive")
