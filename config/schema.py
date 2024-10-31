from rest_framework_json_api.schemas.openapi import SchemaGenerator as JSONAPISchemaGenerator


class MySchemaGenerator(JSONAPISchemaGenerator):
    """
    Describe my OAS schema info in detail (overriding what DRF put in) and list the servers where it can be found.
    """
    def get_schema(self, request, public):
        schema = super().get_schema(request, public)
        schema['info'] = {
            'version': '1.0',
            'title': 'my demo API',
            'description': 'A demonstration of [OAS 3.0](https://www.openapis.org)',
            'contact': {
                'name': 'my name'
            },
            'license': {
                'name': 'BSD 2 clause',
                'url': 'https://github.com/django-json-api/django-rest-framework-json-api/blob/main/LICENSE',
            }
        }
        schema['servers'] = [
            {'url': 'http://localhost/v1', 'description': 'local docker'},
            {'url': 'http://localhost:8000/v1', 'description': 'local dev'},
            {'url': 'https://api.example.com/v1', 'description': 'demo server'},
            {'url': '{serverURL}', 'description': 'provide your server URL',
             'variables': {'serverURL': {'default': 'http://localhost:8000/v1'}}}
        ]
        return schema
