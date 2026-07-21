from django.apps import AppConfig


class ClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client'
    verbose_name = 'Administration JCEM GROUPE TOGO'

    def ready(self):
        from django.contrib import admin

        admin.site.site_header = 'JCEM GROUPE TOGO'
        admin.site.site_title = 'JCEM Admin'
        admin.site.index_title = 'Tableau de bord'
