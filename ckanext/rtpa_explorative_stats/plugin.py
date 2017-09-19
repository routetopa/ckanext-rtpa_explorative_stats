import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from logging import getLogger
from ckan.common import json
import ckan as ckan

log = getLogger(__name__)

class Rtpa_Explorative_StatsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'rtpa_explorative_stats')

    # IResourceView
    
    def info(self):
        return { 
                 'name': 'Rtpa_Explorative_Stats',
                 'title': 'Stats',
                 'icon': 'table',
                 'default_title': 'Stats',
               }

    def can_view(self, data_dict):
    	#return True
    	resource = data_dict['resource']
    	
        _format = resource.get('format', None)
        if (resource.get('datastore_active') or resource.get('url') == '_datastore_only_resource'):
            return True 
        if _format:
            return _format.lower() in ['csv', 'tsv', 'xls', 'xlsx']
        else:
            return False

    def preview_template(self, context, data_dict):
		return "rtpa_explorative_stats-view.html"

    def setup_template_variables(self, context, data_dict):
        return {'resource_json': json.dumps(data_dict['resource']),
        		'resource_view_json': json.dumps(data_dict['resource_view'])}


'''
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from django.http import HttpResponse
from pandas.io.json import json_normalize
from ckan.common import json
import ckan as ckan


class Rtpa_Explorative_StatsPlugin(plugins.SingletonPlugin):
	
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView, inherit=True)
    

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        #toolkit.add_public_directory(config_, 'public')
        #toolkit.add_resource('fanstatic', 'rtpa_explorative_stats')
    
	def view_template(self, context, data_dict):
		return "rtpa_explorative_stats-view.html"

	#def can_view(self, data_dict):
		#print ("\n\n\n\n\nTEST\n\n\n\n")
		#return True

	def info(self):
		return{
			'name': 'rtpa_explorative_stats',
			'title': 'Stats',
			'icon': 'table',
			'default_title': 'Stats',
			}
	
        
    #def box_plot(self, data_dict):
		#print (context['data'])
		
		try:
			url = settings.CKAN_URL + "/api/action/datastore_search?resource_id=" + resource_id + "&limit=99999"
			res = urlopen(url)
			data = json.loads(res.read())
			df = json_normalize(data["result"]["records"])
			fields = data["result"]["fields"]
			numeric_fields = [f["id"] for f in fields if f["type"] == "numeric"]
			df[numeric_fields] = df[numeric_fields].apply(pd.to_numeric)
			del df["_id"] 
			color = dict(boxes='#2196F3', whiskers='#2196F3', medians='#007DBE', caps='#2196F3')
			with mutex:
				box = df.plot.box(color=color)
				plt.subplots_adjust(bottom=0.25)
				plt.xticks(rotation=90)
				plt.tight_layout()
				fig = box.get_figure()
				fig.set_facecolor('white')
				canvas = FigureCanvas(fig)
				response = HttpResponse(content_type='image/png')
				canvas.print_png(response)
			return {'boxplot': json.dumps(response) }
		except Exception as e:
			return {'boxplot_message': str(e)}'''
			

