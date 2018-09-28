var svg = d3.select("svg");
var margin = {top: 20, right: 20, bottom: 50, left: 60};
var width = +svg.attr("width") - margin.left - margin.right;
var height = +svg.attr("height") - margin.top - margin.bottom;
var g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var parseTime = d3.timeParse('%Y-%m-%d %H:%M:%S');

var x = d3.scaleTime()
    .rangeRound([0, width]);

var y = d3.scaleLinear()
    .rangeRound([height, 0]);

var line = d3.line()
    .x(function(d) { return x(d.time); })
    .y(function(d) { return y(d.load); });

var area = d3.area()
    .defined(line.defined())
    .x(line.x())
    .y1(line.y())
    .y0(y(0));



d3.json("/stats", function(error, data) {
  if (error) throw error;

  // format the data
  data.forEach(function(d) {
      d.time = parseTime(d.time);
      d.load = +d.load;
  });

  x.domain(d3.extent(data, function(d) { return d.time; }));
  y.domain(d3.extent(data, function(d) { return d.load; }));

  g.append("g")
   .attr("transform", "translate(0," + height + ")")
   .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%H:%M")))
   .select(".domain")
   
  g.append("text")
   .attr("transform","translate(" + (width/2) + " ," + (height + margin.top + 20) + ")")
   .attr("font-weight", "bold")
   .style("text-anchor", "middle")
   .text("Time")

  g.append("g")
  .call(d3.axisLeft(y))

  g.append("text")
  .attr("fill", "#000")
  .attr("transform", "rotate(-90)")
  .attr("y", 0 - margin.left)
  .attr("x",30 - (height / 2))
  .attr("dy", "0.71em")
  .attr("font-weight", "bold")
  .attr("text-anchor", "end")
  .text("load avg");

  g.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", "steelblue")
  .attr("stroke-linejoin", "round")
  .attr("stroke-linecap", "round")
  .attr("stroke-width", 1.5)
  .attr("d", line);
});





