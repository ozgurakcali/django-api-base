from django.utils import six
from rest_framework.compat import SHORT_SEPARATORS, LONG_SEPARATORS, INDENT_SEPARATORS
from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json


class NormalizedJSONRenderer(JSONRenderer):
    """
    Normalized JSON Renderer, adding passed messages to response
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """

        if data is None:
            return bytes()

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        if 'pagination' not in data:
            # Regular response, encapsulate data in `body` field. Paginated responses already normalized in
            # our normalized paginator
            data = {
                'body': data
            }

        # If messages are provided in response, add them
        if hasattr(renderer_context['response'], 'messages'):
            data['messages'] = renderer_context['response'].messages
        else:
            data['messages'] = []

        ret = json.dumps(
            data, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=separators
        )

        if isinstance(ret, six.text_type):
            ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
            return bytes(ret.encode('utf-8'))

        return ret
