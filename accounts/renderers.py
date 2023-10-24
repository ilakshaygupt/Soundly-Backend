import json

from rest_framework import renderers


class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ""

        # Check if the response status code indicates an error
        if 400 <= renderer_context['response'].status_code < 600:
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({'data': data})

        return response
