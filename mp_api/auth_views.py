# mp_api/auth_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print("===== In CustomLogoutView! =====")
        print("===== request.data:", request.data, "=====")

        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            print("===== No refresh_token found in request.data =====")
            return Response({"detail": "Refresh token not provided."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            print(f"===== Blacklist Exception: {e} =====")
            pass  # We'll still say logout is successful

        return Response({"detail": "Logout successful."},
                        status=status.HTTP_200_OK)
