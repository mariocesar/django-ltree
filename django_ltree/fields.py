from django.db.models.fields import TextField


class PathField(TextField):
    def db_type(self, connection):
        return 'ltree'

