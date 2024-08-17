from drf_yasg import openapi
from rest_framework import status

avatar = openapi.Parameter(
    name="avatar",
    in_=openapi.IN_FORM,
    type=openapi.TYPE_FILE,
    required=True,
    description="Document",
)
#
# passwordCurrent = openapi.Parameter(
#                             name="passwordCurrent",
#                             in_=openapi.IN_BODY,
#                             type=openapi.TYPE_STRING,
#                             required=True,
#                             )
# password = openapi.Parameter(
#                             name="password",
#                             in_=openapi.IN_BODY,
#                             type=openapi.TYPE_STRING,
#                             required=True,
#                             )
# passwordReply = openapi.Parameter(
#                             name="passwordReply",
#                             in_=openapi.IN_BODY,
#                             type=openapi.TYPE_STRING,
#                             required=True,
#                             )
password_input = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "passwordCurrent": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="passwordCurrent",
        ),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description="password"),
        "passwordReply": openapi.Schema(
            type=openapi.TYPE_STRING, description="passwordReply"
        ),
    },
)

profile_schema_response = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "fullName": openapi.Schema(type=openapi.TYPE_STRING),
            "phone": openapi.Schema(type=openapi.TYPE_STRING),
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "avatar": openapi.Schema(type=openapi.TYPE_OBJECT),
        },
    ),
    status.HTTP_400_BAD_REQUEST: openapi.Schema(
        type=openapi.TYPE_STRING, description="the password does not match"
    ),
}

profile_schema = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "fullName": openapi.Schema(type=openapi.TYPE_STRING),
            "phone": openapi.Schema(type=openapi.TYPE_STRING),
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "avatar": openapi.Schema(type=openapi.TYPE_OBJECT),
        },
    ),
}
