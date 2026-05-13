"""
IP Geolocation Lookup
A Flask web app that works on PC and mobile.
Run: python ip-geolocation-lookup.py
Then open: http://localhost:5000
"""

from flask import Flask, render_template_string, request, jsonify
import requests
import re

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>IP Geolocation Lookup</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:        #0d1117;
      --surface:   #161b22;
      --surface2:  #1c2128;
      --border:    #30363d;
      --accent:    #58a6ff;
      --accent2:   #3d8bfd;
      --text:      #e6edf3;
      --muted:     #8b949e;
      --success:   #3fb950;
      --error:     #f85149;
      --radius:    14px;
    }

    body {
      font-family: 'Inter', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 2rem 1rem 4rem;
    }

    /* ── Header ── */
    header {
      text-align: center;
      margin-bottom: 2.5rem;
    }
    header .icon {
      font-size: 3rem;
      line-height: 1;
      margin-bottom: .6rem;
    }
    header h1 {
      font-size: clamp(1.5rem, 5vw, 2.2rem);
      font-weight: 700;
      background: linear-gradient(135deg, #58a6ff, #a371f7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    header p {
      color: var(--muted);
      font-size: .9rem;
      margin-top: .4rem;
    }

    /* ── Card ── */
    .card {
      width: 100%;
      max-width: 560px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.8rem;
    }

    /* ── Search bar ── */
    .search-row {
      display: flex;
      gap: .6rem;
    }
    .search-row input {
      flex: 1;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 10px;
      color: var(--text);
      font-family: inherit;
      font-size: 1rem;
      padding: .75rem 1rem;
      outline: none;
      transition: border-color .2s;
    }
    .search-row input:focus { border-color: var(--accent); }
    .search-row input::placeholder { color: var(--muted); }

    .btn {
      background: var(--accent2);
      border: none;
      border-radius: 10px;
      color: #fff;
      cursor: pointer;
      font-family: inherit;
      font-size: .95rem;
      font-weight: 600;
      padding: .75rem 1.2rem;
      white-space: nowrap;
      transition: background .2s, transform .1s;
    }
    .btn:hover  { background: var(--accent); }
    .btn:active { transform: scale(.97); }
    .btn:disabled { opacity: .5; cursor: not-allowed; }

    .my-ip-link {
      margin-top: .6rem;
      font-size: .82rem;
      color: var(--muted);
      text-align: center;
    }
    .my-ip-link button {
      background: none;
      border: none;
      color: var(--accent);
      cursor: pointer;
      font-size: inherit;
      font-family: inherit;
      text-decoration: underline;
    }

    /* ── Loader ── */
    .loader {
      display: none;
      text-align: center;
      padding: 1.5rem 0;
      color: var(--muted);
      font-size: .9rem;
    }
    .loader .spinner {
      width: 32px; height: 32px;
      border: 3px solid var(--border);
      border-top-color: var(--accent);
      border-radius: 50%;
      animation: spin .7s linear infinite;
      margin: 0 auto .8rem;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* ── Error ── */
    .error-box {
      display: none;
      margin-top: 1.2rem;
      background: rgba(248,81,73,.12);
      border: 1px solid rgba(248,81,73,.35);
      border-radius: 10px;
      padding: .9rem 1rem;
      color: var(--error);
      font-size: .9rem;
    }

    /* ── Results ── */
    .results {
      display: none;
      margin-top: 1.4rem;
    }
    .results-header {
      display: flex;
      align-items: center;
      gap: .6rem;
      margin-bottom: 1rem;
      padding-bottom: .8rem;
      border-bottom: 1px solid var(--border);
    }
    .results-header .ip-badge {
      background: linear-gradient(135deg,#1f6feb,#388bfd);
      border-radius: 8px;
      font-size: .8rem;
      font-weight: 600;
      letter-spacing: .04em;
      padding: .25rem .65rem;
    }
    .results-header .flag { font-size: 1.5rem; }

    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: .75rem;
    }
    @media (max-width: 420px) { .grid { grid-template-columns: 1fr; } }

    .info-item {
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: .75rem 1rem;
    }
    .info-item .label {
      font-size: .72rem;
      font-weight: 600;
      letter-spacing: .06em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: .25rem;
    }
    .info-item .value {
      font-size: .95rem;
      font-weight: 500;
      word-break: break-all;
    }
    .info-item .value.na { color: var(--muted); font-style: italic; }

    .map-link {
      display: inline-flex;
      align-items: center;
      gap: .35rem;
      margin-top: 1rem;
      color: var(--accent);
      font-size: .85rem;
      text-decoration: none;
      font-weight: 500;
    }
    .map-link:hover { text-decoration: underline; }

    /* ── Footer ── */
    footer {
      margin-top: 2.5rem;
      color: var(--muted);
      font-size: .78rem;
      text-align: center;
    }
  </style>
</head>
<body>

<header>
  <div class="icon">🌐</div>
  <h1>IP Geolocation Lookup</h1>
  <p>Instantly locate any IP address on the planet</p>
</header>

<div class="card">
  <div class="search-row">
    <input id="ipInput" type="text" placeholder="Enter IP address (e.g. 8.8.8.8)" autocomplete="off"
           autocorrect="off" autocapitalize="off" spellcheck="false" />
    <button class="btn" id="lookupBtn" onclick="lookup()">Lookup</button>
  </div>
  <div class="my-ip-link">
    <button onclick="lookupMyIP()">Use my IP address</button>
  </div>

  <div class="loader" id="loader">
    <div class="spinner"></div>
    Fetching geolocation data…
  </div>

  <div class="error-box" id="errorBox"></div>

  <div class="results" id="results">
    <div class="results-header">
      <span class="flag" id="flagEmoji"></span>
      <span class="ip-badge" id="ipBadge"></span>
      <span id="hostnameSmall" style="color:var(--muted);font-size:.82rem;"></span>
    </div>
    <div class="grid" id="infoGrid"></div>
    <a class="map-link" id="mapLink" href="#" target="_blank" rel="noopener noreferrer">
      📍 View on Google Maps
    </a>
  </div>
</div>

<footer>Powered by <a href="https://ipinfo.io" style="color:var(--accent);text-decoration:none;">ipinfo.io</a></footer>

<script>
  const input = document.getElementById('ipInput');
  input.addEventListener('keydown', e => { if (e.key === 'Enter') lookup(); });

  function countryToFlag(code) {
    if (!code || code.length !== 2) return '🌍';
    return String.fromCodePoint(...[...code.toUpperCase()].map(c => 0x1F1E6 + c.charCodeAt(0) - 65));
  }

  function val(v) {
    return v && v !== 'undefined' ? v : null;
  }

  function setLoading(on) {
    document.getElementById('loader').style.display = on ? 'block' : 'none';
    document.getElementById('lookupBtn').disabled = on;
    if (on) {
      document.getElementById('results').style.display = 'none';
      document.getElementById('errorBox').style.display = 'none';
    }
  }

  function showError(msg) {
    const box = document.getElementById('errorBox');
    box.textContent = '⚠️  ' + msg;
    box.style.display = 'block';
  }

  function renderResults(d) {
    document.getElementById('flagEmoji').textContent = countryToFlag(d.country);
    document.getElementById('ipBadge').textContent   = d.ip || '—';
    document.getElementById('hostnameSmall').textContent = val(d.hostname) || '';

    const fields = [
      { label: 'City',         value: val(d.city) },
      { label: 'Region',       value: val(d.region) },
      { label: 'Country',      value: val(d.country) },
      { label: 'Postal Code',  value: val(d.postal) },
      { label: 'Coordinates',  value: val(d.loc) },
      { label: 'Timezone',     value: val(d.timezone) },
      { label: 'Organization', value: val(d.org) },
      { label: 'Hostname',     value: val(d.hostname) },
    ];

    const grid = document.getElementById('infoGrid');
    grid.innerHTML = fields.map(f => `
      <div class="info-item">
        <div class="label">${f.label}</div>
        <div class="value ${f.value ? '' : 'na'}">${f.value || 'N/A'}</div>
      </div>`).join('');

    if (d.loc) {
      const [lat, lon] = d.loc.split(',');
      document.getElementById('mapLink').href =
        `https://www.google.com/maps?q=${encodeURIComponent(lat)},${encodeURIComponent(lon)}`;
      document.getElementById('mapLink').style.display = 'inline-flex';
    } else {
      document.getElementById('mapLink').style.display = 'none';
    }

    document.getElementById('results').style.display = 'block';
  }

  async function lookup() {
    const ip = input.value.trim();
    if (!ip) { showError('Please enter an IP address.'); return; }
    setLoading(true);
    try {
      const res  = await fetch('/api/lookup', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ ip })
      });
      const data = await res.json();
      setLoading(false);
      if (!res.ok || data.error) { showError(data.error || 'Lookup failed.'); return; }
      renderResults(data);
    } catch (err) {
      setLoading(false);
      showError('Network error. Is the server running?');
    }
  }

  async function lookupMyIP() {
    setLoading(true);
    try {
      const res  = await fetch('/api/lookup', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ ip: '' })
      });
      const data = await res.json();
      setLoading(false);
      if (!res.ok || data.error) { showError(data.error || 'Lookup failed.'); return; }
      input.value = data.ip || '';
      renderResults(data);
    } catch (err) {
      setLoading(false);
      showError('Network error. Is the server running?');
    }
  }
</script>
</body>
</html>"""

IP_RE = re.compile(
    r"^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)

def is_valid_ip(ip: str) -> bool:
    return bool(IP_RE.match(ip))


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/lookup", methods=["POST"])
def api_lookup():
    body = request.get_json(silent=True) or {}
    ip = (body.get("ip") or "").strip()

    # If non-empty, validate format to prevent SSRF-style abuse
    if ip and not is_valid_ip(ip):
        return jsonify({"error": "Invalid IP address format."}), 400

    try:
        target = ip if ip else ""
        url = f"https://ipinfo.io/{target}/json" if target else "https://ipinfo.io/json"
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            return jsonify({"error": f"ipinfo.io returned status {resp.status_code}."}), 502
        return jsonify(resp.json())
    except requests.Timeout:
        return jsonify({"error": "Request timed out. Try again."}), 504
    except requests.RequestException as exc:
        return jsonify({"error": str(exc)}), 502


if __name__ == "__main__":
    import webbrowser, threading, time

    def open_browser():
        time.sleep(1)
        webbrowser.open("http://localhost:5000")

    threading.Thread(target=open_browser, daemon=True).start()
    print("Starting IP Geolocation Lookup → http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
