from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from common.permissions import SuperUserPermissions, AdministratorPermissions
from profiles.models import User, UserRole
from profiles.permissions import UserViewPermissions
from profiles.serializers import UserSerializer, UserRoleManagementSerializer, SimpleUserSerializer, \
    PasswordUpdateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    View set enabling list, retrieve, create, update and destroy methods for users
    """

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (UserViewPermissions,)

    @detail_route(methods=['put'])
    def passwords(self, request, *args, **kwargs):
        """
        Update user password
        """

        user = self.get_object()
        request_data = request.data
        request_data['username'] = user.username
        serializer = PasswordUpdateSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        # Serializer data valid. Proceed with update
        serializer.save()

        return Response(self.get_serializer(user).data)

    @list_route(methods=['get'], permission_classes=[AdministratorPermissions])
    def typeahead(self, request):
        """
        Return users matching a search query, to be used for typeahead
        """
        users = self.get_queryset()

        query = request.query_params.get('query', None)

        if query and len(query) > 2:
            users = users.filter(username__icontains=query)

        return Response(SimpleUserSerializer(users, many=True).data)


class UserRoleViewSet(viewsets.ModelViewSet):
    """
    View set enabling list, retrieve, create, update and destroy methods for user roles.
    Only accessible by super users.
    """

    queryset = UserRole.objects.all()
    serializer_class = UserRoleManagementSerializer
    permission_classes = (SuperUserPermissions,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('user', 'role',)
