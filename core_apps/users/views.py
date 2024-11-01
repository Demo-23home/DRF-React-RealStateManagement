from rest_framework.response import Response
from rest_framework.request import Request
import logging
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from typing import Optional
from djoser.social.views import ProviderAuthView

logger = logging.getLogger(__name__)


def set_auth_cookies(response: Response, access_token: str, refresh_token: Optional[str]):
    # Refresh and Access Cookies are HTTP Only , they are accessible to client side JS
    access_token_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(
    )

    cookie_settings = {
        "path": settings.COOKIE_PATH,
        "secure": settings.COOKIE_SECURE,
        "http_only": settings.HTTP_ONLY,
        "same_site": settings.SAME_SITE,
        "max_age": access_token_lifetime
    }

    response.set_cookie("access", access_token, **cookie_settings)

    if refresh_token:
        refresh_token_lifetime = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(
        )
        refresh_token_settings = cookie_settings.copy()
        refresh_token_settings["max_age"] = refresh_token_lifetime

        response.set_cookie("refresh", refresh_token, **refresh_token_settings)

    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings["http_only"] = False
    response.set("logged_in", "true", **logged_in_cookie_settings)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs) -> Response:
        token_res = super.post(request, *args, **kwargs)

        if token_res.status_code == status.HTTP_200_OK:
            access_token = token_res.data.get("access")
            refresh_token = token_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(token_res, access_token, refresh_token)

                token_res.data.pop("access", None)
                token_res.data.pop("refresh", None)
                token_res.data["message"] = "Login Successful."
            else:
                token_res.data["message"] = "Login Failed."
                logger.error(
                    "Access or Refresh Tokens not found in login response data")

        return token_res


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            request.data["refresh"] = refresh_token

        refresh_res = super().post(request, *args, **kwargs)

        if refresh_res.status_code == status.HTTP_200_OK:
            access_token = refresh_res.data.get("access")
            refresh_token = refresh_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(refresh_res, access_token, refresh_token)

                refresh_res.data.pop("access", None)
                refresh_res.data.pop("refresh", None)

                refresh_res.data["message"] = "Access Tokens Refreshed Successfully."
            else:
                refresh_res.data["message"] = "Access or Refresh Tokens not found in login response data."
                logger.error(
                    "Access or Refresh Tokens not found in login response data .")

        return refresh_res


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs) -> Response:
        provider_res = super.post(request, *args, **kwargs)

        if provider_res.status_code == status.HTTP_201_CREATED:
            access_token = provider_res.data.get("access")
            refresh_token = provider_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(provider_res, access_token, refresh_token)

                provider_res.data.pop("access", None)
                provider_res.data.pop("refresh", None)
                provider_res.data["message"] = "You are logged in Successfully."
            else:
                provider_res.data["message"] = "Access or Refresh tokens not found in provider response."
                logger.error(
                    "Access or Refresh Tokens not found in provider response data")

        return provider_res


class LogoutAPIView(APIView):
    def post(request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("logged_in")
        return response
