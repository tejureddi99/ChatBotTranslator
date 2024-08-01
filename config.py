import os

class DefaultConfig:
    """ Bot Configuration """
    PORT = int(os.environ.get('PORT', 3978))
    APP_ID = os.environ.get('MicrosoftAppId', '')
    APP_PASSWORD = os.environ.get('MicrosoftAppPassword', '')
    APP_TYPE = os.environ.get('MicrosoftAppType', 'MultiTenant')
    APP_TENANTID = os.environ.get('MicrosoftAppTenantId', '')

    # Translator Text API Configuration
    SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY", "ea800e77eed8493995a8b4997c21f678")
    SUBSCRIPTION_REGION = os.getenv("SUBSCRIPTION_REGION", "centralus")
    TRANSLATOR_TEXT_ENDPOINT = "https://api.cognitive.microsofttranslator.com/"
