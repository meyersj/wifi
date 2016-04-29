function ScaleFactory(w, h, window_size) {
    this.w = w;
    this.h = h;
    this.window_size = window_size;
    this.LEFT_PADDING = 50;
    this.TOP_PADDING = 100;
}

ScaleFactory.prototype = {
    constructor: ScaleFactory,
    // COLOR
    windowAge: function(start) {
        return d3.scale.pow().exponent(1/2)
            .domain([start + (this.window_size * 60), start])
            .range([1, 0.3]);
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
            .domain([-10, -100])
            .range([0 + this.LEFT_PADDING, this.w - 50]);
    },
    // Y-AXIS
    windowTime: function(start) {
        return d3.scale.linear()
            .domain([start, start + (60 * this.window_size)])
            .range([this.h - 120, 0 + this.TOP_PADDING]);
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
            .domain([-10, -100])
            .range(["#7B7B76", "#7B7B76"]);

    },
    // X-AXIS
    hourTime: function(start) {
        var HOUR = 3600;
        return d3.scale.linear()
            .domain([start, start + HOUR])
            .range([0 + this.LEFT_PADDING, this.w - 50]);
    },
    // X-AXIS
    dailyTime: function(start) {
        var HOUR = 3600;
        return d3.scale.linear()
            .domain([start, start + (HOUR * 24)])
            .range([0 + this.LEFT_PADDING, this.w - 50]);
    }
}
