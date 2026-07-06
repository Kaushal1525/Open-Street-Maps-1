#!/usr/bin/env python3
"""
osrm1.py

Interactive OSRM router:
  - Click on the map: 1st click sets Start, 2nd click sets End and triggers routes.
  - Shows Driving, Cycling, Walking routes (OSRM) with durations.
  - Shows a Railway straight-line estimate (configurable speed).
  - Can be launched with coordinates to auto-route:
      python osrm1.py start_lat start_lon end_lat end_lon [--open]

Writes: osrm1_map.html
"""
import sys
import webbrowser
import os
from math import radians, sin, cos, sqrt, atan2

OUT_HTML = "osrm1_map.html"
DEFAULT_TRAIN_SPEED_KMPH = 80.0


HTML_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>OSRM Multi-Profile Router (Interactive)</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<style>
  html, body, #map { height: 100%; margin: 0; padding: 0; }
  .info-box { position: absolute; top: 10px; right: 10px; z-index: 1000; background: white; padding: 10px; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.3); font-family: Arial, sans-serif; font-size: 13px; max-width:340px; }
  .route-label { margin-bottom:6px; }
</style>
</head>
<body>
<div id="map"></div>
<div class="info-box" id="info">
  <div><strong>Instructions</strong>: Click map to set <em>Start</em> (1st click) and <em>End</em> (2nd click). Driving, Cycling, Walking routes will be requested automatically. Railway shows an estimated time (straight-line).</div>
  <hr/>
  <div id="routes-summary"></div>
  <div style="margin-top:8px"><button id="clearBtn">Clear</button></div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
// OSRM public endpoint
const OSRM_BASE = "https://router.project-osrm.org/route/v1";

let map = L.map('map').setView([<<MID_LAT>>, <<MID_LON>>], <<ZOOM>>);
let osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let startMarker = null, endMarker = null;
let clickCount = 0;
let layerGroup = L.layerGroup().addTo(map);

const profiles = [
  { id: "driving", name: "Driving (car)", profile: "driving" },
  { id: "cycling", name: "Cycling (bike)", profile: "cycling" },
  { id: "walking", name: "Walking (foot)", profile: "walking" }
];

function clearAll() {
  layerGroup.clearLayers();
  if (startMarker) { map.removeLayer(startMarker); startMarker = null; }
  if (endMarker) { map.removeLayer(endMarker); endMarker = null; }
  clickCount = 0;
  document.getElementById("routes-summary").innerHTML = "";
}
document.getElementById("clearBtn").addEventListener("click", clearAll);

function formatTimeSeconds(sec) {
  sec = Math.round(sec);
  if (sec < 60) return sec + " s";
  let min = Math.floor(sec/60);
  if (min < 60) return min + " min";
  let hr = Math.floor(min/60);
  min = min % 60;
  return hr + " h " + min + " min";
}

