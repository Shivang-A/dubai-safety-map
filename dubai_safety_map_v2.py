import json
from datetime import datetime, timezone

# Dubai Safety Map Generator v2
# Generates an interactive HTML map with configurable risk radii.

LOCATIONS = [
    {
        "name": "Al Dhafra Air Base",
        "type": "US Air Force Base — Abu Dhabi",
        "lat": 24.248,
        "lng": 54.591,
        "color": "#cc0000",
        "status": "CONFIRMED IRANIAN MISSILE TARGET",
        "note": (
            "Directly targeted by Iranian ballistic missiles. "
            "Hosts US F-35s, AWACS, and tanker aircraft. "
            "Primary US air power hub in the Gulf."
        ),
        "risk": "critical",
    },
    {
        "name": "Al Minhad Air Base",
        "type": "Coalition Air Base — South Dubai",
        "lat": 25.026,
        "lng": 55.366,
        "color": "#cc0000",
        "status": "HIGH RISK — US COALITION PRESENCE",
        "note": (
            "Hosts US and allied coalition forces south of Dubai. "
            "Likely on Iranian secondary target list. "
            "Shares corridor with Dubai International Airport."
        ),
        "risk": "critical",
    },
    {
        "name": "Jebel Ali Port",
        "type": "Strategic Port / US Navy Docking",
        "lat": 24.993,
        "lng": 55.058,
        "color": "#e06000",
        "status": "ELEVATED RISK — US NAVAL USE",
        "note": (
            "World's largest man-made harbour. Regularly used by US Navy. "
            "Strategic dual-use civilian/military target. "
            "~12km from Palm Jumeirah drone strike — likely causal link."
        ),
        "risk": "high",
    },
    {
        "name": "Palm Jumeirah — Drone Strike",
        "type": "Confirmed Drone Incident",
        "lat": 25.113,
        "lng": 55.138,
        "color": "#cc8800",
        "status": "CONFIRMED DRONE INCIDENT — 4 INJURED",
        "note": (
            "Iranian drone struck hotel/building. Fire reported. "
            "Proximity to Jebel Ali Port suggests drift or intentional near-miss. "
            "Dense residential/tourist area."
        ),
        "risk": "incident",
    },
]

INNER_RADIUS_KM = 5
OUTER_RADIUS_KM = 12
AWARE_RADIUS_KM = 22

TIMESTAMP = datetime.now(timezone.utc).strftime("%d %b %Y  %H:%M UTC")
CONTACT_URL = "https://www.linkedin.com/in/shivangagarwal22/"


