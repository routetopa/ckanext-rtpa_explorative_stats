this.ckan.module('rtpaexplorativestats_view', function(jQuery, _) {
	return{
		initialize: function() {
            jQuery.proxyAll(this, /_on/);
            this.el.ready(this._onReady);
		},
		_onReady: function() {
			//console.log( "on ready!" );
			var BoxPlotData=this.options.resource;
			this.renderBoxPlot(BoxPlotData)
			//console.log(BoxPlotData);
			
		},
		renderBoxPlot: function(data){
			console.log("Here...");
            console.log(data);
            //var boxplotdiv=$( document ).ready(function(){
				//return document.getElementById('Boxplot')});
			var boxPlotData=JSON.parse(data)
			console.log(boxPlotData);
			var BoxPlotArray=[];
			for (var i=0 ; i<boxPlotData.length; i++){
				var element = boxPlotData[i];
				console.log(element[0]);
				var tempElement={
					y: element[0],
					type: 'box',
					name: element[1]};
				BoxPlotArray.unshift(tempElement);
			}
			Plotly.newPlot('Boxplot', BoxPlotArray);
/*				
			var y0=[],y1=[]
			for ( i = 0; i < 50; i ++) 
{
    y0[i] = Math.random();
    y1[i] = Math.random();
}

var trace1 = {
  y: y0,
  type: 'box'
};

var trace2 = {
  y: y1,
  type: 'box'
};

var data = [trace1, trace2];

Plotly.newPlot('Boxplot', data);*/	
					
            //Plotly.newPlot(boxplotdiv,data);
            //Plotly.newPlot('Boxplot',data);
            
		}
		
	};
});


/*$( document ).ready(function() {
    console.log( "ready!" );
    $('#Boxplot').fadeOut();
});*/
