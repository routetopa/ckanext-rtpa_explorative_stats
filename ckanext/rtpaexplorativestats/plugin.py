import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from logging import getLogger
from ckan.common import json
import ckan as ckan


class RtpaexplorativestatsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'rtpaexplorativestats')
        
        
    def info(self):
        return { 
                 'name': 'rtpaexplorativestats',
                 'title': 'Stats',
                 'icon': 'table',
                 'default_title': 'Stats',
               }
               
    def can_view(self, data_dict):
        return True
        
    def view_template(self, context, data_dict):
        return "rtpaexplorativestats-view.html"
        
    def setup_template_variables(self, context, data_dict):
        return {'resource_json': json.dumps(data_dict['resource']),
        		'resource_view_json': json.dumps(data_dict['resource_view'])}
