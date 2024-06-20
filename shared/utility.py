from rest_framework import serializers
import uuid
from django.core.files.base import ContentFile
import base64

class Base64FileField(serializers.FileField):
    """ Base64 File Field for Serializers instead of sending files. """
    def to_internal_value(self, data):
        try:
            if isinstance(data, str) and ";base64," in data:
                format, file = data.split(";base64,")
                ext = format.split("/")[-1]
                unique_id = uuid.uuid4()
                file = ContentFile(
                    base64.b64decode(file), name=f"{unique_id.urn[9:]}.{ext}"
                )
                return super(Base64FileField, self).to_internal_value(file)
            return super(Base64FileField, self).to_internal_value(data)
        except ValueError:
            raise serializers.ValidationError(
                "Invalid base64 format please add in first data:file/{type};base64,"
            )


class CsrfTokenMixin:
    def dispatch(self, request, *args, **kwargs):
        csrf_token = request.COOKIES.get('csrftoken', '')
        if csrf_token:
            request.META['HTTP_X_CSRFTOKEN'] = csrf_token
        return super().dispatch(request, *args, **kwargs)
    
    def get_headers(self, request):
        headers = super().get_headers(request)
        headers['X-CSRFToken'] = request.META.get('HTTP_X_CSRFTOKEN', '')
        return headers