import django_tables2 as tables
from .models import Person, camping_results, Demos, SuperHeroFight
from django.utils.html import format_html


class PersonTable(tables.Table):
    class Meta:
        model = Person
        fields = ('name', 'gender', 'marital', 'age', 'job', 'camping_results__product', 'camping_results__prediction')
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}


class HtmlColumn(tables.Column):
    def render(self, value):
        return format_html(value)


class DemosTable(tables.Table):
    path = tables.URLColumn()
    description = HtmlColumn()
    class Meta:
        model = Demos
        fields = {'name', 'description', 'path'}
        sequence = ('name', 'description', 'path')
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}



class SuperHeroTable(tables.Table):

    heroone_score = tables.Column("Score")
    herotwo_score = tables.Column("Score")

    def render_winner(self, value):
        return SuperHeroFight.heroes[value][1]

    class Meta:
        model = SuperHeroFight
        fields = {'SuperHeroOne', 'heroone_score', 'SuperHeroTwo', 'herotwo_score', 'winner'}
        sequence = ('SuperHeroOne', 'heroone_score', 'SuperHeroTwo', 'herotwo_score', 'winner')
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}
