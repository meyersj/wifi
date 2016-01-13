function ScaleFactory(w, h, window_size) {
    this.w = w;
    this.h = h;
    this.window_size = window_size;
}

ScaleFactory.prototype = {
    constructor: ScaleFactory,
    windowAge: function(start) {
        return d3.scale.pow().exponent(1/2)
            .domain([start + (this.window_size * 60), start])
            .range(["blue", "white"]);
    },
    windowDuration: function() {
        return d3.scale.linear()
            .domain([0, this.window_size * 60])
            .range([5, 15]);
    },
    windowSignal: function() {
        return d3.scale.linear()
            .domain([-30, -100])
            .range([0 + 50, this.w - 50]);
    },
    windowTime: function(start) {
        return d3.scale.linear()
            .domain([start, start + (60 * this.window_size)])
            .range([this.h - 50, 0 + 50]);
    },
    hourPingRate: function() {
        var MAX_PING_PER_HOUR = 12;
        var MIN_RADIUS = 5;
        var MAX_RADIUS = 15;
        return d3.scale.linear()
            .domain([1, MAX_PING_PER_HOUR])
            .range([MIN_RADIUS, MAX_RADIUS]);
    },
    hourSignal: function() {
        return d3.scale.linear()
            .domain([-30, -100])
            .range(["#3E932A", "white"]);

    },
    hourTime: function(start) {
        var HOUR = 3600;
        return d3.scale.linear()
            .domain([start, start + HOUR])
            .range([0 + 50, this.w - 50]);
    }
}
