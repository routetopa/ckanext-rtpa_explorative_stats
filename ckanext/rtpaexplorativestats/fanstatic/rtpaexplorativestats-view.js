this.ckan.module('rtpaexplorativestats_view', function(jQuery, _) {
	return{
		initialize: function() {
            jQuery.proxyAll(this, /_on/);
            this.el.ready(this._onReady);
		},
		_onReady: function() {
			var BoxPlotData=JSON.parse(this.options.resource);
			console.log(BoxPlotData);
			this.renderBoxPlot(BoxPlotData);
					
		},
		renderBoxPlot: function(data){
			console.log("Here...");
            console.log(data);
            boxPlotData=data;
			if(boxPlotData != false)
			{
				var BoxPlotArray=[];
				if (boxPlotData.length>0)
				{
					for (var i=0 ; i<boxPlotData.length; i++)
					{
						var element = boxPlotData[i];
						console.log(element[0]);
						var tempElement={
							y: element[0],
							type: 'box',
							name: element[1]};
						BoxPlotArray.unshift(tempElement);
					}
				}
				Plotly.newPlot('Boxplot', BoxPlotArray);

			}
			else
			{
				$('#Boxplot').text("Error! No numeric data found!");
			}
			
            
		}
		
			
		
		
	};
});

