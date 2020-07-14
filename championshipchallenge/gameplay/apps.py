from django.apps import AppConfig


class GameplayConfig(AppConfig):
  name = 'gameplay'

  def ready(self):
    # pylint: disable=unused-import, import-outside-toplevel
    from . import signals
