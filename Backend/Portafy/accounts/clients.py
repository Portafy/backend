from allauth.socialaccount.providers.oauth2.client import (
    OAuth2Client as OriginalOAuth2Client,
)

class CustomOAuth2Client(OriginalOAuth2Client):
    def __init__(
        self,
        request,
        consumer_key,
        consumer_secret,
        access_token_method,
        access_token_url,
        callback_url,
        _scope=None,
        scope_delimiter=" ",
        headers=None,
        basic_auth=False,
    ):
        # match the signature expected by dj-rest-auth
        super().__init__(
            request=request,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_method=access_token_method,
            access_token_url=access_token_url,
            callback_url=callback_url,
            scope_delimiter=scope_delimiter,
            headers=headers,
            basic_auth=basic_auth,
        )
