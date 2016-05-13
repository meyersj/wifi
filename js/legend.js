function Legend (svg, scales) {
    this.scales = scales;
    this.svg = svg;
    this.font_family = 'sans-serif';
    this.LEFT_PADDING = 50;
    this.TOP_PADDING = 100;
}

Legend.prototype = {
    constructor: Legend,
    clearUserSummaryLegend: function() {
        this.svg.selectAll(".user-summary-legend").remove();
        this.svg.selectAll(".user-summary-line").remove();
    },
    drawUserSummaryLegend: function() {
        // UL = upper left, UR = upper right, BL = bottom left ...
        var UL = [this.LEFT_PADDING, this.scales.h - 60];
        var UR = [this.scales.w - 50, this.scales.h - 60];
        var BL = [this.LEFT_PADDING, this.scales.h - 30];
        var BR = [this.scales.w - 50, this.scales.h - 30];
        var VOFF = 20;
        var labels = [
            [UL[0], UL[1] - VOFF, "-60 min"],
            [(UR[0] - UL[0]) / 2 + 50, UL[1] - VOFF, "-30 min"],
            [UR[0], UR[1] - VOFF, "Current"],
            [BL[0], BL[1] + VOFF + 10, "-24 hr"],
            [(BR[0] - BL[0]) / 2 + 50, BL[1] + VOFF + 10, "-12 hr"],
            [BR[0], BR[1] + VOFF + 10, "Current"],
        ];
        // [x, y]
        var lines = [
            // horizontal lines
            [UL, UR],
            [BL, BR],
            // vertical lines
            [[UL[0], UL[1] - 10], [BL[0], BL[1] + 10]],
            [[UR[0], UR[1] - 10], [BR[0], BR[1] + 10]],
        ];

        this.clearUserSummaryLegend();

        this.svg.selectAll(".user-sumamry-legend").data(labels).enter()
            .append("text")
            .attr("class", "user-summary-legend")
            .attr("font-family", this.font_family)
            .attr("x", function(d) {
                return d[0];
            })
            .attr("y", function(d) {
                return d[1];
            })
            .text(function(d) {
                return d[2];
            });

        var lineFunc = d3.svg.line()
            .x(function(d) { return d[0]; })
            .y(function(d) { return d[1]; })
            .interpolate("linear");

        this.svg.selectAll(".user-sumamry-line").data(lines).enter()
            .append("path")
            .attr("class", "user-summary-line")
            .attr("d", function(d) {
                return lineFunc(d);
            })
            .attr("stroke", "grey")
            .attr("stroke-width", "1");

    },
    drawSignalStrength: function(w) {
        var signals = _.range(-10, -110, -10);
        var scale = this.scales.windowSignal();
        this.svg.selectAll(".signal-legend").remove();
        this.svg.selectAll(".signal-legend").data(signals).enter()
            .append("text")
            .attr("class", "signal-legend")
            //.attr("font-family", this.font_family)
            .text(function(d) {
                return d;
            })
            .attr("x", function(d) {
                return scale(d);
            })
            .attr("y", this.TOP_PADDING - 20);

        this.svg.selectAll(".signal-label").remove();
        this.svg.append('text')
            .attr("class", "signal-label")
            .text("RSSI (dBm)")
            .attr("x", this.scales.w / 2)
            .attr("y", this.TOP_PADDING - 35);
    },
    drawTime: function(start) {
        var recent = start + (this.scales.window_size * 60);
        var times = _.range(start, recent + 60, 60);
        var scale = this.scales.windowTime(start);
        this.svg.selectAll(".time-legend").remove();
        this.svg.selectAll(".time-legend").data(times).enter()
            .append("text")
            .text(function(d) {
                return Math.round((recent - d) / 60) + " min";
            })
            .attr("class", "time-legend")
            .attr("x", 5)
            .attr("y", function(d) {
                return scale(d);
            });
    },
    drawDeviceLegend: function(window_size) {
        var data = [
            //{"name":"new", "class":"wifi-unknown", "size":15},
            //{"name":"old", "class":"wifi-unknown", "size":5},
            {"name":"Device", "class":"wifi-device"},
            {"name":"Mixed","class":"wifi-hybrid"},
            {"name":"AP", "class":"wifi-access-point"},
            {"name":"unknown", "class":"wifi-unknown"}
        ];

        function spacing(i, label) {
            return i * 42 + 22;
        }
        svg.selectAll(".device-legend")
            .data(data)
            .enter()
            .append("circle")
            .attr('r', function(d) {
                if (d.hasOwnProperty("size")) {
                    return d.size;
                }
                return 10;
            })
            .attr('class', function(d) {
                return "device-legend wifi-node " + d.class;
            })
            .attr('cx', function(d, i) {
                return spacing(i, d.name);
            })
            .attr('cy', function(d) {
                return 22;
            });

        svg.selectAll(".device-labels")
            .data(data)
            .enter()
            .append("text")
            .attr("class", "device-labels")
            .attr('x', function(d, i) {
                return spacing(i, d.name);
            })
            .attr('y', function(d) {
                return 49;
            })
            .text(function(d) {
                return d.name;
            });
    }
};
