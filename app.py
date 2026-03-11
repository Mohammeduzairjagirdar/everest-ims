import streamlit as st
import sqlite3
import pandas as pd
import ipaddress
import re

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False

st.set_page_config(page_title="Infrastructure Portal", layout="wide")

# GLOBAL CSS
st.markdown("""
<style>

/* Dialog fixes */
button[aria-label="Close"] { display:none !important; }

/* Sidebar layout */
section[data-testid="stSidebarContent"] { padding-bottom:70px !important; }

/* ADD THESE FROM DELETED BLOCKS */

section[data-testid="stSidebar"] > div:first-child { height:auto !important; }
.stAppViewContainer { height:auto !important; }
.block-container { padding-bottom:0rem !important; }
[data-testid="column"] { align-self:flex-start !important; }

</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "edit_ip" not in st.session_state:
    st.session_state["edit_ip"] = None


def authenticate(email, password):
    conn = sqlite3.connect("infra.db")
    c = conn.cursor()
    c.execute("SELECT * FROM auth_users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()
    return user


if not st.session_state.logged_in:

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; box-sizing: border-box; }

    #MainMenu, header, footer { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    .stApp { background: transparent !important; }

    /* ── Full page fixed background split ── */
    .bg {
        position: fixed; inset: 0; display: flex; z-index: 0;
    }
    .bg-left {
        width: 45%;
        background: linear-gradient(145deg, #2952d9 0%, #1a3ab8 60%, #122a8a 100%);
    }
    .bg-right { width: 55%; background: #eaeef5; }

    /* ── Left branding ── */
    .left-brand {
        position: fixed;
        top: 50%; left: 22.5%;
        transform: translate(-50%, -50%);
        color: white; z-index: 5; pointer-events: none;
    }
    .left-brand h1 { font-size: 44px; font-weight: 800; margin: 0 0 14px 0; line-height: 1.15; color: white; }
    .left-brand p  { font-size: 18px; margin: 5px 0; opacity: 0.9; color: white; }

    /* ── Card container: fixed, centered in right panel ── */
    .card-wrap {
        position: fixed;
        top: 0; bottom: 0;
        left: 45%; right: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 5;
        pointer-events: none;
    }
    .card-box {
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 70px rgba(0,0,0,0.13);
        padding: 50px 44px;
        width: 400px;
        pointer-events: none;
    }

    [data-testid="stForm"] {
        position: fixed !important;
        top: 50% !important;
        left: 72.5% !important;
        transform: translate(-50%, -50%) !important;
        width: 400px !important;
        background: white !important;
        padding: 50px 44px !important;
        border-radius: 20px !important;
        box-shadow: 0 20px 70px rgba(0,0,0,0.13) !important;
        border: none !important;
        z-index: 10 !important;
        height: auto !important;
        max-height: none !important;
        overflow: visible !important;
    }

    [data-testid="stForm"] h3 {
        font-size: 28px !important; font-weight: 700 !important;
        color: #0f172a !important; text-align: center !important;
        margin-bottom: 28px !important;
    }
    [data-testid="stForm"] label p {
        font-size: 14px !important; font-weight: 600 !important; color: #374151 !important;
    }
    [data-testid="stForm"] input {
        height: 48px !important; border-radius: 10px !important;
        border: 1.5px solid #d1d5db !important;
        font-size: 15px !important; background: white !important; color: #111 !important;
    }
    [data-testid="stForm"] input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.15) !important;
    }
    [data-testid="stForm"] button,
    [data-testid="stForm"] .stFormSubmitButton button {
        height: 50px !important; border-radius: 12px !important;
        background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
        color: white !important; font-weight: 700 !important;
        font-size: 16px !important; border: none !important;
        width: 100% !important; letter-spacing: 0.3px !important;
        margin-top: 6px !important;
    }
    [data-testid="stForm"] button:hover { opacity: 0.9 !important; }
    [data-testid="stForm"] > div { border: none !important; }

    [data-testid="stForm"] button[aria-label="Show password text"],
    [data-testid="stForm"] button[aria-label="Hide password text"],
    [data-testid="stForm"] [data-testid="stTextInput"] button {
        background: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
        width: 36px !important;
        height: 36px !important;
        min-height: unset !important;
        padding: 4px !important;
        margin: 0 !important;
        color: #6b7280 !important;
    }
    [data-testid="stForm"] [data-testid="stTextInput"] button:hover {
        background: #f3f4f6 !important;
        opacity: 1 !important;
        transform: none !important;
    }
    [data-testid="stForm"] [data-testid="stTextInput"] button svg {
        width: 18px !important;
        height: 18px !important;
    }

    section[data-testid="stSidebar"] { display: none; }
    .stMainBlockContainer, 
    [data-testid="stMainBlockContainer"] {
        padding: 0 !important;
        margin: 0 !important;
    }
                
    </style>

    <div class="bg">
        <div class="bg-left"></div>
        <div class="bg-right"></div>
    </div>
    <div class="left-brand">
        <h1>EverestIMS IT</h1>
        <p>Authorized Access Only</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <style>
        [data-testid="InputInstructions"] { display: none !important; }
        </style>
        """, unsafe_allow_html=True)
    st.markdown("""
<style>
[data-testid="InputInstructions"] { display: none !important; }
[data-testid="stForm"] input:focus {
    border-color: #d1d5db !important;
    box-shadow: none !important;
    outline: none !important;
}
[data-testid="stForm"] [data-baseweb="input"]:focus-within {
    border-color: #d1d5db !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)
    st.markdown("""
<style>
[data-testid="stForm"] [data-baseweb="input"] {
    border: 1.5px solid #d1d5db !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}
[data-testid="stForm"] [data-baseweb="input"]:focus-within {
    border: 1.5px solid #d1d5db !important;
    box-shadow: none !important;
}
[data-testid="stForm"] input {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}
[data-testid="InputInstructions"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

    with st.form("login_form", border=False):
        st.markdown("### Login")
        email    = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Please enter your email and password.")
            else:
                user = authenticate(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password.")

    st.stop()

# =====================================================
# SMART CSV IMPORT FUNCTION
# =====================================================
def import_csv_data(df, conn):
    # use the shared connection directly to avoid sqlite3 lock contention
    import_conn = conn
    cur = import_conn.cursor()
    ip_count = 0
    server_count = 0
    vm_count_inserted = 0
    filled_count = 0

    # ── normalize column names ──
    df.columns = df.columns.str.strip()
    df = df.rename(columns={
    "IP": "ip_address",
    "HOST": "host_ip",          # ← FIXED
    "TEAM NAME": "team_name",
    "USER NAME": "vm_name",
    "CPU": "cpu_required",
    "RAM(GB)": "ram_required",
    "Disk(GB)": "storage_required",
    "VM Status": "vm_status",
    "STATUS": "status"
})

    if "ip_address" in df.columns:
        # filter out non-IP values like 'free-ip', 'NA'
        valid_ips = df["ip_address"].dropna().astype(str)
        valid_ips = valid_ips[valid_ips.str.match(r'^\d+\.\d+\.\d+\.\d+$')]
        csv_ips = valid_ips.tolist()

        for ip in csv_ips:
            if not validate_ip(ip):
                continue
            ip = str(ip).strip()
            existing = cur.execute("SELECT ip_address FROM ip_pool WHERE ip_address=?", (ip,)).fetchone()
            if not existing:
                cur.execute("INSERT OR IGNORE INTO ip_pool (ip_address, ip_status) VALUES (?, 'free')", (ip,))
                ip_count += 1

                if ip_count % 50 == 0:
                    import_conn.commit()

        if csv_ips:
            try:
                ip_objects = sorted([ipaddress.IPv4Address(str(ip).strip()) for ip in csv_ips])
                min_ip = ip_objects[0]
                max_ip = ip_objects[-1]
                full_range = [str(ipaddress.IPv4Address(i)) for i in range(int(min_ip), int(max_ip) + 1)]
                csv_ip_set = set(str(ip) for ip in ip_objects)
                for ip in full_range:
                    if ip not in csv_ip_set:
                        existing = cur.execute("SELECT ip_address FROM ip_pool WHERE ip_address=?", (ip,)).fetchone()
                        if not existing:
                            cur.execute("INSERT OR IGNORE INTO ip_pool (ip_address, ip_status) VALUES (?, 'free')", (ip,))
                            filled_count += 1
            except Exception:
                pass

    if "host_ip" in df.columns:
        valid_hosts = df["host_ip"].dropna().astype(str)
        valid_hosts = valid_hosts[valid_hosts.str.match(r'^\d+\.\d+\.\d+\.\d+$')]
        for host_ip in valid_hosts.unique():
            host_ip = str(host_ip).strip()
            existing = cur.execute("SELECT server_id FROM servers WHERE host_ip=?", (host_ip,)).fetchone()
            if not existing:
                count = cur.execute("SELECT COUNT(*) FROM servers").fetchone()[0]
                auto_name = f"Host-{str(count + 1).zfill(2)}"
                cur.execute("""
                    INSERT INTO servers
                    (host_ip, server_name, server_type, total_cpu, total_ram, total_storage, status)
                    VALUES (?, ?, 'Unknown', 0, 0, 0, 'active')
                """, (host_ip, auto_name))
                server_count += 1
    
    # CRITICAL FIX: commit servers before VM loop so host_ip lookup works
    import_conn.commit()

    if "vm_name" in df.columns:
        for row in df.itertuples(index=False):

            vm_name = str(getattr(row, "vm_name", "")).strip()
            team_name = str(getattr(row, "team_name", "")).strip()
            ip = str(getattr(row, "ip_address", "")).strip()
            host_ip = str(getattr(row, "host_ip", "")).strip()

            cpu = getattr(row, "cpu_required", 0)
            ram = getattr(row, "ram_required", 0)
            disk = getattr(row, "storage_required", 0)

            try: cpu = int(float(cpu))
            except: cpu = 0
            try: ram = int(float(ram))
            except: ram = 0
            try: disk = int(float(disk))
            except: disk = 0

            if not vm_name or vm_name.lower() == "nan":
                continue

            # Find server_id using host_ip
            server_id = None                          # ← must be at THIS indent level
            if host_ip and re.match(r'^\d+\.\d+\.\d+\.\d+$', host_ip):
                server = cur.execute(
                    "SELECT server_id FROM servers WHERE host_ip=?",
                    (host_ip,)
                ).fetchone()
                if server:
                    server_id = server[0]

            existing = cur.execute(
                "SELECT vm_name FROM vm_requests WHERE vm_name=?",
                (vm_name,)
            ).fetchone()

            if not existing:
                purpose_val = str(getattr(row, "purpose", "Development")).strip()
                purpose = purpose_val if purpose_val in ["Development", "Testing", "R&D"] else "Development"
                cur.execute("""
                INSERT INTO vm_requests
                (vm_name, team_name, server_id, ip_address, cpu_required, ram_required, storage_required, purpose, approval_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
                """, (vm_name, team_name, server_id, ip, cpu, ram, disk, purpose))

                vm_count_inserted += 1
                if ip and validate_ip(ip):
                    cur.execute(
                        "UPDATE ip_pool SET ip_status='assigned' WHERE ip_address=?",
                        (ip,)
                    )

    import_conn.commit()
    return ip_count, server_count, vm_count_inserted, filled_count




def go(page_name):
    st.session_state["page"] = page_name
    st.rerun()

st.markdown("""
<style>
div[role="dialog"] > div {
    background: #ffffff !important; border-radius: 0px !important;
    border: 1px solid #d1d5db !important; box-shadow: 0 8px 25px rgba(0,0,0,0.25) !important;
    padding: 22px !important; max-height: 80vh !important; overflow-y: auto !important;
}
div[role="dialog"] h2, div[role="dialog"] h3 { color: #111827 !important; font-weight: 700 !important; }
div[role="dialog"] p { color: #374151 !important; }
div[role="dialog"] code { background: #ecfdf5 !important; color: #166534 !important; padding: 4px 8px; border-radius: 3px; font-weight: 600; }
div[role="dialog"] button:first-of-type { background: #e11d48 !important; color: white !important; border: none !important; }
div[role="dialog"] button:first-of-type:hover { background: #be123c !important; }
div[role="dialog"] button:last-of-type { background: #e5e7eb !important; color: #111827 !important; border: none !important; }
div[data-testid="stDialog"] { display: flex !important; align-items: center !important; justify-content: center !important; }
div[role="dialog"] { pointer-events: all !important; margin: auto !important; top: auto !important; }
div[role="dialog"][data-testid="stDialog"]::before { content: ""; position: fixed; inset: 0; background: rgba(30, 41, 59, 0.25); backdrop-filter: blur(4px); z-index: -1; }
div[role="dialog"] button { margin-top: 12px !important; }
div[role="dialog"] div[data-testid="stHorizontalBlock"] { margin-top: 18px !important; }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
div[data-testid="stModal"] { position: fixed !important; inset: 0 !important; display: flex !important; align-items: center !important; justify-content: center !important; padding: 0 !important; margin: 0 !important; }
div[data-testid="stModal"] > div { margin: 0 auto !important; transform: none !important; }
div[data-testid="stModalBackdrop"] { position: fixed !important; inset: 0 !important; background: rgba(0,0,0,0.45) !important; backdrop-filter: blur(4px) !important; }
body:has(div[data-testid="stModal"]) { overflow: hidden !important; }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
[data-testid="stDialog"] { position: fixed !important; inset: 0 !important; display: flex !important; align-items: center !important; justify-content: center !important; padding-top: 0px !important; }
[data-testid="stDialog"] > div { margin-top: 0px !important; }
[data-testid="stDialogOverlay"] { position: fixed !important; inset: 0 !important; background: rgba(0,0,0,0.45) !important; backdrop-filter: blur(3px); }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
div[data-testid="stButton"] > button { padding: 0.25rem 0.45rem; font-size: 14px; border-radius: 8px; height: 32px; }
.action-row { display:flex; gap:6px; align-items:center; }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.stApp { background: #f4f7fb !important; }
[data-testid="stMetric"] { border: none !important; }
[data-testid="stMetric"] > div { border: none !important; }
[data-testid="stHorizontalBlock"] { border-top: 0px !important; box-shadow: none !important; }
div[data-testid="stButton"] > button { background: #e9e8ff !important; color: #1e293b !important; border-radius: 12px !important; border: 1px solid #dcdafe !important; font-weight: 600 !important; padding: 0.45rem 1.2rem !important; transition: 0.25s ease !important; }
div[data-testid="stButton"] > button:hover { background: #ddd6fe !important; }
button[data-testid="baseButton-go_dashboard"] p, button[data-testid="baseButton-go_ip"] p, button[data-testid="baseButton-go_host"] p { color: #0f172a !important; font-weight: 700 !important; }
button[data-testid="baseButton-go_dashboard"], button[data-testid="baseButton-go_ip"], button[data-testid="baseButton-go_host"] { color: #0f172a !important; height: 220px !important; width: 100% !important; border-radius: 22px !important; background: #e9e8ff !important; color: #1e293b !important; display:flex !important; flex-direction:column !important; align-items:center !important; justify-content:center !important; gap:14px; font-size:0px !important; }
button[data-testid="baseButton-go_dashboard"] p:first-child, button[data-testid="baseButton-go_ip"] p:first-child, button[data-testid="baseButton-go_host"] p:first-child { font-size:70px !important; }
button[data-testid="baseButton-go_dashboard"] p:last-child, button[data-testid="baseButton-go_ip"] p:last-child, button[data-testid="baseButton-go_host"] p:last-child { font-size:24px !important; font-weight:600 !important; }
button[data-testid="baseButton-primary"] { background: #e9e8ff !important; color: #1e293b !important; border-radius: 12px !important; border: 1px solid #dcdafe !important; font-weight: 600 !important; }
button[data-testid="baseButton-primary"]:hover { background: #ddd6fe !important; border: 1px solid #c4b5fd !important; box-shadow: 0 8px 18px rgba(139,92,246,0.25); }
div[data-testid="stFormSubmitButton"] > button { background: #e9e8ff !important; color: #1e293b !important; border-radius: 12px !important; border: 1px solid #dcdafe !important; font-weight: 600 !important; }
div[data-testid="stFormSubmitButton"] > button:hover { background: #ddd6fe !important; border: 1px solid #c4b5fd !important; box-shadow: 0 8px 18px rgba(139,92,246,0.25); }
.landing-menu { width: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 90px; }
.landing-title { text-align: center !important; font-size: 48px !important; font-weight: 700 !important; color: #0f172a !important; margin-bottom: 8px; }
.landing-sub { text-align: center !important; font-size: 16px !important; color: #64748b !important; margin-bottom: 60px; }
.landing-divider { width: 160px; height: 3px; background: linear-gradient(90deg, #8b87f7, #a5b4fc); border-radius: 10px; margin: 18px auto 35px auto; display: block; }
html, body, [class*="css"] { color: #0f172a !important; }
h1, h2, h3, h4, h5, h6 { color: #020617 !important; font-weight: 700 !important; }
label { color: #111827 !important; font-weight: 600 !important; }
input, textarea { color: #020617 !important; }
div[data-baseweb="select"] div { color: #020617 !important; }
::placeholder { color: #475569 !important; }
[data-testid="stMetricValue"] { color: #020617 !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #334155 !important; }
thead tr th { color: #020617 !important; font-weight: 700 !important; }
tbody tr td { color: #0f172a !important; }
button[data-testid="baseButton-go_dashboard"] div p span, button[data-testid="baseButton-go_ip"] div p span, button[data-testid="baseButton-go_host"] div p span { color: #111827 !important; font-weight: 800 !important; opacity: 1 !important; }
button[data-testid="baseButton-go_dashboard"] div p, button[data-testid="baseButton-go_ip"] div p, button[data-testid="baseButton-go_host"] div p { color: #111827 !important; font-weight: 800 !important; }
.stButton button p, .stButton button span, .stButton button div { color: #111827 !important; font-weight: 800 !important; opacity: 1 !important; }
button[kind="secondary"] p, button[kind="secondary"] span { color: #111827 !important; font-weight: 800 !important; }
button p { color: #111827 !important; font-weight: 800 !important; }
hr { display: none !important; }
section[data-testid="stMain"] { border-top: none !important; }
section[data-testid="stMain"] > div:first-child { border-top: none !important; box-shadow: none !important; }
.landing-wrapper { max-width: 1000px; margin: auto; margin-top: 120px; text-align: center; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1rem !important; margin-top: 0rem !important; }
section[data-testid="stMain"] > div { padding-top: 0.5rem !important; }
header[data-testid="stHeader"] { height: 0px !important; min-height: 0px !important; }
div[data-testid="stAppViewContainer"] { padding-top: 0px !important; }
hr { border: none !important; height: 0px !important; margin: 0px !important; }
[data-testid="stMarkdownContainer"] hr { display: none !important; }
div[data-testid="stDecoration"] { display: none !important; height: 0px !important; }
header[data-testid="stHeader"]::after { display: none !important; content: none !important; }
header[data-testid="stHeader"] { box-shadow: none !important; border-bottom: none !important; }
:focus-visible { outline: none !important; }
[data-testid="stToolbar"] { border-bottom: none !important; box-shadow: none !important; background: transparent !important; }
[data-testid="stToolbar"]::after { display: none !important; content: none !important; height: 0px !important; }
header[data-testid="stHeader"] { border-bottom: 0px !important; box-shadow: none !important; }
button:focus, button:focus-visible { outline: none !important; box-shadow: none !important; }
section[data-testid="stMain"] div[data-testid="stVerticalBlock"] > div:first-child { border-top: none !important; box-shadow: none !important; padding-top: 0 !important; }
div[data-testid="stHorizontalBlock"] { border: none !important; box-shadow: none !important; }
div[data-testid="element-container"] { border-top: none !important; }
a[href^="#"] { display: none !important; }
h1 > a, h2 > a, h3 > a { display: none !important; }
h1::after, h2::after, h3::after { display: none !important; content: none !important; }
:target { outline: none !important; border: none !important; }
div[data-testid="block-container"]::before { display: none !important; content: none !important; background: none !important; height: 0px !important; }
.main .block-container::before { display: none !important; }
div[data-testid="stAppViewContainer"] > section.main > div { padding-top: 0rem !important; }
.main .block-container { padding-top: 1rem !important; margin-top: 0rem !important; }
section[data-testid="stSidebar"] { position: fixed !important; right: 0 !important; left: auto !important; top: 0 !important; height: 100vh !important; width: 620px !important; min-width: 620px !important; max-width: 620px !important; background: #f8fafc !important; border-left: 1px solid #d1d5db !important; z-index: 1000 !important; }
section[data-testid="stSidebar"] > div:first-child { width: 620px !important; padding: 28px !important; }
div[data-testid="stAppViewContainer"] > section.main { margin-right: 620px !important; }
button[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] .stTextInput, section[data-testid="stSidebar"] .stNumberInput, section[data-testid="stSidebar"] .stSelectbox { width: 100% !important; }
header[data-testid="stHeader"] { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
div[data-testid="stAppViewContainer"] > section.main > div { padding-top: 0rem !important; }
.main .block-container { padding-top: 1rem !important; margin-top: 0rem !important; }
section[data-testid="stSidebar"] div[data-testid="stSidebarHeader"] { display: none !important; height: 0px !important; padding: 0px !important; margin: 0px !important; }
section[data-testid="stSidebar"] > div:first-child { padding-top: 8px !important; }
section[data-testid="stSidebar"] .block-container { padding-top: 0px !important; margin-top: 0px !important; }
section[data-testid="stSidebar"] div:first-child > div:first-child { margin-top: 0px !important; padding-top: 0px !important; }
section[data-testid="stSidebar"] > div:first-child { display: flex !important; flex-direction: column !important; height: 100vh !important; }
section[data-testid="stSidebar"] .block-container { flex-grow: 1 !important; display: flex !important; flex-direction: column !important; }
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:last-child { margin-top: auto !important; padding-top: 16px !important; padding-bottom: 18px !important; background: #f8fafc !important; position: sticky; bottom: 0; }
section[data-testid="stSidebar"] button { height: 42px !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]{ margin-bottom: 60px !important; }
section[data-testid="stSidebar"] .block-container{ display:flex !important; flex-direction:column !important; }
section[data-testid="stSidebar"] .stButton button{ margin-bottom: 0px !important; }
div[data-testid="stDialog"], div[role="dialog"] { z-index: 20000 !important; }
div[data-testid="stDialogOverlay"] { z-index: 19999 !important; }
</style>
""", unsafe_allow_html=True)

# ----------- DB -----------
conn = sqlite3.connect("infra.db", check_same_thread=False, timeout=60)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA busy_timeout=60000")
servers = pd.read_sql("SELECT * FROM servers", conn)

st.markdown("""
<style>
/* Force sidebar columns to be side by side */
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    display: flex !important;
    gap: 10px !important;
    margin-bottom: 0px !important;
}
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] > div {
    flex: 1 !important;
    width: auto !important;
}
</style>
""", unsafe_allow_html=True)

# Add this st.markdown block anywhere after your other CSS blocks
# (paste it right before your DB connection line: conn = sqlite3.connect...)

st.markdown("""
<style>
/* ===== PIN SAVE/CANCEL BUTTONS TO BOTTOM OF SIDEBAR ===== */

/* make sidebar a flex column so we can push buttons down */
section[data-testid="stSidebar"] > div:first-child {
    display: flex !important;
    flex-direction: column !important;
    height: 100vh !important;
    overflow-y: auto !important;
}

/* the last horizontal block (Save + Cancel row) sticks to bottom */
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:last-of-type {
    margin-top: auto !important;
    position: sticky !important;
    bottom: 0 !important;
    background: #f8fafc !important;
    padding: 16px 0 20px 0 !important;
    border-top: 1px solid #e2e8f0 !important;
    z-index: 10 !important;
}
</style>
""", unsafe_allow_html=True )

st.markdown("""
<style>
div[data-testid="stDownloadButton"] > button {
    background: #e9e8ff !important;
    color: #1e293b !important;
    border-radius: 12px !important;
    border: 1px solid #dcdafe !important;
    font-weight: 600 !important;
    padding: 0.45rem 1.2rem !important;
    transition: 0.25s ease !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: #ddd6fe !important;
    border: 1px solid #c4b5fd !important;
}
</style>
""", unsafe_allow_html=True)


# ================= CAPACITY CHECK FUNCTION =================
def check_server_capacity(server_id, cpu_req, ram_req, disk_req):
    cur = conn.cursor()
    total = cur.execute("SELECT total_cpu, total_ram, total_storage FROM servers WHERE server_id=?", (server_id,)).fetchone()
    total_cpu, total_ram, total_disk = total
    used = cur.execute("SELECT COALESCE(SUM(cpu_required),0), COALESCE(SUM(ram_required),0), COALESCE(SUM(storage_required),0) FROM vm_requests WHERE server_id=?", (server_id,)).fetchone()
    used_cpu, used_ram, used_disk = used
    available_cpu = total_cpu - used_cpu
    available_ram = total_ram - used_ram
    available_disk = total_disk - used_disk
    if cpu_req > available_cpu:
        return False, f"Only {available_cpu} CPU cores available"
    if ram_req > available_ram:
        return False, f"Only {available_ram} GB RAM available"
    if disk_req > available_disk:
        return False, f"Only {available_disk} GB storage available"
    return True, "OK"

# ----------- SESSION STATES -----------
if "editing_ip" not in st.session_state:
    st.session_state.editing_ip = None

if "form_reset" not in st.session_state:
    st.session_state.form_reset = 0

if "form_id" not in st.session_state:
    st.session_state.form_id = 0

if "show_form" not in st.session_state:
    st.session_state.show_form = False

if "edit_vm_ip" not in st.session_state:
    st.session_state.edit_vm_ip = None

if "ip_page" not in st.session_state:
    st.session_state.ip_page = 1

if "open_host_drawer" not in st.session_state:
    st.session_state.open_host_drawer = False

if "open_vm_drawer" not in st.session_state:
    st.session_state.open_vm_drawer = False

if "show_host_csv" not in st.session_state:
    st.session_state.show_host_csv = False

if "confirm_vm_create" not in st.session_state:
    st.session_state.confirm_vm_create = False
# ================= EDIT MODAL STATE =================
if "edit_ip_open" not in st.session_state:
    st.session_state.edit_ip_open = False

if "edit_ip_data" not in st.session_state:
    st.session_state.edit_ip_data = None
# ---------- PAGE ROUTER ----------
if "page" not in st.session_state:
    st.session_state.page = "landing"
@st.dialog("Confirm VM Creation")
def confirm_vm_dialog(owner_name, team_name, server_choice, ip_choice, cpu, ram, disk, purpose):
    st.markdown("### ⚠️ Are you sure you want to create this VM?")
    st.write(f"**IP:** {ip_choice}")
    st.write(f"**CPU:** {cpu} cores | **RAM:** {ram} GB | **Disk:** {disk} GB")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes, Create", use_container_width=True):
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO vm_requests
                    (vm_name, team_name, server_id, ip_address, cpu_required, ram_required, storage_required, purpose, approval_status)
                    VALUES(?,?,?,?,?,?,?,?,?)
                """, (owner_name, team_name, server_choice, ip_choice, cpu, ram, disk, purpose, "Pending"))
                cur.execute("UPDATE ip_pool SET ip_status='assigned' WHERE ip_address=?", (ip_choice,))
                conn.commit()
                st.session_state.open_vm_drawer = False
                st.rerun()
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
                st.rerun()

# =====================================================
# LANDING PAGE
# =====================================================
if st.session_state.page == "landing":
    st.markdown("""<style>
.logout-btn { position: fixed; top: 12px; right: 16px; z-index: 9999; display: flex; gap: 10px; align-items: center; }
.logout-btn button { background: #e9e8ff !important; color: #1e293b !important; border-radius: 12px !important; border: 1px solid #dcdafe !important; font-weight: 600 !important; padding: 10px 22px !important; }
.logout-btn button:hover { background: #ddd6fe !important; }
</style>""", unsafe_allow_html=True)

    st.markdown("""
        <div style="position:fixed;top:12px;right:16px;z-index:99999;">
            <a href="?logout=true" target="_self">
                <button style="background:#b3c2e8;color:#1a2f6e;border:none;border-radius:12px;font-weight:700;padding:8px 20px;cursor:pointer;font-size:14px;box-shadow:0 2px 8px rgba(0,0,0,0.08);">🔓 Logout</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

    if st.query_params.get("logout") == "true":
        st.session_state.logged_in = False
        st.session_state.page = "landing"
        st.query_params.clear()
        st.rerun()

    st.markdown("""
    <style>
    section[data-testid="stMain"] {
        background: linear-gradient(145deg, #2952d9 0%, #1a3ab8 60%, #122a8a 100%) !important;
        min-height: 100vh !important;
    }
    .stApp { background: linear-gradient(145deg, #2952d9 0%, #1a3ab8 60%, #122a8a 100%) !important; }
    .landing-title { color: white !important; -webkit-text-fill-color: white !important; }
    .landing-sub { color: rgba(255,255,255,0.85) !important; }
    div[data-testid="stButton"] > button {
        background: #b3c2e8 !important;
        color: #1a2f6e !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        font-weight: 700 !important;
        height: 130px !important;
        font-size: 16px !important;
    }
    div[data-testid="stButton"] > button:hover {
        background: #c5d0f0 !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.13) !important;
    }
    button p { color: #1a2f6e !important; font-weight: 700 !important; }
    div[data-testid="stDownloadButton"] > button {
        background: #b3c2e8 !important;
        color: #1a2f6e !important;
        border: none !important;
        border-radius: 20px !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background: #c5d0f0 !important;
    }
    button p { color: #1a2f6e !important; font-weight: 700 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="landing-title"> IP Management Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="landing-sub">Server & VM Management System</div>', unsafe_allow_html=True)

    _, center_col, _ = st.columns([3, 2, 3])
    with center_col:

        # -------- DOWNLOAD TEMPLATE --------
        template = """IP,HOST,TEAM NAME,USER NAME,CPU,RAM(GB),Disk(GB),VM Status,STATUS,PURPOSE
        10.0.4.1,10.0.0.1,DevOps,vm_dev_01,2,4,50,Running,assigned,Development
        10.0.4.2,10.0.0.1,QA,vm_test_01,2,4,50,Running,assigned,Testing
        10.0.4.3,10.0.0.1,Research,vm_rnd_01,4,8,100,Running,assigned,R&D
        """

        st.download_button(
        "⬇ Download CSV Template",
        template,
        file_name="vm_import_template.csv",
        mime="text/csv",
        use_container_width=True,
        type="secondary"
        )

        # -------- IMPORT BUTTON --------
        if st.button("📂 Import CSV", use_container_width=True):
            st.session_state.show_csv_uploader = True

    if st.session_state.get("show_csv_uploader"):
        csv_file = st.file_uploader("Choose a CSV file", type=["csv"], key="landing_csv")
        if csv_file:
            df_preview = pd.read_csv(csv_file, encoding='latin1')
            df_preview = pd.read_csv(csv_file, encoding='latin1')

            # -------- CSV VALIDATION --------
            required_columns = [
                    "IP","HOST","TEAM NAME","USER NAME",
                    "CPU","RAM(GB)","Disk(GB)","VM Status","STATUS"
            ]

            missing_cols = [col for col in required_columns if col not in df_preview.columns]

            if missing_cols:
                    st.error(f"❌ CSV missing required columns: {', '.join(missing_cols)}")
                    st.stop()
            st.session_state["pending_import_df"] = df_preview
            st.session_state["pending_import_name"] = csv_file.name
            st.info(f"📄 **{csv_file.name}** — {len(df_preview)} rows detected. Click Import to confirm.")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Import", use_container_width=True, key="confirm_import"):

                    df_to_import = st.session_state.get("pending_import_df")

                    if df_to_import is not None:
                        with st.spinner("Importing CSV... Please wait"):
                            ip_count, server_count, vm_count, filled_count = import_csv_data(df_to_import, conn)

                        st.session_state.show_csv_uploader = False
                        st.session_state.pop("pending_import_df", None)
                        st.session_state.pop("pending_import_name", None)

                        st.success(
                            f"✅ Imported — {ip_count} IPs, {server_count} Servers, {vm_count} VMs added. "
                            f"{filled_count} missing IPs filled as free."
                        )

                        st.rerun()
                 
            with c2:
                if st.button("✖ Cancel", use_container_width=True, key="cancel_import"):
                    st.session_state.show_csv_uploader = False
                    st.session_state.pop("pending_import_df", None)
                    st.session_state.pop("pending_import_name", None)
                    st.rerun()
        elif st.session_state.get("pending_import_df") is not None:
            df_preview = st.session_state["pending_import_df"]
            fname = st.session_state.get("pending_import_name", "file.csv")
            st.info(f"📄 **{fname}** — {len(df_preview)} rows detected. Click Import to confirm.")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Import", use_container_width=True, key="confirm_import"):
                    ip_count, server_count, vm_count, filled_count = import_csv_data(df_preview, conn)
                    st.session_state.show_csv_uploader = False
                    st.session_state.pop("pending_import_df", None)
                    st.session_state.pop("pending_import_name", None)
                    st.success(f"✅ Imported — {ip_count} IPs, {server_count} Servers, {vm_count} VMs added. {filled_count} missing IPs filled as free.")
                    st.rerun()
            with c2:
                if st.button("✖ Cancel", use_container_width=True, key="cancel_import"):
                    st.session_state.show_csv_uploader = False
                    st.session_state.pop("pending_import_df", None)
                    st.session_state.pop("pending_import_name", None)
                    st.rerun()
        else:
            if st.button("✖ Cancel", key="cancel_import_empty"):
                st.session_state.show_csv_uploader = False
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        if st.button("📊\nDashboard", key="go_dashboard", use_container_width=True):
            go("Home")
    with col2:
        if st.button("🌐\nIP Availability", key="go_ip", use_container_width=True):
            go("IP Availability")
    with col3:
        if st.button("🖥️\nHost Grid", key="go_host", use_container_width=True):
            go("Host Grid")

    st.markdown("""
    <div style="position:fixed;bottom:20px;left:0;right:0;text-align:center;color:rgba(255,255,255,0.85);font-size:20px;font-weight:700;letter-spacing:1px;">
        © 2026 Infraon IT
    </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# HOME PAGE
# =====================================================
elif st.session_state.page == "Home":
    colb1, colb2 = st.columns([1,9])
    with colb1:
        if st.button("⬅ Home", key="back_home_dashboard"):
            st.session_state.page = "landing"
            st.rerun()

    st.markdown('<div class="landing-title">Infrastructure Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="landing-sub">Configurable view — choose what you want to see</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Load all data ──
    ip_df = pd.read_sql("""
        SELECT ip_pool.ip_address,
               CASE WHEN vm_requests.ip_address IS NULL THEN 'free' ELSE 'assigned' END AS ip_status,
               vm_requests.vm_name, vm_requests.team_name, vm_requests.server_id,
               vm_requests.cpu_required, vm_requests.ram_required, vm_requests.storage_required,
               vm_requests.purpose, servers.server_name, servers.host_ip
        FROM ip_pool
        LEFT JOIN vm_requests ON ip_pool.ip_address = vm_requests.ip_address
        LEFT JOIN servers ON vm_requests.server_id = servers.server_id
        ORDER BY ip_pool.ip_address
    """, conn)

    servers_df = pd.read_sql("SELECT * FROM servers", conn)
    vm_df      = pd.read_sql("SELECT * FROM vm_requests", conn)

    total_ips  = len(ip_df)
    free_ips   = len(ip_df[ip_df["ip_status"] == "free"])
    used_ips   = total_ips - free_ips
    total_hosts = len(servers_df)
    total_vms   = len(vm_df)

    # ── CONFIGURATION PANEL ──
    with st.expander("⚙️ Configure Dashboard", expanded=st.session_state.get("dash_config_open", True)):
        st.session_state["dash_config_open"] = True
        st.markdown("**Select Widgets to Display**")
        cfg_col1, cfg_col2, cfg_col3 = st.columns(3)

        with cfg_col1:
            show_summary    = st.checkbox("📊 Summary Metrics",    value=st.session_state.get("cfg_summary", True),    key="cfg_summary")
            show_ip_status  = st.checkbox("🥧 IP Status Chart",    value=st.session_state.get("cfg_ip_status", True),  key="cfg_ip_status")
            show_subnet     = st.checkbox("🌐 Subnet Breakdown",   value=st.session_state.get("cfg_subnet", True),     key="cfg_subnet")

        with cfg_col2:
            show_team       = st.checkbox("👥 VMs by Team",        value=st.session_state.get("cfg_team", True),       key="cfg_team")
            show_purpose    = st.checkbox("🎯 VMs by Purpose",     value=st.session_state.get("cfg_purpose", True),    key="cfg_purpose")
            show_host_cap   = st.checkbox("🖥️ Host Capacity",      value=st.session_state.get("cfg_host_cap", True),   key="cfg_host_cap")

        with cfg_col3:
            show_ip_table   = st.checkbox("📋 IP Records Table",   value=st.session_state.get("cfg_ip_table", True),   key="cfg_ip_table")
            show_vm_table   = st.checkbox("🗃️ VM Records Table",   value=st.session_state.get("cfg_vm_table", False),  key="cfg_vm_table")
            show_host_table = st.checkbox("🖥️ Host Records Table", value=st.session_state.get("cfg_host_table", False),key="cfg_host_table")

        st.markdown("**Select Columns to Show in IP Table**")
        all_ip_cols = ["ip_address", "host_ip", "vm_name", "team_name", "cpu_required", "ram_required", "storage_required", "purpose", "server_name", "ip_status"]
        col_labels  = {"ip_address":"IP Address","host_ip":"Host IP","vm_name":"Owner","team_name":"Team","cpu_required":"CPU","ram_required":"RAM","storage_required":"Disk","purpose":"Purpose","server_name":"Server","ip_status":"Status"}
        default_cols = st.session_state.get("cfg_ip_cols", all_ip_cols)
        selected_ip_cols = st.multiselect(
            "IP Table Columns",
            options=all_ip_cols,
            default=default_cols,
            format_func=lambda x: col_labels[x],
            key="cfg_ip_cols"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 1. SUMMARY METRICS ──
    if show_summary:
        st.markdown("### 📊 Summary Metrics")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Total IPs",    total_ips)
        m2.metric("Free IPs",     free_ips)
        m3.metric("Assigned IPs", used_ips)
        m4.metric("Total Hosts",  total_hosts)
        m5.metric("Total VMs",    total_vms)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── 2. CHARTS ROW ──
    chart_items = [show_ip_status, show_team, show_purpose]
    if any(chart_items):
        st.markdown("### 📈 Charts")
        chart_cols = st.columns(sum(1 for x in chart_items if x))
        ci = 0

        if show_ip_status:
            import plotly.express as px
            pie_df = pd.DataFrame({"Status": ["Free", "Assigned"], "Count": [free_ips, used_ips]})
            fig = px.pie(pie_df, names="Status", values="Count",
                         color="Status",
                         color_discrete_map={"Free": "#2952d9", "Assigned": "#6366f1"},
                         title="IP Pool Status")
            fig.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                              title_font_color="#1a3ab8", margin=dict(t=40,b=10,l=10,r=10))
            chart_cols[ci].plotly_chart(fig, use_container_width=True)
            ci += 1

        if show_team and not vm_df.empty:
            import plotly.express as px
            team_counts = vm_df["team_name"].value_counts().reset_index()
            team_counts.columns = ["Team", "VMs"]
            fig2 = px.bar(team_counts, x="Team", y="VMs",
                          color_discrete_sequence=["#2952d9"],
                          title="VMs per Team")
            fig2.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                               title_font_color="#1a3ab8", margin=dict(t=40,b=10,l=10,r=10))
            chart_cols[ci].plotly_chart(fig2, use_container_width=True)
            ci += 1

        if show_purpose and not vm_df.empty:
            import plotly.express as px
            purpose_counts = vm_df["purpose"].value_counts().reset_index()
            purpose_counts.columns = ["Purpose", "Count"]
            fig3 = px.pie(purpose_counts, names="Purpose", values="Count",
                          color_discrete_sequence=["#2952d9","#4f6ee8","#818cf8","#c7d2fe"],
                          title="VMs by Purpose")
            fig3.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                               title_font_color="#1a3ab8", margin=dict(t=40,b=10,r=10,l=10))
            chart_cols[ci].plotly_chart(fig3, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── 3. SUBNET BREAKDOWN ──
    if show_subnet:
        st.markdown("### 🌐 Subnet Breakdown")
        ip_df["Subnet"] = ip_df["ip_address"].apply(lambda x: ".".join(str(x).split(".")[:3]) + ".0/24")
        subnet_stats = ip_df.groupby("Subnet").agg(
            **{"Total IPs": ("ip_address","count"),
               "Used IPs":  ("ip_status", lambda x: (x=="assigned").sum()),
               "Free IPs":  ("ip_status", lambda x: (x=="free").sum())}
        ).reset_index()
        dl_subnet = subnet_stats.to_csv(index=False).encode("utf-8")
        sc1, sc2 = st.columns([9,1])
        with sc2:
            st.download_button("⬇ CSV", dl_subnet, "subnet_summary.csv", "text/csv", use_container_width=True)
        st.dataframe(subnet_stats, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── 4. HOST CAPACITY ──
    if show_host_cap:
        st.markdown("### 🖥️ Host Capacity Overview")
        vm_count_df = pd.read_sql("SELECT server_id, COUNT(*) as running_vms FROM vm_requests GROUP BY server_id", conn)
        servers_df["server_id"] = servers_df["server_id"].astype(str)
        vm_count_df["server_id"] = vm_count_df["server_id"].astype(str)
        cap_df = servers_df.merge(vm_count_df, on="server_id", how="left")
        cap_df["running_vms"] = cap_df["running_vms"].fillna(0).astype(int)
        dl_cap = cap_df.to_csv(index=False).encode("utf-8")
        hc1, hc2 = st.columns([9,1])
        with hc2:
            st.download_button("⬇ CSV", dl_cap, "host_capacity.csv", "text/csv", use_container_width=True)
        st.dataframe(cap_df[["host_ip","server_name","server_type","total_cpu","total_ram","total_storage","status","running_vms"]], use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── 5. IP RECORDS TABLE ──
    if show_ip_table:
        st.markdown("### 📋 IP Records")
        display_cols = selected_ip_cols if selected_ip_cols else all_ip_cols
        ip_table = ip_df[display_cols].rename(columns=col_labels).fillna("—")
        dl_ip = ip_table.to_csv(index=False).encode("utf-8")
        it1, it2 = st.columns([9,1])
        with it2:
            st.download_button("⬇ CSV", dl_ip, "ip_records.csv", "text/csv", use_container_width=True)
        st.dataframe(ip_table, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── 6. VM RECORDS TABLE ──
    if show_vm_table:
        st.markdown("### 🗃️ VM Records")
        dl_vm = vm_df.to_csv(index=False).encode("utf-8")
        vt1, vt2 = st.columns([9,1])
        with vt2:
            st.download_button("⬇ CSV", dl_vm, "vm_records.csv", "text/csv", use_container_width=True)
        st.dataframe(vm_df, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── 7. HOST RECORDS TABLE ──
    if show_host_table:
        st.markdown("### 🖥️ Host Records")
        dl_host = servers_df.to_csv(index=False).encode("utf-8")
        ht1, ht2 = st.columns([9,1])
        with ht2:
            st.download_button("⬇ CSV", dl_host, "host_records.csv", "text/csv", use_container_width=True)
        st.dataframe(servers_df, use_container_width=True)

# =====================================================
# IP AVAILABILITY PAGE
# =====================================================
elif st.session_state.page == "IP Availability":

    colb1, colb2 = st.columns([1,9])
    with colb1:
        if st.button("⬅ Home", key="back_home_ip"):
            st.session_state.page = "landing"
            st.rerun()

    st.title("IP Availability Grid")

    ip_data = pd.read_sql("""
    SELECT 
        ip_pool.ip_address,

        CASE 
            WHEN vm_requests.ip_address IS NULL THEN 'free'
            ELSE 'assigned'
        END AS ip_status,

        vm_requests.vm_name,
        vm_requests.team_name,
        vm_requests.server_id,
        vm_requests.cpu_required,
        vm_requests.ram_required,
        vm_requests.storage_required,
        vm_requests.purpose,
        servers.server_name,
        servers.host_ip

    FROM ip_pool

    LEFT JOIN vm_requests 
        ON ip_pool.ip_address = vm_requests.ip_address

    LEFT JOIN servers 
        ON vm_requests.server_id = servers.server_id

    ORDER BY ip_pool.ip_address
    """, conn)

    
    

    ip_data["ip_sort"] = ip_data["ip_address"].apply(lambda ip: int(ipaddress.IPv4Address(ip)))
    ip_data = ip_data.sort_values("ip_sort")
    ip_data = ip_data.drop(columns=["ip_sort"])
    ip_display = ip_data.rename(columns={
        "vm_name": "Owner",
        "host_ip": "Host IP",
        "team_name": "Team",
        "server_name": "Server",
        "cpu_required": "CPU",
        "ram_required": "RAM",
        "storage_required": "Disk",
        "purpose": "Purpose",
        "ip_address": "IP Address",
        "ip_status": "Status"
    })
    # ensure column exists
    ip_display = ip_display.fillna("—")
    ip_display.replace("None", "—", inplace=True)

    # Replace None explicitly
    ip_display["Host IP"] = ip_display["Host IP"].replace("None", "—")
    ip_display["Server"] = ip_display["Server"].replace("None", "—")

    total_ips = len(ip_display)
    free_ips = len(ip_display[ip_display["Status"] == "free"])
    used_ips = total_ips - free_ips

    st.markdown("### IP Pool Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total IPs", total_ips)
    c2.metric("Free IPs", free_ips)
    c3.metric("Assigned IPs", used_ips)
    st.markdown("<br>", unsafe_allow_html=True)
    # ---------------- SUBNET SUMMARY ----------------

    st.markdown("### Subnet Summary")

    # extract subnet (first 3 octets)
    ip_display["Subnet"] = ip_display["IP Address"].apply(lambda x: ".".join(str(x).split(".")[:3]) + ".0/24")

    subnet_stats = ip_display.groupby("Subnet").agg(
    **{"Total IPs": ("IP Address", "count"),
       "Used IPs": ("Status", lambda x: (x == "assigned").sum()),
       "Free IPs": ("Status", lambda x: (x == "free").sum())}
    ).reset_index()

    st.dataframe(subnet_stats, use_container_width=True)

    @st.dialog("Confirm IP Release")
    def confirm_delete_dialog(ip_address):
        st.markdown(f"### ⚠️ Release IP: `{ip_address}`")
        st.write("This will remove the VM assignment and return the IP to the pool.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, Release", use_container_width=True):
                cur = conn.cursor()
                cur.execute("DELETE FROM vm_requests WHERE ip_address=?", (ip_address,))
                cur.execute("UPDATE ip_pool SET ip_status='free' WHERE ip_address=?", (ip_address,))
                conn.commit()
                st.session_state.ip_deleted = True
                st.rerun()
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.rerun()

    rows_per_page = 10
    total_rows = len(ip_display)
    total_pages = max(1, (total_rows - 1) // rows_per_page + 1)
    if st.session_state.ip_page > total_pages:
        st.session_state.ip_page = total_pages
    start = (st.session_state.ip_page - 1) * rows_per_page
    end = start + rows_per_page
    page_df = ip_display.iloc[start:end]

    st.markdown("### IP Records")
    h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11 = st.columns([1.3,1.3,1.4,1.4,1,1,1.2,1.3,1.2,1,1.4])
    h1.markdown("**IP Address**")
    h2.markdown("**Host IP**")
    h3.markdown("**Owner**")
    h4.markdown("**Team**")
    h5.markdown("**CPU**")
    h6.markdown("**RAM**")
    h7.markdown("**Disk**")
    h8.markdown("**Purpose**")
    h9.markdown("**Server**")
    h10.markdown("**Status**")
    h11.markdown("**Actions**")
    st.markdown("---")

    for i, row in page_df.iterrows():
        c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11 = st.columns([1.3,1.3,1.4,1.4,1,1,1.2,1.3,1.2,1,1.4])
        c1.write(row["IP Address"])
        c2.write(row["Host IP"])
        c3.write(row["Owner"])
        c4.write(row["Team"])
        c5.write(row["CPU"])
        c6.write(row["RAM"])
        c7.write(row["Disk"])
        c8.write(row["Purpose"])
        c9.write(row["Server"])
        c10.write(row["Status"])
        with c11:
            a1, a2 = st.columns([1,1], gap="small")
            with a1:
                if st.button("✏️", key=f"edit_{i}"):
                    st.session_state.edit_ip = row["IP Address"]
                    st.session_state.open_host_drawer = False  # ← FIX
                    st.session_state.open_vm_drawer = False    # ← FIX
                    st.rerun()
            with a2:
                if st.button("🗑️", key=f"delete_{i}"):
                    confirm_delete_dialog(row["IP Address"])

    st.markdown("<br>", unsafe_allow_html=True)
    if "ip_deleted" in st.session_state:
        del st.session_state["ip_deleted"]
        st.rerun()

    left, mid, right = st.columns([2,11,1])
    with left:
        if st.button("⬅ Prev", disabled=st.session_state.ip_page == 1):
            st.session_state.ip_page -= 1
            st.rerun()
    with mid:
        st.markdown(f"<div style='text-align:center;font-weight:600;'>Page {st.session_state.ip_page} of {total_pages}</div>", unsafe_allow_html=True)
    with right:
        if st.button("Next ➡", disabled=st.session_state.ip_page >= total_pages):
            st.session_state.ip_page += 1
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# HOST GRID PAGE
# =====================================================
elif st.session_state.page == "Host Grid":

    colb1, colb2 = st.columns([1,9])
    with colb1:
        if st.button("⬅ Home", key="back_home_host"):
            st.session_state.page = "landing"
            st.session_state.open_host_drawer = False
            st.session_state.open_vm_drawer = False
            st.session_state.edit_host_id = None
            st.rerun()

    title_col, btn_col1, btn_col2, btn_col3 = st.columns([4,2,2,2])
    with title_col:
        st.title("Host Grid & VM Inventory")
    with btn_col1:
        st.write("")
        st.write("")
        if st.button("➕ New Host", use_container_width=True):
            st.session_state.open_host_drawer = True
            st.session_state.open_vm_drawer = False
            st.rerun()
    with btn_col2:
        st.write("")
        st.write("")
        if st.button("➕ New VM Request", use_container_width=True):
            st.session_state.open_vm_drawer = True
            st.session_state.open_host_drawer = False
            st.rerun()
    with btn_col3:
        st.write("")
        st.write("")
        if st.button("📂 Import Hosts CSV", use_container_width=True):
            st.session_state.show_host_csv = True
            st.rerun()

            # ── HOST CSV TEMPLATE ──
    host_template = """HOST IP,HOST NAME,SERVER TYPE,CPU,RAM(GB),STORAGE(GB)
192.168.1.10,Host-01,KVM,32,128,2000
192.168.1.11,Host-02,VMware,64,256,4000
"""
    if st.session_state.get("show_host_csv"):
        st.markdown("---")
        dl_col, _ = st.columns([2, 8])
        with dl_col:
            st.download_button("⬇ Download Host Template", host_template,
                               file_name="host_import_template.csv", mime="text/csv",
                               use_container_width=True)

        host_csv = st.file_uploader("Upload Hosts CSV", type=["csv"], key="host_csv_upload")

        if host_csv:
            df_hosts = pd.read_csv(host_csv, encoding="latin1")
            df_hosts.columns = df_hosts.columns.str.strip()

            required_host_cols = ["HOST IP", "HOST NAME", "SERVER TYPE", "CPU", "RAM(GB)", "STORAGE(GB)"]
            missing = [c for c in required_host_cols if c not in df_hosts.columns]
            if missing:
                st.error(f"❌ Missing columns: {', '.join(missing)}")
            else:
                st.info(f"📄 {host_csv.name} — {len(df_hosts)} rows detected. Click Import to confirm.")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Import Hosts", use_container_width=True, key="confirm_host_import"):
                        cur = conn.cursor()
                        added = 0
                        skipped = 0
                        for _, row in df_hosts.iterrows():
                            host_ip   = str(row["HOST IP"]).strip()
                            host_name = str(row["HOST NAME"]).strip()
                            srv_type  = str(row["SERVER TYPE"]).strip()
                            try: cpu = int(float(row["CPU"]))
                            except: cpu = 0
                            try: ram = int(float(row["RAM(GB)"]))
                            except: ram = 0
                            try: storage = int(float(row["STORAGE(GB)"]))
                            except: storage = 0

                            if not validate_ip(host_ip):
                                skipped += 1
                                continue

                            existing = cur.execute(
                                "SELECT server_id FROM servers WHERE host_ip=?", (host_ip,)
                            ).fetchone()

                            if existing:
                                cur.execute("""
                                    UPDATE servers SET server_name=?, server_type=?,
                                    total_cpu=?, total_ram=?, total_storage=?
                                    WHERE host_ip=?
                                """, (host_name, srv_type, cpu, ram, storage, host_ip))
                            else:
                                cur.execute("""
                                    INSERT INTO servers
                                    (host_ip, server_name, server_type, total_cpu, total_ram, total_storage, status)
                                    VALUES (?, ?, ?, ?, ?, ?, 'active')
                                """, (host_ip, host_name, srv_type, cpu, ram, storage))
                                added += 1

                        conn.commit()
                        st.session_state.show_host_csv = False
                        st.success(f"✅ Import done — {added} hosts added, {skipped} skipped (invalid IP).")
                        st.rerun()
                with c2:
                    if st.button("✖ Cancel", use_container_width=True, key="cancel_host_import"):
                        st.session_state.show_host_csv = False
                        st.rerun()
        else:
            if st.button("✖ Cancel", key="cancel_host_csv_empty"):
                st.session_state.show_host_csv = False
                st.rerun()
        st.markdown("---")

    # =====================================================
    # NEW HOST SIDEBAR
    # =====================================================
    if st.session_state.open_host_drawer:

        st.sidebar.markdown("## ➕ New Host")
        st.sidebar.markdown("---")

        new_host_ip   = st.sidebar.text_input("Host IP Address", placeholder="e.g. 192.168.1.20")
        new_host_name = st.sidebar.text_input("Host Name",       placeholder="e.g. Host-04")
        new_server_type = st.sidebar.selectbox("Server Type", ["KVM", "VMware", "Hypervisor", "Proxmox", "Other"])
        new_cpu     = st.sidebar.number_input("CPU Cores",    min_value=1,  max_value=512,    value=16)
        new_ram     = st.sidebar.number_input("RAM (GB)",     min_value=1,  max_value=4096,   value=64)
        new_ssd     = st.sidebar.number_input("SSD (GB)",     min_value=0,  max_value=100000, value=0)
        new_hdd     = st.sidebar.number_input("HDD (GB)",     min_value=0,  max_value=100000, value=500)
        new_storage = new_ssd + new_hdd
        st.sidebar.info(f"Total Storage: {new_storage} GB (SSD: {new_ssd} GB + HDD: {new_hdd} GB)")
        

        st.sidebar.markdown("---")
        sb1, sb2 = st.sidebar.columns(2)
        with sb1:
                if st.button("💾 Save Host", use_container_width=True, key="save_new_host"):

                    if not validate_ip(new_host_ip):
                        st.sidebar.error("Invalid Host IP address")
                        st.stop()

                    if not new_host_name.strip():
                        st.sidebar.error("Host name is required")
                        st.stop()

                    cur = conn.cursor()

                    cur.execute("""
                        INSERT INTO servers
                        (host_ip, server_name, server_type, total_cpu, total_ram, total_storage, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (new_host_ip.strip(), new_host_name.strip(), new_server_type, new_cpu, new_ram, new_storage, 'active'))

                    conn.commit()
                    st.sidebar.success(f"✅ Host '{new_host_name}' added!")
                    st.session_state.open_host_drawer = False
                    st.rerun()
        with sb2:
            if st.button("✖ Cancel", use_container_width=True, key="cancel_new_host"):
                st.session_state.open_host_drawer = False
                st.rerun()

    # =====================================================
    # CREATE VM SIDEBAR
    # =====================================================
    if st.session_state.open_vm_drawer:

        header_left, header_right = st.sidebar.columns([9,1])
        with header_left:
            st.sidebar.markdown("### Create VM Request")

        free_ips_df  = pd.read_sql("SELECT ip_address FROM ip_pool WHERE ip_status='free'", conn)
        servers_list = pd.read_sql("SELECT * FROM servers", conn)

        ip_choice  = st.sidebar.selectbox("VM IP Address", free_ips_df["ip_address"].tolist())
        owner_name = st.sidebar.text_input("Owner Name")
        team_name  = st.sidebar.text_input("Team Name")
        server_choice = st.sidebar.selectbox(
            "Server Name",
            options=servers_list["server_id"],
            format_func=lambda x: servers_list.loc[servers_list["server_id"] == x, "server_name"].values[0]
        )

        selected_server = servers_list.loc[servers_list["server_id"] == server_choice].iloc[0]
        total_cpu  = int(selected_server["total_cpu"])
        total_ram  = int(selected_server["total_ram"])
        total_disk = int(selected_server["total_storage"])

        used_resources = pd.read_sql("""
            SELECT COALESCE(SUM(cpu_required),0) AS used_cpu,
                   COALESCE(SUM(ram_required),0) AS used_ram,
                   COALESCE(SUM(storage_required),0) AS used_disk
            FROM vm_requests WHERE server_id=?
        """, conn, params=(server_choice,))

        used_cpu  = int(used_resources.iloc[0]["used_cpu"])
        used_ram  = int(used_resources.iloc[0]["used_ram"])
        used_disk = int(used_resources.iloc[0]["used_disk"])

        available_cpu  = max(total_cpu  - used_cpu,  512)   if total_cpu  == 0 else max(total_cpu  - used_cpu,  1)
        available_ram  = max(total_ram  - used_ram,  4096)  if total_ram  == 0 else max(total_ram  - used_ram,  1)
        available_disk = max(total_disk - used_disk, 100000) if total_disk == 0 else max(total_disk - used_disk, 10)

        st.sidebar.info(f"Available Resources:\nCPU: {available_cpu} cores\nRAM: {available_ram} GB\nDisk: {available_disk} GB")

        purpose = st.sidebar.selectbox("Purpose", ["Development","Testing","R&D"])
        cpu  = st.sidebar.number_input("CPU Cores", min_value=1,  max_value=available_cpu,  value=min(2, available_cpu))
        ram  = st.sidebar.number_input("RAM (GB)",  min_value=1,  max_value=available_ram,  value=min(4, available_ram))
        disk = st.sidebar.number_input("Disk (GB)", min_value=10, max_value=available_disk, value=min(50, available_disk))
        st.sidebar.markdown("---")
        btn_cols = st.sidebar.columns(2)
        with btn_cols[0]:
            if st.button("💾 Create", use_container_width=True, key="create_vm_btn"):
                confirm_vm_dialog(owner_name, team_name, server_choice, ip_choice, cpu, ram, disk, purpose)
        with btn_cols[1]:
            if st.button("✖ Cancel", use_container_width=True, key="cancel_vm_btn"):
                st.session_state.open_vm_drawer = False
                st.rerun()
    # =====================================================
    # SERVER CAPACITY TABLE
    # =====================================================
    st.markdown("---")
    st.subheader("Server Capacity Overview")

    vm_count = pd.read_sql(
    "SELECT server_id, COUNT(*) as running_vms FROM vm_requests GROUP BY server_id",
    conn
    )

    servers_df = pd.read_sql("SELECT * FROM servers", conn)

    # FIX TYPE MISMATCH
    servers_df["server_id"] = servers_df["server_id"].astype(str)
    vm_count["server_id"] = vm_count["server_id"].astype(str)

    capacity_df = servers_df.merge(vm_count, on="server_id", how="left")
    capacity_df["running_vms"] = capacity_df["running_vms"].fillna(0)

    if "edit_host_id" not in st.session_state:
        st.session_state.edit_host_id = None

    h1,h2,h3,h4,h5,h6,h7,h8,h9 = st.columns([1.5,1.5,1.5,1,1,1.5,1,1.2,1])
    h1.markdown("**Host IP**")
    h2.markdown("**Host Name**")
    h3.markdown("**Server Type**")
    h4.markdown("**CPU**")
    h5.markdown("**RAM (GB)**")
    h6.markdown("**Storage (GB)**")
    h7.markdown("**Status**")
    h8.markdown("**Running VMs**")
    h9.markdown("**Actions**")
    st.markdown("---")

    for i, row in capacity_df.iterrows():
        sid = int(row["server_id"])
        c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns([1.5,1.5,1.5,1,1,1.5,1,1.2,1])
        c1.write(row["host_ip"])
        c2.write(row["server_name"])
        c3.write(row["server_type"])
        c4.write(int(row["total_cpu"]))
        c5.write(int(row["total_ram"]))
        c6.write(int(row["total_storage"]))
        c7.write(row["status"])
        c8.write(int(row["running_vms"]))
        with c9:
            if st.button("✏️", key=f"edit_host_{sid}"):
                st.session_state.edit_host_id = sid
                st.session_state.open_host_drawer = False
                st.session_state.open_vm_drawer = False
                st.rerun()

    # ── HOST EDIT SIDEBAR ──
    if st.session_state.edit_host_id is not None:
        host_row = pd.read_sql(
            "SELECT * FROM servers WHERE server_id=?", conn,
            params=(st.session_state.edit_host_id,)
        )
        if len(host_row) > 0:
            hd = host_row.iloc[0]
            st.sidebar.title("✏️ Edit Host")
            st.sidebar.markdown(f"### {hd['server_name']}")
            st.sidebar.markdown("---")

            st.sidebar.text_input("Host IP", value=hd["host_ip"], disabled=True)
            new_name = st.sidebar.text_input("Host Name", value=hd["server_name"], key="eh_name")
            new_type = st.sidebar.selectbox("Server Type",
                ["KVM","VMware","Hypervisor","Proxmox","Unknown","Other"],
                index=["KVM","VMware","Hypervisor","Proxmox","Unknown","Other"].index(
                    hd["server_type"] if hd["server_type"] in
                    ["KVM","VMware","Hypervisor","Proxmox","Unknown","Other"] else "Unknown"
                ), key="eh_type")
            new_cpu  = st.sidebar.number_input("CPU Cores",    min_value=0, max_value=512,    value=int(hd["total_cpu"]),     key="eh_cpu")
            new_ram  = st.sidebar.number_input("RAM (GB)",     min_value=0, max_value=4096,   value=int(hd["total_ram"]),     key="eh_ram")
            new_disk = st.sidebar.number_input("Storage (GB)", min_value=0, max_value=100000, value=int(hd["total_storage"]), key="eh_disk")
            new_status = st.sidebar.selectbox("Status", ["active","inactive"],
                index=0 if hd["status"] == "active" else 1, key="eh_status")

            st.sidebar.markdown("---")
            sb1, sb2 = st.sidebar.columns(2)
            with sb1:
                if st.button("💾 Save", use_container_width=True, key="save_host_edit"):
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE servers
                        SET server_name=?, server_type=?, total_cpu=?,
                            total_ram=?, total_storage=?, status=?
                        WHERE server_id=?
                    """, (new_name, new_type, new_cpu, new_ram, new_disk,
                          new_status, st.session_state.edit_host_id))
                    conn.commit()
                    st.session_state.edit_host_id = None
                    st.rerun()
            with sb2:
                if st.button("✖ Cancel", use_container_width=True, key="cancel_host_edit"):
                    st.session_state.edit_host_id = None
                    st.rerun()

    edit_data = None
    if st.session_state.edit_vm_ip:
        df = pd.read_sql("SELECT * FROM vm_requests WHERE ip_address=?", conn, params=(st.session_state.edit_vm_ip,))
        if len(df) > 0:
            edit_data = df.iloc[0]

# =====================================================
# ← THIS IS THE BLOCK THAT WAS MISSING — ADDED BACK
# SIDEBAR EDIT PANEL (IP Availability edit button)
# =====================================================
if "edit_ip" in st.session_state and st.session_state.edit_ip is not None and st.session_state.page == "IP Availability":
    st.session_state.open_host_drawer = False
    st.session_state.open_vm_drawer = False

    ip_address = st.session_state.edit_ip

    # ---------------- FETCH DATA ----------------
    df = pd.read_sql("""
        SELECT ip_pool.ip_address, ip_pool.ip_status,
               vm_requests.vm_name, vm_requests.team_name,
               vm_requests.server_id, vm_requests.cpu_required,
               vm_requests.ram_required, vm_requests.storage_required,
               vm_requests.purpose
        FROM ip_pool
        LEFT JOIN vm_requests ON ip_pool.ip_address = vm_requests.ip_address
        WHERE ip_pool.ip_address=?
    """, conn, params=(ip_address,))

    if len(df) == 0:
        st.session_state.edit_ip = None
        st.rerun()

    data = df.iloc[0]

    if "edit_server" not in st.session_state and pd.notna(data["server_id"]):
        st.session_state.edit_server = int(data["server_id"])

    servers_list = pd.read_sql("SELECT server_id, server_name FROM servers", conn)
    server_ids   = list(servers_list["server_id"])

    if "edit_server" not in st.session_state:
        st.session_state.edit_server = server_ids[0]

    st.sidebar.title("Edit IP")
    st.sidebar.markdown(f"### {ip_address}")

    server_choice = st.sidebar.selectbox(
        "Server Name",
        options=server_ids,
        index=server_ids.index(st.session_state.edit_server),
        format_func=lambda x: servers_list.loc[servers_list["server_id"] == x, "server_name"].values[0],
        key="edit_server"
    )

    server_cap = pd.read_sql("SELECT total_cpu, total_ram, total_storage FROM servers WHERE server_id=?", conn, params=(server_choice,))
    total_cpu  = int(server_cap.iloc[0]["total_cpu"])
    total_ram  = int(server_cap.iloc[0]["total_ram"])
    total_disk = int(server_cap.iloc[0]["total_storage"])

    used = pd.read_sql("""
        SELECT COALESCE(SUM(cpu_required),0) AS used_cpu,
            COALESCE(SUM(ram_required),0) AS used_ram,
            COALESCE(SUM(storage_required),0) AS used_disk
        FROM vm_requests WHERE server_id=? AND ip_address != ?
    """, conn, params=(server_choice, ip_address))

    used_cpu  = int(used.iloc[0]["used_cpu"])
    used_ram  = int(used.iloc[0]["used_ram"])
    used_disk = int(used.iloc[0]["used_disk"])

    # current VM's own values — use as minimum ceiling if host has 0 total
    current_cpu  = int(data["cpu_required"])  if pd.notna(data["cpu_required"])  else 1
    current_ram  = int(data["ram_required"])  if pd.notna(data["ram_required"])  else 1
    current_disk = int(data["storage_required"]) if pd.notna(data["storage_required"]) else 10

    available_cpu  = max(total_cpu  - used_cpu,  current_cpu,  1)
    available_ram  = max(total_ram  - used_ram,  current_ram,  1)
    available_disk = max(total_disk - used_disk, current_disk, 10)

    st.sidebar.info(f"Available Resources:\nCPU: {available_cpu} cores\nRAM: {available_ram} GB\nDisk: {available_disk} GB")
    

    owner = st.sidebar.text_input("Owner Name",  value=data["vm_name"]    if pd.notna(data["vm_name"])    else "")
    team  = st.sidebar.text_input("Team Name",   value=data["team_name"]  if pd.notna(data["team_name"])  else "")

    if not owner.strip():
        st.sidebar.error("Owner name required")
        st.stop()

    if not team.strip():
        st.sidebar.error("Team name required")
        st.stop()

    purpose_options = ["Development", "Testing", "R&D"]
    purpose_idx = purpose_options.index(data["purpose"]) if pd.notna(data["purpose"]) and data["purpose"] in purpose_options else 0
    purpose = st.sidebar.selectbox("Purpose", purpose_options, index=purpose_idx)

    cpu = st.sidebar.number_input(
        "CPU Cores", min_value=1, max_value=int(available_cpu),
        value=min(int(data["cpu_required"]) if pd.notna(data["cpu_required"]) else 1, int(available_cpu))
    )
    ram = st.sidebar.number_input(
        "RAM (GB)", min_value=1, max_value=int(available_ram),
        value=min(int(data["ram_required"]) if pd.notna(data["ram_required"]) else 1, int(available_ram))  
    )

    disk_min = min(10, int(available_disk))
    disk_value = int(data["storage_required"]) if pd.notna(data["storage_required"]) else 10
    disk_value = max(disk_min, min(disk_value, int(available_disk)))
    disk = st.sidebar.number_input(
        "Disk (GB)", min_value=disk_min, max_value=int(available_disk), value=disk_value
    )

    status = st.sidebar.selectbox(
        "Status", ["free", "assigned"],
        index=0 if data["ip_status"] == "free" else 1
    )

    c1, c2 = st.sidebar.columns(2)

    with c1:
        if st.button("💾 Save", use_container_width=True):

            if not owner.strip():
                st.sidebar.error("Owner name required")
                st.stop()

            if not team.strip():
                st.sidebar.error("Team name required")
                st.stop()

            cur = conn.cursor()

            cur.execute("SELECT * FROM vm_requests WHERE ip_address=?", (ip_address,))
            existing = cur.fetchone()

            if existing:
                cur.execute("""
                    UPDATE vm_requests
                    SET vm_name=?, team_name=?, server_id=?, cpu_required=?, ram_required=?, storage_required=?, purpose=?
                    WHERE ip_address=?
                """, (owner, team, server_choice, cpu, ram, disk, purpose, ip_address))
            else:
                cur.execute("""
                    INSERT INTO vm_requests
                    (ip_address, vm_name, team_name, server_id, cpu_required, ram_required, storage_required, purpose)
                    VALUES(?,?,?,?,?,?,?,?)
                """, (ip_address, owner, team, server_choice, cpu, ram, disk, purpose))
 
            cur.execute("UPDATE ip_pool SET ip_status=? WHERE ip_address=?", (status, ip_address))
            conn.commit()

            st.session_state.edit_ip = None
            st.rerun()

    with c2:
        if st.button("Cancel", use_container_width=True):
            st.session_state.edit_ip = None
            if "edit_server" in st.session_state:
                del st.session_state.edit_server
            st.rerun()