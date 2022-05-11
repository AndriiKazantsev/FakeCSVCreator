from django.apps import AppConfig


class FakeSchemesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FakeCSVCreator'
