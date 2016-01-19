function Legend (svg, scales) {
    this.scales = scales;
    this.svg = svg;
}

Legend.prototype = {
    constructor: Legend,
    drawSignalStrength: function() {
        var signals = _.range(-30, -110, -10);
        var scale = this.scales.windowSignal();
        this.svg.selectAll(".signal-legend").remove();
        this.svg.selectAll(".signal-legend").data(signals).enter()
            .append("text")
            .attr("class", "signal-legend")
            .text(function(d) {
                return d;
            })
            .attr("x", function(d) {
                return scale(d);
            })
            .attr("y", 35);
        
        this.svg.selectAll(".signal-label").remove();
        this.svg.append('text')
            .attr("class", "signal-label")
            .text("RSSI (dBm)")
            .attr("x", this.scales.w / 2)
            .attr("y", 20);
    },
    drawTime: function(start) {
        var recent = start + (this.scales.window_size * 60) 
        var times = _.range(start, recent + 60, 60);
        var scale = this.scales.windowTime(start);
        this.svg.selectAll(".time-legend").remove();
        this.svg.selectAll(".time-legend").data(times).enter()
            .append("text")
            .text(function(d) {
                return Math.round((recent - d) / 60) + " min";
            })
            .attr("class", "time-legend")
            .attr("x", 0)
            .attr("y", function(d) {
                return scale(d);
            });
    }
};
