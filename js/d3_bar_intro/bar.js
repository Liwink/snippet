translation_dic = {
  "goal": "进球",
  "shot_on_target": "射正",
  "shot_off_target": "射偏",
  "successful_pass": "传球成功",
  "unsuccessful_pass": "传球失败",
  "ctrl_ratio": "控球率",
  "tackle_won": "抢断",
  "save": "扑救",
  "goal_against": "失球",
}

window.onscroll = scroll;

function scroll() {
  if( window.pageYOffset > 320) {
    navCard = document.getElementsByClassName("nav-card")
    navCard[0].style.position = 'fixed'
    navCard[0].style.top = '80px'
  }
  else {
    navCard = document.getElementsByClassName("nav-card")
    navCard[0].style.position = 'relative'
    navCard[0].style.top = '10px'
  }
}

function httpGetAsync(theUrl, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState==4) {
      callback(JSON.parse(xmlHttp.responseText))
    }
  }
  xmlHttp.open("GET", theUrl, true);
  xmlHttp.send(null)
}

httpGetAsync("/v1/visualization/564446bfc8f97c48711e1d78", generateChart)

function generateChart(data) {

  generateBars(data, "shot_on_target")
  generateBars(data, "successful_pass")
  generateBars(data, "ctrl_ratio")
  generateBars(data, "tackle_won")
  generateBars(data, "save")
}

function generateBars(data, bar_type) {

  data.sort(function(a, b) {
      return parseFloat(b[bar_type]) - parseFloat(a[bar_type]);
  });

  switch (bar_type) {
    case ("shot_on_target"):
      data.sort(function(a, b) {
          return parseFloat(b["goal"]) - parseFloat(a["goal"]);
      });
      var maxCount = d3.max(data, function(d, i) {
          return Math.max(d["shot_on_target"], d["shot_off_target"])
      });
      break;
    case ("save"):
      data.sort(function(a, b) {
          return parseFloat(-b["goal_against"]) + parseFloat(a["goal_against"]);
      });
      var maxCount = d3.max(data, function(d, i) {
          return Math.max(d["goal_against"], d["save"])
      });
      break;
    default:
      data.sort(function(a, b) {
          return parseFloat(b[bar_type]) - parseFloat(a[bar_type]);
      });
      var maxCount = d3.max(data, function(d, i) {
          return d[bar_type]
      });
      break;
  }

  

  // var w = document.getElementById("main").offsetWidth
  var w = document.getElementsByClassName("card")[0].offsetWidth

  var margin = {top: 14, right: 60, bottom: 60, left: 60},
      width = w - margin.left - margin.right,
      height = width * 0.33
      barWidth = width / data.length;

  window.selected = 0

  var color = d3.scale.category20();

  var x = d3.scale.ordinal()
      .domain(data.map(function(d) { return d.team_name; }))
      .rangeRoundBands([0, width]);

  var y = d3.scale.linear()
      .domain([maxCount, 0])
      .range([0, height]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var chart = d3.select("." + bar_type)
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  chart.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      // .attr("transform", "rotate(90)")
      .call(xAxis)
    .selectAll("text")
      .attr("transform", "rotate(45)")
      .style("text-anchor", "start")
      .attr("dy", ".70em");

  switch (bar_type) {
    case ("shot_on_target"):
      generateBar(3, 0, "goal");
      generateBar(3, 1, bar_type);
      generateBar(3, 2, "shot_off_target");
      generateLegend(["goal", bar_type, "shot_off_target"]);
      break;
    case ("save"):
      generateBar(2, 0, "goal_against");
      generateBar(2, 1, bar_type);
      generateLegend(["goal_against", bar_type]);
      break;
    case ("successful_pass"):
      generateBar(2, 0, "successful_pass");
      generateBar(2, 1, "unsuccessful_pass");
      generateLegend(["successful_pass", "unsuccessful_pass"]);
      break;
    default:
      generateBar(1, 0, bar_type);
      generateLegend([bar_type]);
      break;
  }

  

  function generateBar(n, j, stat_type) {
    // barWidth = width / (data.length * n);

    var bar = chart.selectAll(".bar" + j)
        .data(data)
      .enter().append("g")
      .attr("transform", function(d, i) { return "translate(" + (i + 0.66/n * j + 0.17 ) * barWidth + ",0)"; })
      .attr("width", barWidth)
      // .append("group")

    bar.append("rect")
        // .attr("transform", function(d, i) { return "translate(" + i * barWidth + ",0)"; })
        // .attr("x", function(d) { return x(d.team_name); })
        .attr("y", function(d) { return y(d[stat_type]); })
        .attr("name", function(d) { return d["team_name"] })
        .attr("class", "bar")
        .style("fill", function (d, i) { return color(j); })
        .attr("height", function(d) { return height - y(d[stat_type]); })
        .attr("width", barWidth * 0.66/n)
        .style("cursor", "pointer")
        .on({"click": changeOpacityByName});

    bar.append("text")
        // .attr("transform", function(d, i) { return "translate(" + i * barWidth + ",0)"; })
        // .attr("x", function(d) { return x(d.team_name); })
        .attr("y", function(d) { return y(d[stat_type]); })
        .attr("transform", function(d, i) { return "translate(" + 0.33 * barWidth / n + ",0)"; })
        .attr("height", function(d) { return height - y(d[stat_type]) + 9; })
        .attr("width", barWidth)
        .style("text-anchor", "middle")
        .style("font", (16 - 2 * n) + "px Open Sans")
        .attr("dy", "-.3em")
        .text(function(d) { return d[stat_type] });


    function changeOpacityByName(name) {
      name = this.getAttribute("name")
      // selected = 0

      all = document.getElementsByClassName("bar")
      elements = document.getElementsByName(name)

      if (elements[0].style.opacity == 1 && window.selected == 1) {
        for (var i=0, max=all.length; i < max; i++) {
             all[i].style.opacity = 1
        }
        window.selected = 0
      }
      else {
        for (var i=0, max=all.length; i < max; i++) {
             all[i].style.opacity = 0.3
        }
        for (var i=0, max=elements.length; i < max; i++) {
             elements[i].style.opacity = 1
        }
        window.selected = 1
      }
      
    }

    // bar.on("click", console.log("lalala"))
  }

  // Draw legend
  function generateLegend(types) {
    var legendRectSize = 18,
        legendSpacing  = 4,
        gapBetweenGroups = 10,
        spaceForLabels   = 150,
        spaceForLegend   = 150;

    var legend = chart.selectAll('.legend')
        .data(types)
        .enter()
        .append('g')
        .attr('transform', function (d, i) {
            var height = legendRectSize + legendSpacing;
            var offset = -gapBetweenGroups/2;
            var horz = width - spaceForLegend;
            var vert = i * height - offset;
            return 'translate(' + horz + ',' + vert + ')';
        });

    legend.append('rect')
        .attr('width', legendRectSize)
        .attr('height', legendRectSize)
        .style('fill', function (d, i) { return color(i); })
        .style('stroke', function (d, i) { return color(i); });

    legend.append('text')
        .attr('class', 'legend')
        .attr('x', legendRectSize + legendSpacing)
        .attr('y', legendRectSize - legendSpacing)
        .text(function (d) { return translation_dic[d]; });

  }
}


