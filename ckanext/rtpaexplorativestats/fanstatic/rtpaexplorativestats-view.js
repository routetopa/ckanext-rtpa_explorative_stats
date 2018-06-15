this.ckan.module('rtpaexplorativestats_view', function(jQuery, _) {
    return{
        initialize: function() {
            jQuery.proxyAll(this, /_on/);
            this.el.ready(this._onReady);
        },
        _onReady: function() {
            console.log(this.options.resource);
            var BoxPlotData=JSON.parse(this.options.resource.replace(/\bNaN\b/g, "null"));

            //var SummaryDataJSON=JSON.parse(this.options.resource)[1]
            //var SummaryData=JSON.parse(SummaryDataJSON)

            this.summaryTable();
            this.renderBoxPlot(BoxPlotData);

        },
        renderBoxPlot: function(data){
            boxPlotData=data;
            if(boxPlotData != false)
            {
                var BoxPlotArray=[];
                if (boxPlotData.length>0)
                {
                    for (var i=0 ; i<boxPlotData.length; i++)
                    {
                        var element = boxPlotData[i];
                        var tempElement={
                            y: element[0],
                            type: 'box',
                            name: element[1],
                            boxpoints: 'Outliers'};
                        BoxPlotArray.unshift(tempElement);
                    }
                }
                Plotly.newPlot('Boxplot', BoxPlotArray);

            }
            else
            {
                $('#Boxplot').text("Error! No numeric data found!");
            }

        },
        summaryTable: function(){
            $('#Summary').DataTable();
        }

    };
});