// compute haversine distance (km)
function haversineKm(lat1, lon1, lat2, lon2) {
  const R = 6371.0;
  const φ1 = lat1 * Math.PI/180.0;
  const φ2 = lat2 * Math.PI/180.0;
  const Δφ = (lat2-lat1)*Math.PI/180.0;
  const Δλ = (lon2-lon1)*Math.PI/180.0;
  const a = Math.sin(Δφ/2)*Math.sin(Δφ/2) + Math.cos(φ1)*Math.cos(φ2)*Math.sin(Δλ/2)*Math.sin(Δλ/2);
  const c = 2*Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

async function requestOSRM(profile, sLat, sLon, eLat, eLon) {
  const url = `${OSRM_BASE}/${profile}/${sLon},${sLat};${eLon},${eLat}?overview=full&geometries=geojson&annotations=duration,distance`;
  const resp = await fetch(url);
  if (!resp.ok) {
    const txt = await resp.text();
    throw new Error(`OSRM ${profile} failed: ${resp.status} ${txt}`);
  }
  return resp.json();
}

async function routeAll(sLat, sLon, eLat, eLon) {
  layerGroup.clearLayers();
  // markers
  startMarker = L.marker([sLat,sLon], {title:"Start"}).addTo(layerGroup);
  endMarker = L.marker([eLat,eLon], {title:"End"}).addTo(layerGroup);

  const summaryDiv = document.getElementById("routes-summary");
  summaryDiv.innerHTML = "<strong>Calculating...</strong>";

  const results = [];
  for (let p of profiles) {
    try {
      const js = await requestOSRM(p.profile, sLat, sLon, eLat, eLon);
      if(!js.routes || js.routes.length==0) throw new Error("no route");
      const route = js.routes[0];
      const coords = route.geometry.coordinates.map(c => [c[1], c[0]]);
      const color = (p.id==="driving")? "#1f78b4" : (p.id==="cycling")? "#33a02c" : "#b15928";
      const poly = L.polyline(coords, {color: color, weight:6, opacity:0.8}).addTo(layerGroup);
      poly.bindPopup(`<strong>${p.name}</strong><br/>Distance: ${(route.distance/1000).toFixed(2)} km<br/>Time: ${formatTimeSeconds(route.duration)}`);
      results.push({ name: p.name, distance_km: route.distance/1000.0, duration_s: route.duration });
    } catch (e) {
      results.push({ name: p.name, error: e.message });
    }
  }

  // Railway estimate (straight-line)
  const km = haversineKm(sLat, sLon, eLat, eLon);
  const trainSpeed = <<TRAIN_SPEED>>; // km/h
  const trainSeconds = (km / trainSpeed) * 3600;
  // dashed line for railway
  const railLine = L.polyline([[sLat,sLon],[eLat,eLon]], {color:'#6a3d9a', weight:4, dashArray:'10,6', opacity:0.9}).addTo(layerGroup);
  railLine.bindPopup(`<strong>Railway (estimate)</strong><br/>Distance: ${km.toFixed(2)} km<br/>Estimated travel time (@ ${trainSpeed} km/h): ${formatTimeSeconds(trainSeconds)}<br/><small>Note: this is a straight-line estimate; for actual rail routes use GTFS or a rail network.</small>`);

  // build summary HTML
  let html = "<div>";
  for (let r of results) {
    if (r.error) {
      html += `<div class="route-label"><strong>${r.name}</strong>: <span style="color:red">error: ${r.error}</span></div>`;
    } else {
      html += `<div class="route-label"><strong>${r.name}</strong>: ${r.distance_km.toFixed(2)} km — ${formatTimeSeconds(r.duration_s)}</div>`;
    }
  }
  html += `<div class="route-label"><strong>Railway estimate</strong>: ${km.toFixed(2)} km — ${formatTimeSeconds(trainSeconds)}</div>`;
  html += "</div>";
  summaryDiv.innerHTML = html;

  // fit map bounds
  const allLayers = layerGroup.getLayers();
  if (allLayers.length>0) {
    const bounds = layerGroup.getBounds();
    if (bounds.isValid()) map.fitBounds(bounds.pad(0.15));
  }
}

map.on('click', function(e) {
  clickCount++;
  if (clickCount === 1) {
    if (startMarker) map.removeLayer(startMarker);
    startMarker = L.marker(e.latlng, {title:"Start"}).addTo(layerGroup);
    document.getElementById("routes-summary").innerHTML = "<em>Start set — click to set End</em>";
  } else {
    if (endMarker) map.removeLayer(endMarker);
    endMarker = L.marker(e.latlng, {title:"End"}).addTo(layerGroup);
    // get coords and route
    const s = startMarker.getLatLng();
    const t = endMarker.getLatLng();
    routeAll(s.lat, s.lng, t.lat, t.lng);
    clickCount = 0; // reset for next pair of clicks
  }
});

// If initial points were provided, auto-route:
<<INITIAL_ROUTE_JS>>

</script>
</body>
</html>
"""

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    φ1, φ2 = radians(lat1), radians(lat2)
    dφ = radians(lat2 - lat1)
    dλ = radians(lon2 - lon1)
    a = sin(dφ/2)**2 + cos(φ1)*cos(φ2)*sin(dλ/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def build_html(mid_lat, mid_lon, zoom, start=None, end=None, train_speed=DEFAULT_TRAIN_SPEED_KMPH):
    if start and end:
        initial_route_js = f"""
// pre-populate and route automatically
startMarker = L.marker([{start[0]}, {start[1]}]).addTo(layerGroup);
endMarker = L.marker([{end[0]}, {end[1]}]).addTo(layerGroup);
routeAll({start[0]}, {start[1]}, {end[0]}, {end[1]});
"""
    else:
        initial_route_js = ""

    html = HTML_TEMPLATE.replace("<<MID_LAT>>", str(mid_lat)) \
                        .replace("<<MID_LON>>", str(mid_lon)) \
                        .replace("<<ZOOM>>", str(zoom)) \
                        .replace("<<TRAIN_SPEED>>", str(train_speed)) \
                        .replace("<<INITIAL_ROUTE_JS>>", initial_route_js)
    return html

def main():
    args = sys.argv[1:]
    start = None
    end = None
    do_open = False

    if "--open" in args:
        do_open = True
        args = [a for a in args if a != "--open"]

    if len(args) == 4:
        try:
            s_lat = float(args[0]); s_lon = float(args[1])
            e_lat = float(args[2]); e_lon = float(args[3])
            start = (s_lat, s_lon)
            end = (e_lat, e_lon)
        except ValueError:
            print("Invalid coordinates. Expected: start_lat start_lon end_lat end_lon")
            return
    elif len(args) != 0:
        print("Usage: python osrm1.py [--open]  OR  python osrm1.py start_lat start_lon end_lat end_lon [--open]")
        return


    if start and end:
        mid_lat = (start[0] + end[0]) / 2.0
        mid_lon = (start[1] + end[1]) / 2.0
        zoom = 7 if haversine_km(start[0], start[1], end[0], end[1]) > 200 else 13
    else:

        mid_lat = 16.441173
        mid_lon = 80.621980
        zoom = 16

    html = build_html(mid_lat, mid_lon, zoom, start=start, end=end, train_speed=DEFAULT_TRAIN_SPEED_KMPH)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {OUT_HTML}")

    if do_open:
        webbrowser.open("file://" + os.path.abspath(OUT_HTML))

if __name__ == "__main__":
    main()
