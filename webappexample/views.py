# 📁 webappexample/views.py -----

import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
import requests


# 👆 We're continuing from the steps above. Append this to your webappexample/views.py file.

oauth = OAuth()

# oauth.register(
#     "auth0",
#     client_id=settings.AUTH0_CLIENT_ID,
#     client_secret=settings.AUTH0_CLIENT_SECRET,
#     client_kwargs={
#         "scope": "openid profile email",
#     },
#     server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
# )

oauth.register(
    "okta",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://dev-82880810.okta.com/.well-known/openid-configuration",
)

# 👆 We're continuing from the steps above. Append this to your webappexample/views.py file.

def login(request):
    return oauth.okta.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

# 👆 We're continuing from the steps above. Append this to your webappexample/views.py file.

def callback(request):
    token = oauth.okta.authorize_access_token(request)
    request.session["user"] = token
    #print(token)
    return redirect(request.build_absolute_uri(reverse("index")))

# 👆 We're continuing from the steps above. Append this to your webappexample/views.py file.

## Auth0 way
# def logout(request):
#     request.session.clear()

#     return redirect(
#         f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
#         + urlencode(
#             {
#                 "returnTo": request.build_absolute_uri(reverse("index")),
#                 "client_id": settings.AUTH0_CLIENT_ID,
#             },
#             quote_via=quote_plus,
#         ),
#     )

## Okta way
def logout(request):
    id_token = request.session["user"]["id_token"]
    request.session.clear()
    
    return redirect(f"https://dev-82880810.okta.com/oauth2/v1/logout?"
        + urlencode(
            {
                "post_logout_redirect_uri": "https://developerday.com",
                "id_token_hint": id_token,
            },
            quote_via=quote_plus,
        ))


# 👆 We're continuing from the steps above. Append this to your webappexample/views.py file.

def index(request):
    return render(
        request,
        "index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )