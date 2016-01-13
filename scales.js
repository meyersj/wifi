function buildAgeScale(start, window_size) {
    return d3.scale.pow().exponent(1/2)
        .domain([start + (window_size * 60), start])
        .range(["blue", "white"]);
}

function buildDurationScale(window_size) {
    return d3.scale.linear()
        .domain([0, window_size * 60])
        .range([5, 15]);
}

function buildXScale(w) {
    return d3.scale.linear()
        .domain([-30, -100])
        .range([0 + 50, w - 50]);
}

function buildYScale(h, start, window_size) {
    return d3.scale.linear()
        .domain([start, start + (60 * window_size)])
        .range([h - 50, 0 + 50]);
}

function buildHourRadiusScale() {
    // ping count
    var MAX_PING_PER_HOUR = 12;
    var MIN_RADIUS = 5;
    var MAX_RADIUS = 15;
    return d3.scale.linear()
        .domain([1, MAX_PING_PER_HOUR])
        .range([MIN_RADIUS, MAX_RADIUS]);
}

function buildHourColorScale() {
    // signal strength
    return d3.scale.linear()
        .domain([-30, -100])
        .range(["#3E932A", "white"]);
}

function buildHourXScale(w, start_time) {
    // x coordinate
    return d3.scale.linear()
        .domain([start_time, start_time + 3600])
        .range([0 + 50, w - 50]);
}
