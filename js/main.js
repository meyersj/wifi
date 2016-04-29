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


$(document).ready(function() {
    initialize();
});

$(window).resize(function(e) {
    initialize();
});

function initialize() {
    clearInterval(polling);
    // set up size of svg visualization
    var windowHeight = window.innerHeight;
    var padding = $('.content-container').css('padding-top');
    padding = parseInt(padding.substring(0, padding.length - 2), 10) * 2;
    h = (windowHeight - padding) * 0.95;
    w = $("#visual").outerWidth();
    svg = canvas("#visual");
    scaleFactory = new ScaleFactory(w, h, window_size);
    legend = initLegend(svg, scaleFactory); 
    userDataCache = new DataCache();
    buildScales(scaleFactory);
    update();
    polling = setInterval(function() { update(); }, interval);
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
    console.log("ACTIVE: " + active + " DATA: " + d.Mac)
    if (active === d.Mac) {
        console.log("already");
        return;
    }
    clear_hour_circles();
    toggleUserSummary(d);
    active = d.Mac;
}

function mouseoutNode(d) {
    active = null;
}

function clear_hour_circles() {
    var nodes = svg.selectAll(".hour-data-point");
    nodes.selectAll(".hour-data-point").selectAll("*").remove();
    nodes.remove();
    nodes = svg.selectAll(".daily-data-point");
    nodes.selectAll(".daily-data-point").selectAll("*").remove();
    nodes.remove();
}

function initLegend(svg, scaleFactory) {
    var legend = new Legend(svg, scaleFactory);
    legend.drawUserSummaryLegend();
    legend.drawDeviceLegend();
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
        .attr("class", "hour-data-point")
        .attr("mac", function(d) {
            return d.Mac     
        })
        .append("circle")
        .attr('fill', function(d) {
            return scales.hourColor(d.AvgSignal);         
        })
        .attr('r', function(d) {
            return scales.hourRadius(d.PingCount);
        })
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
        .attr("class", "daily-data-point")
        .attr("mac", function(d) {
            return d.Mac     
        })
        .append("circle")
        .attr('fill', function(d) {
            return scales.hourColor(d.AvgSignal);         
        })
        .attr('r', function(d) {
            return scales.hourRadius(d.Bucket5Count);
        })
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
        legend.drawSignalStrength(w);
        legend.drawTime(h, data.Start, window_size);    
        scales.age = scaleFactory.windowAge(data.Start);
        scales.scaleY = scaleFactory.windowTime(data.Start);
        var dataset = merge(devices, data.Start, data.Data);
        visualize(dataset);
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
        })
        .on("mouseover", mouseoverNode)
        .on("mouseout", mouseoutNode);


    function class_builder(d) {
        var cls = "recent-node";
        if (!d.AP && !d.Device) {
            return cls + " wifi-unknown";
        }
        else if (d.AP && !d.Device) {
            return cls + " wifi-access-point";
        }
        else if (!d.AP && d.Device) {
            return cls + " wifi-device";
        }
        else if (d.AP && d.Device) {
            return cls + " wifi-hybrid";
        }
        return cls + " wifi-error";
    }


    group.append("circle")
        .attr('opacity', function(d) { 
            return scales.age(d.LastArrival);
        })
        .attr("class", "recent-node")
        .attr("class", function(d) {
            return class_builder(d);
        })
        .attr("signal", function(d) {
            console.log(d);
            return d.AvgSignal;
        });
    
    /*
    group.append("text")
    
    nodes.select("text").transition().duration(interval)
        .attr('x', function(d) {
            var r = scales.duration(d.LastArrival - d.FirstArrival);
            return 0;
        })
        .attr('y', function(d) {
            return 20;
        })
        .text(function(d) { return "Device: " + d.Mac; });
    */

    nodes.select("circle").transition().duration(interval)
        .attr('opacity', function(d) { 
            return scales.age(d.LastArrival);
        })
        //.attr('fill', function(d) {
        //    return scales.age(d.LastArrival);
        //})
        .attr('r', function(d) {
            return scales.duration(d.LastArrival - d.FirstArrival);
        })
        .attr('cx', function(d) {
            return scales.scaleX(d.AvgSignal);
        })
        .attr('cy', function(d) {
            return scales.scaleY(d.LastArrival);
        });
    
    nodes.exit().remove();
}
