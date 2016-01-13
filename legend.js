function xAxisLabelBuilder(svg) {
    var signals = _.range(-30, -110, -10);
    var xScale = buildXScale(w);
   
    svg.selectAll(".signal-legend").data(signals).enter()
        .append("text")
        .text(function(d) {
            return d;
        })
        .attr("class", "signal-legend")
        .attr("x", function(d) {
            return xScale(d);
        })
        .attr("y", 35);
}

function yAxisLabelBuilder(svg, h, start, window_size) {
    var recent = start + (window_size * 60) 
    var times = _.range(start, recent + 60, 60);
    var yScale = buildYScale(h, start, window_size);
    svg.selectAll(".time-legend").data(times).enter()
        .append("text")
        .text(function(d) {
            return (recent - d) / 60 + " min";
        })
        .attr("class", "time-legend")
        .attr("x", 20)
        .attr("y", function(d) {
            return yScale(d);
        });
}

function Legend () {}

Legend.prototype = {
    constructor: Legend,
    setSvg: function(svg) {
        this.svg = svg;
    },
    drawSignalStrength: function(w) {
        this.svg.selectAll(".signal-label").remove();
        this.svg.selectAll(".signal-legend").remove();
        xAxisLabelBuilder(svg);
        this.svg.append('text')
            .text("RSSI (dBm)")
            .attr("class", "signal-label")
            .attr("x", w / 2)
            .attr("y", 20);
    },
    drawTime: function(h, start, window_size) {
        this.svg.selectAll(".time-label").remove();
        this.svg.selectAll(".time-legend").remove();
        yAxisLabelBuilder(svg, h, start, window_size)
    }
};
