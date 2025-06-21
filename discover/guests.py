from models.models import Guest, Owner


def get_owner(request) -> Owner:
    if 'owner' in request.session:
        owner_id = request.session.get('owner')
        try:
            return Owner.objects.get(id=owner_id)
        except Owner.DoesNotExist:
            raise ValueError("Owner ID in session does not exist.")
    if request.user.is_authenticated:
        if hasattr(request.user, 'owner'):
            return request.user.owner
        return Owner.objects.create(auth_user=request.user)
    guest_uuid = request.GET.get('guest_uuid', None) or request.COOKIES.get('guest_uuid', None)
    if guest_uuid:
        try:
            guest = Guest.objects.get(uuid=guest_uuid)
            return Owner.objects.get(guest=guest)
        except Guest.DoesNotExist:
            raise ValueError("Guest not found.")
        except Owner.DoesNotExist:
            raise ValueError("Owner not found for the given guest.")
    guest = Guest.objects.create()
    return Owner.objects.create(guest=guest)


def with_owner(function):
    def wrapper(request, *args, **kwargs):
        owner = get_owner(request)
        request.session['owner'] = owner.pk
        res = function(request, *args, **kwargs)
        if not owner.is_authenticated:
            res.set_cookie('guest_uuid', owner.guest.uuid, max_age=60*60*24*30)
        return res
    return wrapper

