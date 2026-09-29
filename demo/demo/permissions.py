class ClientScopedQuerysetMixin(object):
    """Limit client-owned records to the authenticated user's clients."""

    def filter_queryset(self, queryset):
        queryset = super(ClientScopedQuerysetMixin, self).filter_queryset(queryset)
        user = self.request.user
        if user.is_staff:
            return queryset

        model = getattr(queryset, 'model', None)
        if model is None:
            raise TypeError(
                'Client-scoped views must return a Django queryset')
        field_names = {field.name for field in model._meta.get_fields()}
        if 'client' in field_names:
            return queryset.filter(client__user=user)
        if model.__name__ == 'Client' and 'user' in field_names:
            return queryset.filter(user=user)
        if 'cow' in field_names:
            return queryset.filter(cow__client__user=user)
        raise TypeError(
            'No client ownership relation found for {}'.format(model.__name__))
