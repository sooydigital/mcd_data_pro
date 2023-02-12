// You can reproduce this figure in plotly.js with the following code!

// Learn more about plotly.js here: https://plotly.com/javascript/getting-started

/* Here's an example minimal HTML template
 *
 * <!DOCTYPE html>
 *   <head>
 *     <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
 *   </head>
 *   <body>
 *   <!-- Plotly chart will be drawn inside this div -->
 *   <div id="plotly-div"></div>
 *     <script>
 *     // JAVASCRIPT CODE GOES HERE
 *     </script>
 *   </body>
 * </html>
 */

trace1 = {
  uid: '00e4ba', 
  mode: 'markers', 
  name: 'Our Jobs', 
  type: 'scattermapbox', 
  lat: ['Lattitude', '33.749', '39.9042', '42.3601', '', '35.2271', '41.8781', '', '32.7767', '38.9072', '39.7392', '', '22.3964', '29.7604', '34.0522', '', '25.7617', '', '40.7128', '37.4419', '39.9526', '', '32.7157', '47.6062'], 
  lon: ['Longitude', '-84.388', '116.4074', '-71.0589', '', '-80.8431', '-87.6298', '', '-96.797', '-77.0369', '-104.9903', '', '114.1095', '-95.3698', '-118.2437', '', '-80.1918', '', '-74.0059', '-122.143', '-75.1652', '', '-117.1611', '-122.3321'], 
  marker: {
    sizeref: null, 
    size: ['Size E', '26.5', '16', '46.5', '', '12', '58.5', '', '7', '84.5', '13', '', '10.5', '11', '54.5', '', '8.5', '', '188.5', '44', '18', '', '18.5', '21.5']
  }, 
  text: ['Our Jobs', '53', '32', '93', '', '24', '117', '', '14', '169', '26', '', '21', '22', '109', '', '17', '', '377', '88', '36', '', '37', '43'], 
  visible: true, 
  hoverinfo: 'text+name'
};
trace2 = {
  uid: '507651', 
  mode: 'markers', 
  name: 'Public Jobs', 
  type: 'scattermapbox', 
  lat: ['Lattitude', '33.749', '39.9042', '42.3601', '', '35.2271', '41.8781', '', '32.7767', '38.9072', '39.7392', '', '22.3964', '29.7604', '34.0522', '', '25.7617', '', '40.7128', '37.4419', '39.9526', '', '32.7157', '47.6062'], 
  lon: ['Longitude', '-84.388', '116.4074', '-71.0589', '', '-80.8431', '-87.6298', '', '-96.797', '-77.0369', '-104.9903', '', '114.1095', '-95.3698', '-118.2437', '', '-80.1918', '', '-74.0059', '-122.143', '-75.1652', '', '-117.1611', '-122.3321'], 
  marker: {
    sizeref: null, 
    size: ['Size B', '4', '1.5', '12', '', '3.5', '9', '', '2.5', '13.5', '1.5', '', '1.5', '2', '5.5', '', '1', '', '26.5', '11.5', '1.5', '', '3.5', '.5']
  }, 
  text: ['TOTAL JOBS', '8', '3', '24', '', '7', '18', '', '5', '27', '3', '', '3', '4', '11', '', '2', '', '53', '23', '3', '', '7', '0'], 
  hoverinfo: 'text+name'
};
data = [trace1, trace2];
layout = {
  geo: {}, 
  title: 'Public Jobs Vs. Unlisted Jobs', 
  width: 845, 
  height: 474.438, 
  legend: {
    x: 0.2260060115025426, 
    y: 0.0011792682689115556
  }, 
  mapbox: {
    zoom: 0.9650853245504711, 
    pitch: 2, 
    style: 'outdoors', 
    center: {
      lat: 17.775422712281127, 
      lon: -120.48678030960035
    }, 
    bearing: 0
  }, 
  margin: {
    b: 40, 
    l: 40, 
    r: 40, 
    t: 40
  }, 
  autosize: true, 
  hovermode: 'closest', 
  showlegend: true
};
Plotly.plot('plotly-div', {
  data: data,
  layout: layout
});