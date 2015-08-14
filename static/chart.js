//Make jquery Deferred objects for all the events we need to wait for: Loading Google Charts, initializing chart, document.ready
var _chartload_deferred = new $.Deferred();
google.load('visualization', '1', {packages:['orgchart'], 'callback': _chartload_deferred.resolve});
var _chart_ready_deferred = _chartload_deferred.then(function() {
  _initChart();
});
var _doc_ready_deferred = new $.Deferred();
$( document ).ready( function() {
  _doc_ready_deferred.resolve();
});

//Implement String.format:
String.prototype.format = function() {
  var args = arguments;
  return this.replace(/{(\d+)}/g, function(match, number) { 
    return typeof args[number] != 'undefined'
      ? args[number]
      : match
    ;
  });
};

function _updateChartFromBodyName(body_name) {
  var q = $("#SPARQLtemplate").html().format(body_name);
  console.log(q);
  $.ajax({
      url: "http://rdfendpoints.appspot.com/ds",
      method: 'GET',
      data: {query: q},
      dataType: 'json',
      success: _docReady_updateChartFromJson,
      timeout: 60000
    });
}

//Bind AJAX data load to hashchange event
$(window).bind( 'hashchange', function( event ) {
  var body_name = event.getState( 'body_name' ) || 'Sun';
  _updateChartFromBodyName( body_name );
});

function _docReady_updateChartFromJson(response) {
  $.when(_chart_ready_deferred, _doc_ready_deferred).done(function() {
    _updateChartFromJson(response)
  });
}
  
function _updateChartFromJson(response) {
    var parentMap = {};
    var labelMap = {};
    $.each(response.results.bindings, function(index, binding){
      if (binding.p.value == 'http://rdfendpoints.appspot.com/tmp-ontology/setlabel') {
          labelMap[binding.s.value] = binding.o.value;
      } else if (binding.p.value == 'http://rdfendpoints.appspot.com/tmp-ontology/setparent') {
          parentMap[binding.s.value] = binding.o.value;          
      } else {
          console.log('ERROR: p is ' + binding.p.value);
      }
    });
    _updateChart(parentMap, labelMap);        
}

var _tbl;
var _chart;
function _initChart() {
    //Initialize _tbl (internal data table drawn on the chart) and _chart
    _tbl = new google.visualization.DataTable();
    _tbl.addColumn('string', 'UrlAndLabel');
    _tbl.addColumn('string', 'ParentUrl');
    _tbl.addColumn('string', 'ToolTip');//Not used but specified by orgchart
    _chart = new google.visualization.OrgChart(document.getElementById('chartPanel'));
    //Get a call to selectHandler() when chart is clicked
    google.visualization.events.addListener(_chart, 'select', function () {
      //Get the rowId which will be the URI for the resource shown
      var rowIndex = _chart.getSelection()[0].row;//This may work badly if more than one node is selected
      var rowId = _tbl.getValue(rowIndex, 0);
      //Change URL fragment of this page, causing a hashchange event
      jQuery.bbq.pushState({'body_name' : rowId.split("/").pop()});
    });
}

function _updateChart(parentMap, labelMap) {
    $.each(labelMap, function (id, label){
        _tbl.addRow(
                [ { v: id, //v is the URL that child nodes can point to
                    f: '<p>' + label + '</p>'},
                    parentMap[id],
                    ""//No tooltip
                ]);
    })
    _chart.draw(_tbl, {allowHtml:true, size:'large'});
}