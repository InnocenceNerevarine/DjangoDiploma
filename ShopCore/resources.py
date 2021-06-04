from import_export import resources
from .models import Contact


class ContactResource(resources.ModelResource):

    class Meta:
        model = Contact
        fields = ('email', 'date')
        export_order = ('email', 'date')
        widgets = {
            'date': {'format': '%d.%m.%Y'},
        }



