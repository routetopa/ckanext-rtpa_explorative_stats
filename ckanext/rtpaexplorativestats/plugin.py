import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from logging import getLogger
from ckan.common import json
import ckan as ckan
import urllib2
import pandas as pd


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
               
    def boxplot(self, context, data_dict):
		datasetId=(data_dict['resource']['id'])
		(ckanprotocol,ckanip)=ckan.lib.helpers.get_site_protocol_and_host()
		ckanurl=ckanprotocol+'://'+ckanip
		datadownloadurl=ckanurl+'/api/3/action/datastore_search?resource_id='+datasetId
		data=json.loads(urllib2.urlopen(datadownloadurl).read())
		Dataframe=pd.read_json(json.dumps(data['result']['records']))
		try:
			del Dataframe['_id']
			del Dataframe['Id']
		except:
			Done=True
		NumericColumns=(Dataframe.select_dtypes(exclude=['object','datetime']).columns)
		CheckNumericColumns=[]
		CheckNumericColumns=(NumericColumns.tolist())
		if not CheckNumericColumns:
			return False
		temp=[]
		DataBoxPlot=[]
		for column in NumericColumns:
			DataColumn=Dataframe[column].tolist()
			NumericDataColumn=[]
			DataBoxPlot.append([DataColumn,column])
		return DataBoxPlot              
     
               
    def can_view(self, data_dict):
		resource = data_dict['resource']
		_format = resource.get('format', None)
		if (resource.get('datastore_active') or resource.get('url') == '_datastore_only_resource'):
			return True 
		if _format:
			return _format.lower() in ['csv', 'tsv', 'xls', 'xlsx']
		else:
			return False
        
    def view_template(self, context, data_dict):
		#self.boxplot(context, data_dict)
		return "rtpaexplorativestats-view.html"
        
    def setup_template_variables(self, context, data_dict):
		Data=self.boxplot(context, data_dict)
		return {'resource_json': json.dumps(Data)}

