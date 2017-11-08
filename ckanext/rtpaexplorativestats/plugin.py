import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from logging import getLogger
from ckan.common import json
import ckan as ckan
import urllib2
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import urlparse
try:
	from ckan.common import config
except Exception as e:
	from ckan.common import c
#from pylons import config


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
               
    def ExplorativeStats(self, context, data_dict):
		print(c.remote_addr)
		datasetId=(data_dict['resource']['id'])
		try:
			(ckanprotocol,ckanip)=config.get_site_protocol_and_host()
		except Exception as e:
			ckanip=c.remote_addr
			ckanprotocol='http'
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

		TableData=Dataframe[NumericColumns.tolist()].copy()
		#NumericColumnsLis=
		##ExplorativeStats table

		#print(SummaryDataframe.tolist())
		
		####Correlation Matrix
		Correlation=self.CorrelationMatrix(TableData)
		###SummaryDataTable
		(SummaryData,SummaryDataColumns)=self.SummaryDataTable(TableData,NumericColumns)
		
		return DataBoxPlot,SummaryData,SummaryDataColumns,Correlation
		'''
#    def get_site_protocol_and_host(self):		site_url = config.get('ckan.site_url', None)
		if site_url is not None:
			parsed_url = urlparse.urlparse(site_url)
			return (
			parsed_url.scheme.encode('utf-8'),
			parsed_url.netloc.encode('utf-8')
			)
		return (None, None)'''

    def SummaryDataTable(self, TableData, NumericColumns):
		SummaryData=[]
		SummaryDataColumns=["Summary"]+NumericColumns.tolist()
		#SummaryData.append(SummaryDataColumns)
		
		SummaryData.append(["25%"]+(TableData.quantile(0.25).tolist()))
		SummaryData.append(["50%"]+TableData.quantile(0.5).tolist())
		SummaryData.append(["75%"]+TableData.quantile(0.75).tolist())
		
		SummaryData.append(["max"]+(TableData.max()).tolist())
		SummaryData.append(["min"]+(TableData.min()).tolist())
		SummaryData.append(["std"]+(TableData.std()).tolist())
		SummaryData.append(["mean"]+(TableData.mean()).tolist())
		SummaryData.append(["count"]+(TableData.count()).tolist())
			
		return SummaryData,SummaryDataColumns
	
		
    def CorrelationMatrix(self, dataframe):
		corr = dataframe.corr()
		fig, ax = plt.subplots()
		cax = ax.matshow(corr)
		fig.colorbar(cax)
		plt.xticks(range(len(corr.columns)), corr.columns);
		plt.yticks(range(len(corr.columns)), corr.columns);
		plt.xticks(rotation=90)
		plt.tight_layout()
		CorrelationFile=BytesIO()
		plt.savefig(CorrelationFile, format='png')
		CorrelationFile.seek(0) 
		CorrelationPNG = base64.b64encode(CorrelationFile.getvalue())
		return CorrelationPNG
		
     
               
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
		#self.ExplorativeStats(context, data_dict)
		return "rtpaexplorativestats-view.html"
        
    def setup_template_variables(self, context, data_dict):
		(Data,SummaryData,SummaryColumns,Correlation)=self.ExplorativeStats(context, data_dict)
		return {'resource_json': json.dumps(Data),
				'resource_summarydata': SummaryData,
				'resource_summaryheaders':SummaryColumns,
				'resource_correlationmatrix' : Correlation}

