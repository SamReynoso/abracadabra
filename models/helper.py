from models.models import (
        Images,
        Organization,
        Event,
        DivisionInfo,
        DivisionOrg,
        Images,
        Organization,
        DivisionOrg,
        Address,
        )


class Helper:
    class GetCreate:
        @staticmethod
        def division(data):
            obj, _ =  DivisionInfo.objects.get_or_create(
                    gender=data.get('gender', ''),
                    age=data.get('age', ''),
                    level=data.get('level', ''))
            return obj

    class Get:
        @staticmethod
        def images(user):
            return Images.objects.filter(user=user)

        @staticmethod
        def image(data, user):
            image_slug = data.get('image_slug', '')
            if not image_slug:
                raise ValueError("Image slug is required.")
            try:
                image = Images.from_slug(image_slug)
            except Images.DoesNotExist:
                raise ValueError("Image not found.")
            if image.user != user:
                raise ValueError("You do not have permission to access this image.")
            return image

        @staticmethod
        def organization(data, user):
            org_slug = data.get('organization_slug', '')
            if not org_slug:
                raise ValueError("Organization slug is required.")
            organization = Organization.from_slug(org_slug)
            if not organization:
                raise ValueError("Organization not found.")
            if organization.director != user:
                raise ValueError("You are not a member of this organization.")
            return organization

        @staticmethod
        def event(data, user):
            event_slug = data.get('event_slug', '')
            if not event_slug:
                raise ValueError("Event slug is required.")
            event = Event.from_slug(event_slug)
            if not event:
                raise ValueError("Event not found.")
            if not event.organization.director == user:
                raise ValueError("You are not a member of this event's organization.")
            return event

        @staticmethod
        def address(data, user) -> Address:
            address_id = data.get('address_id', '')
            if not address_id:
                raise ValueError("Address ID is required.")
            try:
                address = Address.objects.get(id=address_id, user=user)
            except Address.DoesNotExist:
                raise ValueError("Address not found or does not belong to this user.")
            return address


    class Create:
        @staticmethod
        def image(data, files, user):
            if 'image' not in files:
                raise ValueError("Image file is required.")
            return Images.objects.create(
                image=files['image'],
                caption=data.get('caption', ''),
                user=user,
            )

        @staticmethod
        def event(data, user):
            organization = Helper.Get.organization(data, user)
            return Event.objects.create(
                name=data.get('name', 'new event'),
                organization=organization,
                status=Event.Status.CREATED,
            )

        @staticmethod
        def organization_division(data, user):
            org_obj = Helper.Get.organization(data, user)
            info_obj, _ = DivisionInfo.objects.get_or_create(
                    level=data.get('level', ''),
                    age=data.get('age', ''),
                    gender=data.get('gender', ''),
                    )
            obj, _ = DivisionOrg.objects.get_or_create(
                organization=org_obj,
                info=info_obj,
            )
            return obj

        @staticmethod
        def address(data, user):
            return Address.objects.create(
                user=user,
                street=data.get('street', ''),
                city=data.get('city', ''),
                state=data.get('state', ''),
                postal_code=data.get('postal_code', ''),
            )

    class Update:
        @staticmethod
        def event(data, obj):
            obj.name = data.get('name', '')
            obj.description = data.get('description', '')
            obj.save()
            return obj

        @staticmethod
        def image(data, user):
            image = Helper.Get.image(data, user)
            caption = data.get('caption', '')
            if caption:
                image.caption = caption
            is_profile_picture = data.get('is_profile_picture', 'off') == 'on'
            if is_profile_picture and not image.is_profile_picture:
                Images.objects.filter(
                    user=user,
                    is_profile_picture=True
                ).update(is_profile_picture=False)
                image.is_profile_picture = True
            image.save()


