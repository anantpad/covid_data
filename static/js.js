// Load google charts
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
// Draw the chart and set the chart values
function drawChart() {
  // console.log(JSON.stringify('{{trends}}'));
  var positive_cases = {{positive_cases}};
  var dataRows = [['State','Positive Cases']];
  for ( key in positive_cases ){
    dataRows.push([key, positive_cases[key]])
  }
  var data = google.visualization.arrayToDataTable(dataRows);
  // Optional; add a title and set the width and height of the chart
  var options = {'title':'State-wise Positive Cases', 'width':600, 'height':400};
  // Display the chart inside the <div> element with id="piechart"
  var chart = new google.visualization.ColumnChart(document.getElementById('columnchart'));
  chart.draw(data, options);
}
