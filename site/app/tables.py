import django_tables2 as tables
from .models import Person, camping_results


class PersonTable(tables.Table):
    #country = tables.RelatedLinkColumn()
    #product =

    class Meta:
        model = Person
        fields = ('name', 'gender', 'marital', 'age', 'job', 'camping_results__product', 'camping_results__prediction')
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}