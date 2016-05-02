var window_size = 10;
var interval = 5000;
var w, h, svg;
var scaleFactory, legend, userDataCache;
var scales = {};
var active = null;
var legend;
var devices = {};
//var base_url = "http://127.0.0.1:8005";
var base_url = "https://explore.meyersj.com:8005";
var query_endpoint = base_url + "/query";
var summary_endpoint = base_url + "/user/summary";
var polling = null;
var downloading = false;
var resize_timeout = null;

$(document).ready(function() {
    initialize();
});

$(window).resize(function(e) {
    clearTimeout(resize_timeout);
    resize_timeout = setTimeout(function() { initialize(); }, 1000);
});

function compute_svg_size() {
    var windowHeight = window.innerHeight;
    var padding = $('.content-container').css('padding-top');
    padding = parseInt(padding.substring(0, padding.length - 2), 10) * 2;
    var height = (windowHeight - padding) * 0.95;
    var width = $("#visual").outerWidth();
    return [height, width];
}

function initialize() {
    clearInterval(polling);
    // set up size of svg visualization
    var size = compute_svg_size();
    h = size[0];
    w = size[1];
    svg = canvas("#visual");
    scaleFactory = new ScaleFactory(w, h, window_size);
    legend = initLegend(svg, scaleFactory); 
    userDataCache = new DataCache();
    buildScales(scaleFactory);
    update();
}

function canvas(div) {
    if(svg) svg.remove();
    return d3.select(div)
        .append("svg")
        .attr("height", h)
        .attr("width", w);
}

function buildScales(factory) {
    scales.duration = factory.windowDuration();
    scales.scaleX = factory.windowSignal();
    scales.hourColor = factory.hourSignal();
    scales.hourRadius = factory.hourPingRate();
}

function mouseoverNode(d) {
    if (active === d.Mac) {
        // device already active, do nothing
        return;
    }
    clear_device_summary();
    toggleUserSummary(d);
    active = d.Mac;
}

function mouseoutNode(d) {
    active = null;
}

function clear_device_summary() {
    var nodes = svg.selectAll(".summary-node");
    nodes.selectAll(".summary-node").selectAll("*").remove();
    nodes.remove();
}

function device_type(d) {
    if (!d.AP && !d.Device) {
        return "wifi-unknown";
    }
    else if (d.AP && !d.Device) {
        return "wifi-access-point";
    }
    else if (!d.AP && d.Device) {
        return "wifi-device";
    }
    else if (d.AP && d.Device) {
        return "wifi-hybrid";
    }
    return "wifi-error";
}

function initLegend(svg, scaleFactory) {
    var legend = new Legend(svg, scaleFactory);
    legend.drawUserSummaryLegend();
    legend.drawDeviceLegend(window_size);
    return legend
}

function drawUserSummary(mac, data) {
    drawHourSummary(mac, data);
    drawDailySummary(mac, data);
}

function drawHourSummary(mac, data) {
    var xScale = scaleFactory.hourTime(data.HourStart)
    var nodes = svg.selectAll(".hour-data-point")
        .data(data.HourData)
        .enter()
        .append("g")
        .attr("class", "hour-data-point summary-node")
        .attr("mac", function(d) {
            return d.Mac     
        })
        .append("circle")
        .attr("class", function(d) {
            var device_data = devices[d.Mac];
            return "wifi-node " + device_type(device_data);
        })
        .attr('r', 6)
        .attr('cx', function(d) {
            return xScale(d.Bucket);
        })
        .attr('cy', function(d) {
            return h - 60;
        });
}

function drawDailySummary(mac, data) {
    var xScale = scaleFactory.dailyTime(data.DailyStart)
    var nodes = svg.selectAll(".daily-data-point")
        .data(data.DailyData)
        .enter()
        .append("g")
        .attr("class", "daily-data-point summary-node")
        .attr("mac", function(d) {
            return d.Mac     
        })
        .append("circle")
        .attr('class', function(d) {
            var device_data = devices[d.Mac];
            return "wifi-node " + device_type(device_data); 
        })
        .attr('r', 6)
        .attr('cx', function(d) {
            return xScale(d.Hour);
        })
        .attr('cy', function(d) {
            return h - 30;
        });
}

function toggleUserSummary(d) {
    var cache = userDataCache.get(d.Mac);
    if (cache == null) {
        // download and update cache
        $.getJSON(summary_endpoint, {mac:d.Mac}, function(data) {
            //console.log(data);
            userDataCache.put(d.Mac, data, 360);
            drawUserSummary(d.Mac, data)
        });
    }
    else {
        // use cached data
        drawUserSummary(d.Mac, cache)
    }
}

function update() {
    $.getJSON(query_endpoint, {"window":window_size}, function(data) {
        if (h >= 500) {
            legend.drawTime(h, data.Start, window_size);    
        }
        if (w >= 500) {
            legend.drawSignalStrength(w);
        }
        scales.age = scaleFactory.windowAge(data.Start);
        scales.scaleY = scaleFactory.windowTime(data.Start);
        var dataset = merge(devices, data.Start, data.Data);
        visualize(dataset);
        if (!polling) {
            polling = setInterval(function() { update(); }, interval);
        }
    });
}

function merge(devices, start, data) {
    var dataset = []
    $.each(data, function(i, d) {
        devices[d.Mac] = d;
    });
    for (var key in devices) {
        // expire old devices
        if (devices[key].LastArrival < start) {
            delete devices[key];
        }
        else {
            dataset.push(devices[key]);
        }
    }
    dataset.sort(function(a, b) {
        return a.LastArrival - b.LastArrival;
    });
    return dataset; 
}

function visualize(data) {
    var nodes = svg.selectAll(".node")
        .data(data, function(d) {
            return d.Mac;        
        });
    
    var group = nodes.enter()
        .append("g")
        .attr("class", "node")
        .attr("mac", function(d) {
            return d.Mac;
        });
        
    group.append("circle")
        .attr('opacity', function(d) { 
            return scales.age(d.LastArrival);
        })
        .attr("class", function(d) {
            return "wifi-node recent-node " + device_type(d);
        })
        .attr("signal", function(d) {
            return d.AvgSignal;
        })
        .on("mouseover", mouseoverNode)
        .on("mouseout", mouseoutNode);

    group.append("text")
        .attr("class", "mac-label")
        .text(function(d) {
            return d.Mac;
        });

    group.append("text")
        .attr("class", "manuf-label")
        .text(function(d) {
            return d.Manuf;
        });

    nodes.select("circle").transition().duration(interval)
        .attr('opacity', function(d) { 
            return scales.age(d.LastArrival);
        })
        .attr('r', function(d) {
            return scales.duration(d.LastArrival - d.FirstArrival);
        })
        .attr('cx', function(d) {
            return scales.scaleX(d.AvgSignal);
        })
        .attr('cy', function(d) {
            return scales.scaleY(d.LastArrival);
        });

    nodes.select(".mac-label").transition().duration(interval)
        .attr('x', function(d) {
             return scales.scaleX(d.AvgSignal);
        })
        .attr('y', function(d) {
            return scales.scaleY(d.LastArrival) + 50;
        });

    nodes.select(".manuf-label").transition().duration(interval)
        .attr('x', function(d) {
             return scales.scaleX(d.AvgSignal);
        })
        .attr('y', function(d) {
            return scales.scaleY(d.LastArrival) + 65;
        });
    
    nodes.exit().remove();
}
