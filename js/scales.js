function ScaleFactory(w, h, window_size) {
    this.w = w;
    this.h = h;
    this.window_size = window_size;
}

ScaleFactory.prototype = {
    constructor: ScaleFactory,
    // COLOR
    windowAge: function(start) {
        return d3.scale.pow().exponent(1/2)
            .domain([start + (this.window_size * 60), start])
            .range(["blue", "white"]);
    },
    // RADIUS
    windowDuration: function() {
        return d3.scale.linear()
            .domain([0, this.window_size * 60])
            .range([5, 15]);
    },
    // X-AXIS
    windowSignal: function() {
        return d3.scale.linear()
            .domain([-30, -100])
            .range([0 + 50, this.w - 50]);
    },
    // Y-AXIS
    windowTime: function(start) {
        return d3.scale.linear()
            .domain([start, start + (60 * this.window_size)])
            .range([this.h - 120, 0 + 60]);
    },
    // RADIUS
    hourPingRate: function() {
        var MAX_PING_PER_HOUR = 12;
        var MIN_RADIUS = 7;
        var MAX_RADIUS = 7; //15;
        return d3.scale.linear()
            .domain([1, MAX_PING_PER_HOUR])
            .range([MIN_RADIUS, MAX_RADIUS]);
    },
    // COLOR
    hourSignal: function() {
        return d3.scale.linear()
            .domain([-30, -100])
            .range(["#3E932A", "white"]);

    },
    // X-AXIS
    hourTime: function(start) {
        var HOUR = 3600;
        return d3.scale.linear()
            .domain([start, start + HOUR])
            .range([0 + 50, this.w - 50]);
    },
    // X-AXIS
    dailyTime: function(start) {
        var HOUR = 3600;
        return d3.scale.linear()
            .domain([start, start + (HOUR * 24)])
            .range([0 + 50, this.w - 50]);
    }
}