def generate_html(output_path="index.html"):
    locations_json = json.dumps(LOCATIONS, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dubai Safety Map — {TIMESTAMP}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Barlow+Condensed:wght@400;600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  :root {{
    --bg:      #f0ece4;
    --panel:   #f7f4ef;
    --border:  #d8d0c4;
    --red:     #cc0000;
    --orange:  #e06000;
    --yellow:  #cc8800;
    --text:    #1a1a1a;
    --dim:     #7a6a5a;
    --mono:    'Share Tech Mono', monospace;
    --ui:      'Barlow Condensed', sans-serif;
    --shadow:  0 2px 12px rgba(0,0,0,0.15);
  }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: var(--ui);
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}

  header {{
    background: #1a1008;
    border-bottom: 3px solid var(--red);
    padding: 12px 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
    box-shadow: var(--shadow);
  }}
  .title {{
    font-weight: 900; font-size: 22px;
    letter-spacing: 4px; text-transform: uppercase;
    color: #ff3333;
  }}
  .subtitle {{
    font-family: var(--mono); font-size: 11px;
    color: #a09080; margin-top: 2px; letter-spacing: 1px;
  }}
  .pills {{ display:flex; gap:10px; align-items:center; }}
  .pill {{
    font-family: var(--mono); font-size: 11px;
    padding: 4px 12px; border-radius: 2px;
    border: 1px solid currentColor;
    animation: blink 1.4s infinite;
    letter-spacing: 1px;
  }}
  .pill.red   {{ color:#ff4444; background:rgba(204,0,0,.15); }}
  .pill.amber {{ color:#ffaa00; background:rgba(224,96,0,.12); animation-duration:.9s; }}
  @keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:.3}} }}

  .main {{ display:flex; flex:1; overflow:hidden; }}
  #map  {{ flex:1; }}

  .sidebar {{
    width: 360px;
    background: var(--panel);
    border-left: 2px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    flex-shrink: 0;
    box-shadow: -4px 0 20px rgba(0,0,0,0.08);
  }}
  .sec {{
    border-bottom: 1px solid var(--border);
    padding: 16px 18px;
  }}
  .sec-lbl {{
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 2.5px;
    color: var(--dim);
    text-transform: uppercase;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .sec-lbl::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }}

  .zone {{
    display: flex; gap: 10px; align-items: flex-start;
    margin-bottom: 12px; cursor: pointer;
    padding: 10px 10px;
    border: 1px solid transparent;
    border-radius: 4px;
    transition: .2s;
    background: rgba(0,0,0,.02);
  }}
  .zone:hover {{
    border-color: var(--border);
    background: rgba(0,0,0,.05);
    transform: translateX(2px);
  }}
  .dot {{
    width: 12px; height: 12px;
    border-radius: 50%; margin-top: 4px; flex-shrink: 0;
  }}
  .zname  {{ font-size: 16px; font-weight: 800; color: #111; margin-bottom: 2px; letter-spacing:.3px; }}
  .ztype  {{ font-family: var(--mono); font-size: 10px; color: var(--dim); margin-bottom: 4px; letter-spacing:.5px; }}
  .zstatus {{ font-size: 13px; font-weight: 700; }}
  .rc {{ color: var(--red); }}
  .ro {{ color: var(--orange); }}
  .ry {{ color: var(--yellow); }}

  .slider-row {{
    display: flex; justify-content: space-between;
    margin-bottom: 6px; font-size: 14px; font-weight: 700;
    color: #2a1a0a;
  }}
  .sval {{
    font-family: var(--mono); font-size: 14px;
    color: var(--red); min-width: 55px; text-align: right;
  }}
  input[type=range] {{
    -webkit-appearance: none; width: 100%; height: 4px;
    background: var(--border); border-radius: 2px;
    outline: none; cursor: pointer; margin-bottom: 14px;
  }}
  input[type=range]::-webkit-slider-thumb {{
    -webkit-appearance: none; width: 16px; height: 16px;
    border-radius: 50%; background: var(--red);
    box-shadow: 0 0 5px rgba(204,0,0,.4); cursor: pointer;
  }}

  .legend {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:6px; }}
  .litem  {{ display:flex; align-items:center; gap:5px;
             font-size: 12px; font-family: var(--mono); color: var(--dim); }}
  .ldot   {{ width:10px; height:10px; border-radius:50%; flex-shrink:0; }}

  .adv {{
    display: flex; gap: 10px; margin-bottom: 9px;
    font-size: 13px; line-height: 1.55; color: #2a1a0a;
    padding: 9px 10px;
    background: rgba(204,0,0,.04);
    border-left: 3px solid var(--orange);
    border-radius: 0 4px 4px 0;
  }}
  .adv.crit {{ border-left-color: var(--red); background: rgba(204,0,0,.07); }}
  .adv.info {{ border-left-color: #2266aa; background: rgba(34,102,170,.05); }}
  .adv-icon {{ font-size: 16px; flex-shrink:0; margin-top:1px; }}

  .ts {{
    font-family: var(--mono); font-size: 10px;
    color: var(--dim); padding: 10px 16px; text-align: center;
    border-top: 1px solid var(--border); margin-top: auto;
    display: flex; align-items: center; justify-content: center; gap: 8px;
    flex-wrap: wrap;
  }}
  .ts .sep {{ opacity: .35; }}
  .contact-link {{
    color: var(--dim);
    text-decoration: none;
    opacity: .72;
    border-bottom: 1px dotted transparent;
    transition: opacity .2s ease, border-color .2s ease, color .2s ease;
  }}
  .contact-link:hover {{
    opacity: 1;
    color: #4a3a2a;
    border-bottom-color: #8a7a6a;
  }}

  .leaflet-control-zoom a {{
    background: var(--panel) !important;
    color: #333 !important;
    border-color: var(--border) !important;
  }}
  .leaflet-control-attribution {{ font-size:9px; opacity:.5; }}
  .cpop .leaflet-popup-content-wrapper {{
    background: #fffdf8; border: 1px solid #d8d0c4;
    border-radius: 5px; color: #1a1a1a;
    font-family: 'Barlow Condensed', sans-serif;
    box-shadow: 0 6px 24px rgba(0,0,0,.18);
  }}
  .cpop .leaflet-popup-tip {{ background: #fffdf8; }}
  .ptitle {{ font-weight:800; font-size:15px; margin-bottom:3px; }}
  .ptype  {{ font-family:'Share Tech Mono',monospace; font-size:10px; color:#7a6a5a; margin-bottom:5px; }}
  .pnote  {{ font-size:12px; color:#5a4a3a; margin-top:4px; line-height:1.45; }}

  @media (max-width: 900px) {{
    .main {{ flex-direction: column; }}
    #map {{ min-height: 55vh; }}
    .sidebar {{ width: 100%; border-left: 0; border-top: 2px solid var(--border); }}
    header {{ flex-direction: column; align-items: flex-start; gap: 8px; }}
  }}
</style>
</head>
<body>

<header>
  <div>
    <div class="title">Dubai Safety Map</div>
    <div class="subtitle">CIVILIAN SAFETY ADVISORY · {TIMESTAMP}</div>
  </div>
  <div class="pills">
    <div class="pill red">CONFLICT ACTIVE</div>
    <div class="pill amber">AIRSPACE CLOSED</div>
  </div>
</header>

<div class="main">
  <div id="map"></div>

  <div class="sidebar">
    <div class="sec">
      <div class="sec-lbl">Risk Zones</div>
      <div id="zone-list"></div>
    </div>

    <div class="sec">
      <div class="sec-lbl">Avoidance Radius Control</div>
      <div class="slider-row">
        <span>Inner Exclusion</span>
        <span class="sval" id="r1v">{INNER_RADIUS_KM} km</span>
      </div>
      <input type="range" id="r1" min="1" max="25" value="{INNER_RADIUS_KM}" step="0.5" oninput="updateR(1)">

      <div class="slider-row">
        <span>Caution Zone</span>
        <span class="sval" id="r2v">{OUTER_RADIUS_KM} km</span>
      </div>
      <input type="range" id="r2" min="2" max="40" value="{OUTER_RADIUS_KM}" step="0.5" oninput="updateR(2)">

      <div class="slider-row">
        <span>Awareness Zone</span>
        <span class="sval" id="r3v">{AWARE_RADIUS_KM} km</span>
      </div>
      <input type="range" id="r3" min="5" max="60" value="{AWARE_RADIUS_KM}" step="1" oninput="updateR(3)">

      <div class="legend">
        <div class="litem"><div class="ldot" style="background:#cc0000"></div> Exclusion</div>
        <div class="litem"><div class="ldot" style="background:#e06000"></div> Caution</div>
        <div class="litem"><div class="ldot" style="background:#cc8800"></div> Awareness</div>
      </div>
    </div>

    <div class="sec">
      <div class="sec-lbl">Civilian Advisory</div>
      <div class="adv crit"><div class="adv-icon">!</div><div>Stay &gt;10km from all military bases and Jebel Ali Port. Interception debris is lethal.</div></div>
      <div class="adv"><div class="adv-icon">^</div><div>UAE airspace closed. Do not travel to airports without official confirmation.</div></div>
      <div class="adv"><div class="adv-icon">#</div><div>Shelter in concrete buildings. Avoid glass facades and high floors during alerts.</div></div>
      <div class="adv"><div class="adv-icon">*</div><div>Monitor UAE WAM News Agency and Dubai Media Office for real-time interception alerts.</div></div>
      <div class="adv info"><div class="adv-icon">i</div><div>Civilian risk can come from debris, misfires, and proximity to ports and bases.</div></div>
    </div>

    <div class="ts">
      <span>{TIMESTAMP}</span>
      <span class="sep">|</span>
      <a class="contact-link" href="{CONTACT_URL}" target="_blank" rel="noopener noreferrer">updates: Shivang (LinkedIn)</a>
    </div>
  </div>
</div>

<script>
const LOCS = {locations_json};
const map = L.map('map', {{ zoomControl: true }}).setView([25.05, 55.15], 10);

L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
  subdomains: 'abcd',
  maxZoom: 19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> &copy; <a href="https://carto.com/">CartoDB</a>'
}}).addTo(map);

const circles1 = {{}}, circles2 = {{}}, circles3 = {{}};
let r1 = {INNER_RADIUS_KM} * 1000;
let r2 = {OUTER_RADIUS_KM} * 1000;
let r3 = {AWARE_RADIUS_KM} * 1000;

function mkIcon(color) {{
  return L.divIcon({{
    className: '',
    html: `<div style="width:14px;height:14px;background:${{color}};border-radius:50%;border:2px solid white;box-shadow:0 0 8px ${{color}}, 0 2px 4px rgba(0,0,0,.4);"></div>`,
    iconSize: [14,14],
    iconAnchor: [7,7]
  }});
}}

const zoneList = document.getElementById('zone-list');
LOCS.forEach(loc => {{
  const cls = loc.risk === 'critical' ? 'rc' : loc.risk === 'high' ? 'ro' : 'ry';
  zoneList.innerHTML += `
    <div class="zone" onclick="flyTo(${{loc.lat}},${{loc.lng}})">
      <div class="dot" style="background:${{loc.color}};box-shadow:0 0 5px ${{loc.color}}80"></div>
      <div>
        <div class="zname">${{loc.name}}</div>
        <div class="ztype">${{loc.type}}</div>
        <div class="zstatus ${{cls}}">${{loc.status}}</div>
      </div>
    </div>`;
}});

LOCS.forEach(loc => {{
  L.marker([loc.lat, loc.lng], {{ icon: mkIcon(loc.color) }})
    .addTo(map)
    .bindPopup(`
      <div class="ptitle">${{loc.name}}</div>
      <div class="ptype">${{loc.type}}</div>
      <div class="zstatus ${{loc.risk==='critical' ? 'rc' : loc.risk==='high' ? 'ro' : 'ry'}}" style="font-size:13px">${{loc.status}}</div>
      <div class="pnote">${{loc.note}}</div>
    `, {{ className: 'cpop', maxWidth: 270 }});

  circles1[loc.name] = L.circle([loc.lat, loc.lng], {{
    radius: r1, color: loc.color, fillColor: loc.color, fillOpacity: .12, weight: 2, dashArray: '5 4'
  }}).addTo(map);

  circles2[loc.name] = L.circle([loc.lat, loc.lng], {{
    radius: r2, color: loc.color, fillColor: loc.color, fillOpacity: .05, weight: 1.2, dashArray: '9 6'
  }}).addTo(map);

  circles3[loc.name] = L.circle([loc.lat, loc.lng], {{
    radius: r3, color: loc.color, fillColor: loc.color, fillOpacity: .02, weight: .8, dashArray: '14 8'
  }}).addTo(map);
}});

function updateR(which) {{
  const v = parseFloat(document.getElementById('r' + which).value);
  document.getElementById('r' + which + 'v').textContent = v.toFixed(1) + ' km';
  const m = v * 1000;
  if (which === 1) {{ r1 = m; LOCS.forEach(l => circles1[l.name].setRadius(m)); }}
  if (which === 2) {{ r2 = m; LOCS.forEach(l => circles2[l.name].setRadius(m)); }}
  if (which === 3) {{ r3 = m; LOCS.forEach(l => circles3[l.name].setRadius(m)); }}
}}
window.updateR = updateR;

function flyTo(lat, lng) {{ map.flyTo([lat, lng], 12, {{ duration: 1.2 }}); }}
window.flyTo = flyTo;
</script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[ok] HTML map saved -> {output_path}")
    return output_path


if __name__ == "__main__":
    generate_html("index.html")
    print("Done. Open index.html in a browser.")
