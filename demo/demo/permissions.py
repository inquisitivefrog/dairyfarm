from django.conf import settings
from django.db.models import Count, IntegerField, OuterRef, Subquery

from rest_framework.permissions import BasePermission, SAFE_METHODS


FARM_NUMBER_MODELS = {
    'Cow',
    'Event',
    'Exercise',
    'HealthRecord',
    'Milk',
    'Pasture',
    'Seed',
}


class PublicDemoReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        if settings.PUBLIC_DEMO_READ_ONLY:
            return request.method in SAFE_METHODS
        return request.user.is_authenticated


class ClientScopedQuerysetMixin(object):
    """Limit client-owned records to the authenticated user's clients."""

    def filter_queryset(self, queryset):
        queryset = super(ClientScopedQuerysetMixin, self).filter_queryset(
            queryset)
        user = self.request.user
        model = getattr(queryset, 'model', None)
        if model is None:
            raise TypeError(
                'Client-scoped views must return a Django queryset')
        field_names = {field.name for field in model._meta.get_fields()}

        if settings.PUBLIC_DEMO_READ_ONLY:
            if model.__name__ == 'Client' and 'user' in field_names:
                return queryset.filter(
                    user__username=settings.PUBLIC_DEMO_OWNER_USERNAME,
                    name=settings.PUBLIC_DEMO_CLIENT_NAME)
            if 'client' in field_names:
                queryset = queryset.filter(
                    client__user__username=(
                        settings.PUBLIC_DEMO_OWNER_USERNAME),
                    client__name=settings.PUBLIC_DEMO_CLIENT_NAME)
            elif 'cow' in field_names:
                queryset = queryset.filter(
                    cow__client__user__username=(
                        settings.PUBLIC_DEMO_OWNER_USERNAME),
                    cow__client__name=settings.PUBLIC_DEMO_CLIENT_NAME)
            else:
                raise TypeError(
                    'No client ownership relation found for {}'.format(
                        model.__name__))
        elif not user.is_staff:
            if 'client' in field_names:
                queryset = queryset.filter(client__user=user)
            elif model.__name__ == 'Client' and 'user' in field_names:
                queryset = queryset.filter(user=user)
            elif 'cow' in field_names:
                queryset = queryset.filter(cow__client__user=user)
            else:
                raise TypeError(
                    'No client ownership relation found for {}'.format(
                        model.__name__))

        if model.__name__ in FARM_NUMBER_MODELS:
            sequence = model.objects.filter(
                client_id=OuterRef('client_id'),
                pk__lte=OuterRef('pk'),
            ).order_by().values('client_id').annotate(
                sequence=Count('pk'),
            ).values('sequence')[:1]
            queryset = queryset.annotate(
                farm_number=Subquery(
                    sequence,
                    output_field=IntegerField(),
                ),
            ).order_by('pk')
        return queryset
