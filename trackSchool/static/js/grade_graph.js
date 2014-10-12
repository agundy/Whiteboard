var GREEN = '#0AEA0F';
var YELLOW_GREEN = '#C5EA0A';
var YELLOW = '#E7EA0A';
var ORANGE = '#FFA000';
var RED = '#EA200A';

var grades;

$.get("/student/js_grades/",{request:''}).done(function( data ) {
    // Get grades information from ajax request
    grades = data;
    InitChart();
});


function InitChart() {
    var barData = [];
    
    for(var i = 0; i < grades.length; i++){
        barData.push({
            'x': grades[i]['course'],
            'y': grades[i]['grade'],
            'i': i
        })
    };
    console.log("passed");


    var vis = d3.select('#visualisation'),
    WIDTH = 325,
    HEIGHT = 300,
    MARGINS = {
      top: 20,
      right: 20,
      bottom: 20,
      left: 50
    },
    xRange = d3.scale.ordinal().rangeRoundBands([MARGINS.left, WIDTH - MARGINS.right], 0.1).domain(barData.map(function (d) {
      return d.x;
    })),


    yRange = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([0,
        d3.max([100,      
            d3.max(barData, function (d) {
                return d.y;
              })
            ])
    ]),
    xAxis = d3.svg.axis()
      .scale(xRange)
      .tickSize(5)
      .tickSubdivide(true),

    yAxis = d3.svg.axis()
      .scale(yRange)
      .tickSize(5)
      .orient("left")
      .tickSubdivide(true);


    vis.append('svg:g')
    .attr('class', 'x axis')
    .attr('transform', 'translate(0,' + (HEIGHT - MARGINS.bottom) + ')')
    .call(xAxis);

    vis.append('svg:g')
    .attr('class', 'y axis')
    .attr('transform', 'translate(' + (MARGINS.left) + ',0)')
    .call(yAxis);

    vis.selectAll('rect')
    .data(barData)
    .enter()
    .append('rect')
    .attr('x', function (d) {
      return xRange(d.x);
    })
    .attr('y', function (d) {
      return yRange(d.y);
    })
    .attr('width', xRange.rangeBand())
    .attr('height', function (d) {
      return ((HEIGHT - MARGINS.bottom) - yRange(d.y));
    })
    .attr('fill', function(d) {
        if (d.y >= 90){
            return GREEN;
        } else if(d.y >= 80){
            return YELLOW_GREEN;
        } else if(d.y >= 70){
            return YELLOW;
        } else if(d.y >= 60){
            return ORANGE;
        } else if(d.y < 60){
            return RED;
        }
    });
}