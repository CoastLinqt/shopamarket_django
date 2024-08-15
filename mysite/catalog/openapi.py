from drf_yasg import openapi
from rest_framework import status

name = openapi.Parameter(
                            name="filter[name]",
                            in_=openapi.IN_QUERY,
                            type=openapi.TYPE_STRING,
                            required=True,
                            description="Document"
                            )

minPrice = openapi.Parameter(
                            name="minPrice",
                            in_=openapi.IN_QUERY,
                            default=0,
                            type=openapi.TYPE_NUMBER,
                            required=True,
                            )
maxPrice = openapi.Parameter(
                            name="maxPrice",
                            in_=openapi.IN_QUERY,
                            default=0,
                            type=openapi.TYPE_NUMBER,
                            required=True,
                            )
freeDelivery = openapi.Parameter(
                            name="freeDelivery",
                            in_=openapi.IN_QUERY,
                            type=openapi.TYPE_BOOLEAN,
                            required=True,
                            )

available = openapi.Parameter(
                            name="available",
                            in_=openapi.IN_QUERY,
                            type=openapi.TYPE_BOOLEAN,
                            required=True,
                            )

currentPage = openapi.Parameter(
                            name="currentPage",
                            in_=openapi.IN_QUERY,
                            type=openapi.TYPE_INTEGER,
                            required=True,
                            )

category = openapi.Parameter(
                            name="available",
                            in_=openapi.IN_QUERY,
                            type=openapi.TYPE_INTEGER,
                            required=True,
                            )

sort = openapi.Parameter(
                            name="sort",
                            in_=openapi.IN_QUERY,
                            type=openapi.TYPE_STRING,
                            default='date',
                            enum=('rating', 'price', 'reviews', 'date'),
                            required=True,
                            )

sortType = openapi.Parameter(
                            name="sortType",
                            in_=openapi.IN_QUERY,
                            type=openapi.TYPE_STRING,
                            default='dec',
                            enum=('dec', 'inc',),

                            required=False,
                            )

limit = openapi.Parameter(
                            name="limit",
                            in_=openapi.IN_QUERY,
                            type=openapi.TYPE_NUMBER,
                            default=20,
                            required=True,
                            )

# available = openapi.Parameter(
#                             name="available",
#                             in_=openapi.IN_QUERY,
#                             type=openapi.TYPE_BOOLEAN,
#                             required=True,
#                             )