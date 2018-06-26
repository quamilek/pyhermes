"""
Proxy for all settings of pyhermes

Handles:
    * django settings
    * custom calling of `update` method

Use `HERMES_SETTINGS` for all of pyhermes settings.
"""
import six

from pyhermes.utils import AttributeDict  # noqa

try:
    from django.conf import settings as user_settings
except ImportError:
    user_settings = AttributeDict({'HERMES': {}})


from pyhermes.exceptions import PyhermesImproperlyConfiguredError
from pyhermes.utils import Singleton

_DEFAULT_GROUP_NAME = '__default__'
DEFAULTS = {
    'ENABLED': True,
    'BASE_URL': '',
    'URL_ADAPTER': None,
    'PUBLISHING_GROUP': {
        'groupName': _DEFAULT_GROUP_NAME,
    },
    'PUBLISHING_TOPICS': {},
    'SUBSCRIBERS_MAPPING': {},
    'RETRY_MAX_ATTEMTPS': 3,
}
# TODO: publishing timeout


class HermesSettings(six.with_metaclass(Singleton, object)):
    """

    """
    def __init__(self):
        self._wrapper = AttributeDict()

    def __getattr__(self, attr):
        try:
            if self._wrapper:
                return self._wrapper['HERMES'][attr]
            else:
                return getattr(user_settings, 'HERMES', {})[attr]
        except KeyError:
            return DEFAULTS[attr]

    def update(self, **settings):
        if isinstance(user_settings, AttributeDict):
            user_settings['HERMES'].update(settings)
        else:
            if self._wrapper.get('HERMES'):
                self._wrapper['HERMES'].update(settings)
            else:
                self._wrapper['HERMES'] = settings


HERMES_SETTINGS = HermesSettings()


def _validate_hermes_settings(hermes_settings):
    if not hermes_settings.BASE_URL:
        raise PyhermesImproperlyConfiguredError('Hermes BASE_URL not provided')
    if (
        not hermes_settings.PUBLISHING_GROUP or
        hermes_settings.PUBLISHING_GROUP['groupName'] == _DEFAULT_GROUP_NAME
    ):
        raise PyhermesImproperlyConfiguredError(
            'Hermes GROUP info not provided'
        )


# TODO: validate
# _validate_hermes_settings(HERMES_SETTINGS)
