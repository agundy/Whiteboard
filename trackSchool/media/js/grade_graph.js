var graph_width = 200;
var graph_height = 200;
var bar_height = 175;
var bar_width = 35;
var bar_padding = 25;
var padding = 0;
var canvas;
var grades;
var GREEN = '#0AEA0F';
var YELLOW_GREEN = '#C5EA0A';
var YELLOW = '#E7EA0A';
var ORANGE = '#FFA000';
var RED = '#EA200A';

var init = function(){
    canvas = document.getElementById("canvas");
    canvas.width = graph_width;
    canvas.height = graph_height;
    context = canvas.getContext("2d");
    initDom();
    graph(grades);
}

function initDom(){
    $(canvas).css({"display":"block"});
};


var graph = function(grades){
    context.clearRect(0,0,graph_width,graph_height);
    context.font = '13px';
    context.textBaseline = 'top';
    for(var i = 0; i < grades.length; i++){
        if (grades[i]['grade'] >= 90) {
            context.fillStyle = GREEN;
        } else if(grades[i]['grade'] >= 80){
            context.fillStyle = YELLOW_GREEN;
        } else if(grades[i]['grade'] >= 70){
            context.fillStyle = YELLOW;
        } else if(grades[i]['grade'] >= 60){
            context.fillStyle = ORANGE;
        } else if(grades[i]['grade'] < 60){
            context.fillStyle = RED;
        };
        context.fillRect(i*bar_padding +i*bar_width + padding,bar_height*(1-(grades[i]['grade']/100)),bar_width,bar_height*(grades[i]['grade'])/100)
        context.fillStyle = '#000';
        context.fillText(grades[i]['course'],i*bar_padding+ i*bar_width+padding,graph_height-10);
        console.log(grades[i]);
    }
}

$.get("/student/js_grades/",{request:'{{ csrf_token }}'}).done(function( data ) {
    grades = data;
    init();
});
