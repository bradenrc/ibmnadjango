import django_tables2 as tables
from .models import Person


class PersonTable(tables.Table):
    #country = tables.RelatedLinkColumn()
    class Meta:
        model = Person
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}