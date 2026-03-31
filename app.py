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
   

# =====================================================
# SINGLE GLOBAL CSS BLOCK
# =====================================================
st.markdown("""
<style>

/* ── Dialog fixes ── */
button[aria-label="Close"] { display:none !important; }
div[role="dialog"] > div {
    background:#ffffff !important; border-radius:16px !important;
    border: none !important; box-shadow:0 8px 40px rgba(41,82,217,0.18) !important;
    padding:28px !important; max-height:80vh !important; overflow-y:auto !important;
}
div[role="dialog"] h2, div[role="dialog"] h3 { color:#1a2f6e !important; font-weight:700 !important; }
div[role="dialog"] p { color:#374151 !important; }
div[role="dialog"] code { background:#e8eeff !important; color:#1a3ab8 !important; padding:4px 8px; border-radius:6px; font-weight:600; }
div[role="dialog"] button:first-of-type { background:#e11d48 !important; color:white !important; border:none !important; border-radius:10px !important; }
div[role="dialog"] button:first-of-type:hover { background:#be123c !important; }
div[role="dialog"] button:last-of-type { background:#e8eeff !important; color:#1a2f6e !important; border:none !important; border-radius:10px !important; }
div[data-testid="stDialog"] { display:flex !important; align-items:center !important; justify-content:center !important; }
div[role="dialog"] { pointer-events:all !important; margin:auto !important; top:auto !important; }
div[role="dialog"] button { margin-top:12px !important; }
div[role="dialog"] div[data-testid="stHorizontalBlock"] { margin-top:18px !important; }
div[data-testid="stModal"] { position:fixed !important; inset:0 !important; display:flex !important; align-items:center !important; justify-content:center !important; padding:0 !important; margin:0 !important; }
div[data-testid="stModal"] > div { margin:0 auto !important; transform:none !important; }
div[data-testid="stModalBackdrop"] { position:fixed !important; inset:0 !important; background:rgba(26,58,184,0.3) !important; backdrop-filter:blur(4px) !important; }
body:has(div[data-testid="stModal"]) { overflow:hidden !important; }
[data-testid="stDialog"] { position:fixed !important; inset:0 !important; display:flex !important; align-items:center !important; justify-content:center !important; padding-top:0px !important; }
[data-testid="stDialog"] > div { margin-top:0px !important; }
[data-testid="stDialogOverlay"] { position:fixed !important; inset:0 !important; background:rgba(26,58,184,0.3) !important; backdrop-filter:blur(3px); }
div[data-testid="stDialog"], div[role="dialog"] { z-index:20000 !important; }
div[data-testid="stDialogOverlay"] { z-index:19999 !important; }

/* ── Layout & spacing ── */
.block-container { padding-top:0rem !important; padding-bottom:0rem !important; margin-top:0rem !important; }
.main .block-container { padding-top:0rem !important; margin-top:0rem !important; }
.stAppViewContainer { height:auto !important; }
[data-testid="column"] { align-self:flex-start !important; }
[data-testid="stVerticalBlock"] { padding-bottom:0rem !important; margin-bottom:0rem !important; }
div[data-testid="element-container"] { margin-bottom:0rem !important; border-top:none !important; }
div[data-testid="stAppViewContainer"] > section.main > div { padding-top:0rem !important; }
div[data-testid="stAppViewContainer"] > section { padding-top:0px !important; margin-top:0px !important; }
div[data-testid="stAppViewContainer"] { padding-top:0px !important; }
section[data-testid="stMain"] > div { padding-top:0rem !important; }
section[data-testid="stMain"] > div:first-child { border-top:none !important; box-shadow:none !important; padding-top:0 !important; }
section[data-testid="stMain"] { border-top:none !important; }
div[data-testid="block-container"]::before { display:none !important; content:none !important; background:none !important; height:0px !important; }
.main .block-container::before { display:none !important; }

/* ── Header/toolbar hide ── */
header[data-testid="stHeader"] { display:none !important; height:0px !important; min-height:0px !important; border-bottom:0px !important; box-shadow:none !important; }
div[data-testid="stToolbar"] { display:none !important; }
[data-testid="stDecoration"] { display:none !important; height:0px !important; }
div[data-testid="stDecoration"] { display:none !important; height:0px !important; }
hr { display:none !important; border:none !important; height:0px !important; margin:0px !important; }
[data-testid="stMarkdownContainer"] hr { display:none !important; }
a[href^="#"] { display:none !important; }
h1 > a, h2 > a, h3 > a { display:none !important; }
h1::after, h2::after, h3::after { display:none !important; content:none !important; }
:target { outline:none !important; border:none !important; }
:focus-visible { outline:none !important; }
button:focus, button:focus-visible { outline:none !important; box-shadow:none !important; }
div[data-testid="stHorizontalBlock"] { border:none !important; box-shadow:none !important; border-top:0px !important; }

/* ── App background ── */
.stApp { background: #f0f4ff !important; }

/* ── Global text ── */
html, body, [class*="css"] { color:#1a2f6e !important; }
h1, h2, h3, h4, h5, h6 { color:#1a2f6e !important; font-weight:700 !important; }
label { color:#1a3ab8 !important; font-weight:600 !important; }
input, textarea { color:#1a2f6e !important; }
div[data-baseweb="select"] div { color:#1a2f6e !important; }
::placeholder { color:#7a9acc !important; }
[data-testid="stHeader"] { background:transparent; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: white !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    box-shadow: 0 2px 12px rgba(41,82,217,0.10) !important;
    border: 1px solid #dce8ff !important;
}
[data-testid="stMetric"] > div { border:none !important; }
[data-testid="stMetricValue"] { color:#1a2f6e !important; font-weight:800 !important; font-size:2rem !important; }
[data-testid="stMetricLabel"] { color:#2952d9 !important; font-weight:600 !important; }
thead tr th { color:#1a2f6e !important; font-weight:700 !important; background:#e8eeff !important; }
tbody tr td { color:#1a2f6e !important; }

/* ── Page header band ── */
.page-header {
    background: linear-gradient(135deg, #2952d9 0%, #1a3ab8 100%);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    color: white;
}
.page-header h1 { color: white !important; font-size: 28px !important; margin: 0 !important; }
.page-header p  { color: rgba(255,255,255,0.85) !important; margin: 4px 0 0 0 !important; font-size: 14px !important; }

/* ── Section cards ── */
.section-card {
    background: white;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: 0 2px 12px rgba(41,82,217,0.08);
    border: 1px solid #dce8ff;
}
.section-card:hover {
    transform: translateY(-4px);
    transition: 0.25s ease;
}
.section-title {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #1a2f6e !important;
    margin-bottom: 14px !important;
    padding-bottom: 8px !important;
    border-bottom: 2px solid #e8eeff !important;
}

/* ── Buttons (global) ── */
div[data-testid="stButton"] > button {
    background: white !important;
    color: #1a2f6e !important;
    border-radius: 10px !important;
    border: 1.5px solid #b3c2e8 !important;
    font-weight: 600 !important;
    padding: 0.45rem 1.2rem !important;
    transition: 0.2s ease !important;
    font-size: 14px;
}
div[data-testid="stButton"] > button:hover {
    background: #e8eeff !important;
    border-color: #2952d9 !important;
    color: #2952d9 !important;
}
button p { color:#1a2f6e !important; font-weight:700 !important; }
button[kind="secondary"] p, button[kind="secondary"] span { color:#1a2f6e !important; font-weight:700 !important; }
.stButton button p, .stButton button span, .stButton button div { color:#1a2f6e !important; font-weight:700 !important; opacity:1 !important; }
button[data-testid="baseButton-primary"] { background:#2952d9 !important; color:white !important; border-radius:10px !important; border:none !important; font-weight:600 !important; }
button[data-testid="baseButton-primary"]:hover { background:#1a3ab8 !important; }
div[data-testid="stFormSubmitButton"] > button { background:#2952d9 !important; color:white !important; border-radius:10px !important; border:none !important; font-weight:600 !important; }
div[data-testid="stFormSubmitButton"] > button:hover { background:#1a3ab8 !important; }
div[data-testid="stDownloadButton"] > button { background:white !important; color:#1a2f6e !important; border-radius:10px !important; border:1.5px solid #b3c2e8 !important; font-weight:600 !important; padding:0.45rem 1.2rem !important; }
div[data-testid="stDownloadButton"] > button:hover { background:#e8eeff !important; border-color:#2952d9 !important; }

/* ── Back button special ── */
button[data-testid="baseButton-back_home_ip"],
button[data-testid="baseButton-back_home_host"],
button[data-testid="baseButton-back_home_dashboard"] {
    background: white !important;
    border: 1.5px solid #b3c2e8 !important;
    color: #1a2f6e !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ── Landing nav buttons ── */
button[data-testid="baseButton-go_dashboard"],
button[data-testid="baseButton-go_ip"],
button[data-testid="baseButton-go_host"] {
    color:#1a2f6e !important; height:220px !important; width:100% !important;
    border-radius:22px !important; background:#b3c2e8 !important;
    border:none !important;
    display:flex !important; flex-direction:column !important;
    align-items:center !important; justify-content:center !important;
    gap:14px; font-size:0px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
}
button[data-testid="baseButton-go_dashboard"]:hover,
button[data-testid="baseButton-go_ip"]:hover,
button[data-testid="baseButton-go_host"]:hover { background:#c5d0f0 !important; }
button[data-testid="baseButton-go_dashboard"] p:first-child,
button[data-testid="baseButton-go_ip"] p:first-child,
button[data-testid="baseButton-go_host"] p:first-child { font-size:70px !important; }
button[data-testid="baseButton-go_dashboard"] p:last-child,
button[data-testid="baseButton-go_ip"] p:last-child,
button[data-testid="baseButton-go_host"] p:last-child { font-size:24px !important; font-weight:600 !important; }
button[data-testid="baseButton-go_dashboard"] p,
button[data-testid="baseButton-go_ip"] p,
button[data-testid="baseButton-go_host"] p { color:#1a2f6e !important; font-weight:700 !important; }

/* ── Landing page ── */
.landing-title { text-align:center !important; font-size:48px !important; font-weight:700 !important; color:white !important; -webkit-text-fill-color:white !important; margin-bottom:8px; }
.landing-sub { text-align:center !important; font-size:16px !important; color:rgba(255,255,255,0.85) !important; margin-bottom:60px; }
.landing-wrapper { max-width:1000px; margin:auto; margin-top:0px; text-align:center; }
.action-row { display:flex; gap:6px; align-items:center; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    position:fixed !important; right:0 !important; left:auto !important;
    top:0 !important; height:100vh !important;
    width:620px !important; min-width:620px !important; max-width:620px !important;
    background: white !important;
    border-left: 2px solid #dce8ff !important;
    z-index:1000 !important;
}
section[data-testid="stSidebar"] > div:first-child {
    width:620px !important; padding:28px !important;
    display:flex !important; flex-direction:column !important; height:100vh !important; overflow-y:auto !important;
}
section[data-testid="stSidebarContent"] { padding-bottom:0px !important; }
section[data-testid="stSidebar"] div[data-testid="stSidebarHeader"] { display:none !important; height:0px !important; padding:0px !important; margin:0px !important; }
section[data-testid="stSidebar"] .block-container { padding-top:0px !important; margin-top:0px !important; flex-grow:1 !important; display:flex !important; flex-direction:column !important; }
section[data-testid="stSidebar"] div:first-child > div:first-child { margin-top:0px !important; padding-top:0px !important; }
section[data-testid="stSidebar"] button { height:42px !important; font-weight:600 !important; }
section[data-testid="stSidebar"] .stTextInput,
section[data-testid="stSidebar"] .stNumberInput,
section[data-testid="stSidebar"] .stSelectbox { width:100% !important; }
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
    flex-direction:row !important; display:flex !important; gap:10px !important; margin-bottom:0px !important;
}
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] > div { flex:1 !important; width:auto !important; }
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:last-of-type {
    margin-top:auto !important; position:sticky !important; bottom:0 !important;
    background:white !important; padding:16px 0 20px 0 !important;
    border-top:2px solid #dce8ff !important; z-index:10 !important;
}
section[data-testid="stSidebar"] .stButton button { margin-bottom:0px !important; }
button[data-testid="collapsedControl"] { display:none !important; }

/* ── Sidebar save button blue ── */
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:last-of-type button:first-child {
    background: #2952d9 !important; color: white !important; border: none !important;
}
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:last-of-type button:first-child:hover {
    background: #1a3ab8 !important;
}
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:last-of-type button p {
    color: inherit !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden !important; border: 1px solid #dce8ff !important; }

/* ── Expander ── */
[data-testid="stExpander"] { border: 1.5px solid #dce8ff !important; border-radius: 12px !important; background: white !important; }
[data-testid="stExpanderToggleIcon"] { color: #2952d9 !important; }

/* ── CSV Import Page ── */
.csv-import-page {
    min-height: 100vh;
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
}

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
    * { font-family:'Inter', sans-serif; box-sizing:border-box; }
    #MainMenu, header, footer { visibility:hidden; }
    .block-container { padding:0 !important; max-width:100% !important; }
    .stApp { background:transparent !important; }
    .bg { position:fixed; inset:0; display:flex; z-index:0; }
    .bg-left { width:45%; background:linear-gradient(145deg,#2952d9 0%,#1a3ab8 60%,#122a8a 100%); }
    .bg-right { width:55%; background:#eaeef5; }
    .left-brand { position:fixed; top:50%; left:22.5%; transform:translate(-50%,-50%); color:white; z-index:5; pointer-events:none; }
    .left-brand h1 { font-size:44px; font-weight:800; margin:0 0 14px 0; line-height:1.15; color:white !important; -webkit-text-fill-color:white !important; }
    .left-brand p  { font-size:18px; margin:5px 0; opacity:0.9; color:white !important; }
    [data-testid="stForm"] {
        position:fixed !important; top:50% !important; left:72.5% !important;
        transform:translate(-50%,-50%) !important; width:400px !important;
        background:white !important; padding:50px 44px !important;
        border-radius:20px !important; box-shadow:0 20px 70px rgba(0,0,0,0.13) !important;
        border:none !important; z-index:10 !important; height:auto !important;
        max-height:none !important; overflow:visible !important;
    }
    [data-testid="stForm"] h3 { font-size:28px !important; font-weight:700 !important; color:#1a2f6e !important; text-align:center !important; margin-bottom:28px !important; }
    [data-testid="stForm"] label p { font-size:14px !important; font-weight:600 !important; color:#374151 !important; }
    [data-testid="stForm"] [data-baseweb="input"] { border:1.5px solid #d1d5db !important; border-radius:10px !important; box-shadow:none !important; }
    [data-testid="stForm"] [data-baseweb="input"]:focus-within { border:1.5px solid #2952d9 !important; box-shadow:none !important; }
    [data-testid="stForm"] input { height:48px !important; font-size:15px !important; background:white !important; color:#111 !important; border:none !important; box-shadow:none !important; outline:none !important; }
    [data-testid="stForm"] button, [data-testid="stForm"] .stFormSubmitButton button {
        height:50px !important; border-radius:12px !important;
        background:linear-gradient(90deg,#2563eb,#1d4ed8) !important;
        color:white !important; font-weight:700 !important; font-size:16px !important;
        border:none !important; width:100% !important; letter-spacing:0.3px !important; margin-top:6px !important;
    }
    [data-testid="stForm"] button:hover { opacity:0.9 !important; }
    [data-testid="stForm"] > div { border:none !important; }
    [data-testid="stForm"] button[aria-label="Show password text"],
    [data-testid="stForm"] button[aria-label="Hide password text"],
    [data-testid="stForm"] [data-testid="stTextInput"] button {
        background:transparent !important; background-image:none !important;
        border:none !important; box-shadow:none !important;
        width:36px !important; height:36px !important; min-height:unset !important;
        padding:4px !important; margin:0 !important; color:#6b7280 !important;
    }
    [data-testid="stForm"] [data-testid="stTextInput"] button:hover { background:#f3f4f6 !important; opacity:1 !important; transform:none !important; }
    [data-testid="stForm"] [data-testid="stTextInput"] button svg { width:18px !important; height:18px !important; }
    [data-testid="InputInstructions"] { display:none !important; }
    section[data-testid="stSidebar"] { display:none; }
    .stMainBlockContainer, [data-testid="stMainBlockContainer"] { padding:0 !important; margin:0 !important; }
    </style>
    <div class="bg"><div class="bg-left"></div><div class="bg-right"></div></div>
    <div class="left-brand"><h1>EverestIMS IT</h1><p>Authorized Access Only</p></div>
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
                    st.session_state.logged_in_user = email
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password.")
    st.stop()

# =====================================================
# SMART CSV IMPORT FUNCTION
# =====================================================
def import_csv_data(df, conn):
    import_conn = conn
    cur = import_conn.cursor()
    ip_count = 0; server_count = 0; vm_count_inserted = 0; filled_count = 0
    df.columns = df.columns.str.strip()
    df = df.rename(columns={
        "IP":"ip_address","HOST":"host_ip","TEAM NAME":"team_name","USER NAME":"vm_name",
        "CPU":"cpu_required","RAM(GB)":"ram_required","Disk(GB)":"storage_required",
        "VM Status":"vm_status","STATUS":"status"
    })
    if "ip_address" in df.columns:
        valid_ips = df["ip_address"].dropna().astype(str) 
        valid_ips = valid_ips[valid_ips.str.match(r'^\d+\.\d+\.\d+\.\d+$')]
        csv_ips = valid_ips.tolist()
        for ip in csv_ips:
            if not validate_ip(ip): continue
            ip = str(ip).strip()
            existing = cur.execute("SELECT ip_address FROM ip_pool WHERE ip_address=?", (ip,)).fetchone()
            if not existing:
                cur.execute("INSERT OR IGNORE INTO ip_pool (ip_address, ip_status) VALUES (?, 'free')", (ip,))
                ip_count += 1
                if ip_count % 50 == 0: import_conn.commit()
        if csv_ips:
            try:
                ip_objects = sorted([ipaddress.IPv4Address(str(ip).strip()) for ip in csv_ips])
                full_range = [str(ipaddress.IPv4Address(i)) for i in range(int(ip_objects[0]), int(ip_objects[-1]) + 1)]
                csv_ip_set = set(str(ip) for ip in ip_objects)
                for ip in full_range:
                    if ip not in csv_ip_set:
                        existing = cur.execute("SELECT ip_address FROM ip_pool WHERE ip_address=?", (ip,)).fetchone()
                        if not existing:
                            cur.execute("INSERT OR IGNORE INTO ip_pool (ip_address, ip_status) VALUES (?, 'free')", (ip,))
                            filled_count += 1
            except Exception: pass
    if "host_ip" in df.columns:
        valid_hosts = df["host_ip"].dropna().astype(str)
        valid_hosts = valid_hosts[valid_hosts.str.match(r'^\d+\.\d+\.\d+\.\d+$')]
        for host_ip in valid_hosts.unique():
            host_ip = str(host_ip).strip()
            existing = cur.execute("SELECT server_id FROM servers WHERE host_ip=?", (host_ip,)).fetchone()
            if not existing:
                count = cur.execute("SELECT COUNT(*) FROM servers").fetchone()[0]
                auto_name = f"Host-{str(count+1).zfill(2)}"
                cur.execute("INSERT INTO servers (host_ip,server_name,server_type,total_cpu,total_ram,total_storage,status) VALUES (?,?,'Unknown',0,0,0,'active')", (host_ip,auto_name))
                server_count += 1
    import_conn.commit()
    if "vm_name" in df.columns:
        for row in df.itertuples(index=False):
            vm_name=str(getattr(row,"vm_name","")).strip(); team_name=str(getattr(row,"team_name","")).strip()
            ip=str(getattr(row,"ip_address","")).strip(); host_ip=str(getattr(row,"host_ip","")).strip()
            cpu=getattr(row,"cpu_required",0); ram=getattr(row,"ram_required",0); disk=getattr(row,"storage_required",0)
            try: cpu=int(float(cpu))
            except: cpu=0
            try: ram=int(float(ram))
            except: ram=0
            try: disk=int(float(disk))
            except: disk=0
            if not vm_name or vm_name.lower()=="nan": continue
            server_id=None
            if host_ip and re.match(r'^\d+\.\d+\.\d+\.\d+$',host_ip):
                server=cur.execute("SELECT server_id FROM servers WHERE host_ip=?",(host_ip,)).fetchone()
                if server: server_id=server[0]
            existing=cur.execute("SELECT vm_name FROM vm_requests WHERE vm_name=?",(vm_name,)).fetchone()
            if not existing:
                purpose_val=str(getattr(row,"purpose","Development")).strip()
                purpose=purpose_val if purpose_val in ["Development","Testing","R&D"] else "Development"
                cur.execute("INSERT INTO vm_requests (vm_name,team_name,server_id,ip_address,cpu_required,ram_required,storage_required,purpose,approval_status) VALUES (?,?,?,?,?,?,?,?,'Pending')",(vm_name,team_name,server_id,ip,cpu,ram,disk,purpose))
                vm_count_inserted+=1
                if ip and validate_ip(ip):
                    cur.execute("UPDATE ip_pool SET ip_status='assigned' WHERE ip_address=?",(ip,))
    import_conn.commit()
    return ip_count,server_count,vm_count_inserted,filled_count


def go(page_name):
    st.session_state["page"] = page_name
    st.rerun()

# ----------- DB -----------
conn = sqlite3.connect("infra.db", check_same_thread=False, timeout=60)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA busy_timeout=60000")
servers = pd.read_sql("SELECT * FROM servers", conn)

# -- Audit log table --
conn.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp   TEXT    NOT NULL,
        user        TEXT    NOT NULL,
        action      TEXT    NOT NULL,
        resource    TEXT    NOT NULL,
        resource_id TEXT,
        details     TEXT,
        status      TEXT    DEFAULT 'success'
    )
""")
conn.commit()

def log_action(action, resource, resource_id="", details="", status="success"):
    import datetime
    user = st.session_state.get("logged_in_user", "system")
    ts   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO audit_log (timestamp,user,action,resource,resource_id,details,status) VALUES (?,?,?,?,?,?,?)",
        (ts, user, action, resource, str(resource_id), str(details), status)
    )
    conn.commit()

def check_server_capacity(server_id, cpu_req, ram_req, disk_req):
    cur = conn.cursor()
    total = cur.execute("SELECT total_cpu,total_ram,total_storage FROM servers WHERE server_id=?", (server_id,)).fetchone()
    used  = cur.execute("SELECT COALESCE(SUM(cpu_required),0),COALESCE(SUM(ram_required),0),COALESCE(SUM(storage_required),0) FROM vm_requests WHERE server_id=?", (server_id,)).fetchone()
    if cpu_req  > total[0]-used[0]: return False,f"Only {total[0]-used[0]} CPU cores available"
    if ram_req  > total[1]-used[1]: return False,f"Only {total[1]-used[1]} GB RAM available"
    if disk_req > total[2]-used[2]: return False,f"Only {total[2]-used[2]} GB storage available"
    return True,"OK"

# =====================================================
# SHARED VM DRAWER FUNCTION
# =====================================================
def get_best_server(cpu_req, ram_req, disk_req):
    servers = pd.read_sql("SELECT * FROM servers", conn)
    best_server = None
    best_score = 999999
    for _, server in servers.iterrows():
        server_id = server["server_id"]
        used = pd.read_sql("""
            SELECT 
                COALESCE(SUM(cpu_required),0) as used_cpu,
                COALESCE(SUM(ram_required),0) as used_ram,
                COALESCE(SUM(storage_required),0) as used_disk
            FROM vm_requests
            WHERE server_id=?
        """, conn, params=(server_id,))
        used_cpu = int(used.iloc[0]["used_cpu"])
        used_ram = int(used.iloc[0]["used_ram"])
        used_disk = int(used.iloc[0]["used_disk"])
        total_cpu = int(server["total_cpu"])
        total_ram = int(server["total_ram"])
        total_disk = int(server["total_storage"])
        avail_cpu = total_cpu - used_cpu
        avail_ram = total_ram - used_ram
        avail_disk = total_disk - used_disk
        if avail_cpu >= cpu_req and avail_ram >= ram_req and avail_disk >= disk_req:
            cpu_usage = (used_cpu / total_cpu) if total_cpu > 0 else 1
            ram_usage = (used_ram / total_ram) if total_ram > 0 else 1
            disk_usage = (used_disk / total_disk) if total_disk > 0 else 1
            avg_usage = (cpu_usage + ram_usage + disk_usage) / 3
            if avg_usage < best_score:
                best_score = avg_usage
                best_server = server_id
    return best_server

def render_vm_drawer():
    if not st.session_state.get("open_vm_drawer"):
        return
    st.sidebar.markdown("### Create VM Request")
    free_ips_df  = pd.read_sql("SELECT ip_address FROM ip_pool WHERE ip_status='free'", conn)
    servers_list = pd.read_sql("SELECT * FROM servers", conn)
    ip_choice    = st.sidebar.selectbox("VM IP Address", free_ips_df["ip_address"].tolist())
    owner_name   = st.sidebar.text_input("Owner Name")
    team_name    = st.sidebar.text_input("Team Name")
    auto_mode = st.sidebar.checkbox("🤖 Auto Select Best Server", value=True)

    if auto_mode:
        cpu_input = st.sidebar.number_input("CPU Cores", min_value=1, value=2)
        ram_input = st.sidebar.number_input("RAM (GB)", min_value=1, value=4)
        disk_input = st.sidebar.number_input("Disk (GB)", min_value=10, value=50)
        best_server = get_best_server(cpu_input, ram_input, disk_input)
        if best_server:
            server_choice = best_server
            server_name = servers_list.loc[
                servers_list["server_id"] == server_choice, "server_name"
            ].values[0]
            st.sidebar.success(f"✅ Auto Selected: {server_name}")
        else:
            st.sidebar.error("❌ No server available")
            return
        cpu = cpu_input
        ram = ram_input
        disk = disk_input
    else:
        server_choice = st.sidebar.selectbox(
            "Server Name",
            options=servers_list["server_id"],
            format_func=lambda x: servers_list.loc[servers_list["server_id"]==x,"server_name"].values[0]
        )
        cpu  = st.sidebar.number_input("CPU Cores", min_value=1, value=2)
        ram  = st.sidebar.number_input("RAM (GB)", min_value=1, value=4)
        disk = st.sidebar.number_input("Disk (GB)", min_value=10, value=50)

    selected_server = servers_list.loc[servers_list["server_id"]==server_choice].iloc[0]
    total_cpu  = int(selected_server["total_cpu"])
    total_ram  = int(selected_server["total_ram"])
    total_disk = int(selected_server["total_storage"])
    used_resources = pd.read_sql(
        "SELECT COALESCE(SUM(cpu_required),0) AS used_cpu,COALESCE(SUM(ram_required),0) AS used_ram,COALESCE(SUM(storage_required),0) AS used_disk FROM vm_requests WHERE server_id=?",
        conn, params=(server_choice,)
    )
    used_cpu  = int(used_resources.iloc[0]["used_cpu"])
    used_ram  = int(used_resources.iloc[0]["used_ram"])
    used_disk = int(used_resources.iloc[0]["used_disk"])
    available_cpu  = max(total_cpu  - used_cpu,  1)
    available_ram  = max(total_ram  - used_ram,  1)
    available_disk = max(total_disk - used_disk, 10)
    used_pct_cpu  = round((used_cpu  / total_cpu  * 100), 1) if total_cpu  > 0 else 0
    used_pct_ram  = round((used_ram  / total_ram  * 100), 1) if total_ram  > 0 else 0
    used_pct_disk = round((used_disk / total_disk * 100), 1) if total_disk > 0 else 0
    bar_cpu  = min(int(used_pct_cpu),  100)
    bar_ram  = min(int(used_pct_ram),  100)
    bar_disk = min(int(used_pct_disk), 100)
    col_cpu  = '#e11d48' if bar_cpu  > 85 else '#f59e0b' if bar_cpu  > 60 else '#2952d9'
    col_ram  = '#e11d48' if bar_ram  > 85 else '#f59e0b' if bar_ram  > 60 else '#2952d9'
    col_disk = '#e11d48' if bar_disk > 85 else '#f59e0b' if bar_disk > 60 else '#2952d9'
    st.sidebar.markdown(f"""
<div style="background:#f0f4ff;border-radius:10px;padding:14px 16px;border:1px solid #dce8ff;margin:8px 0;">
<p style="font-weight:700;color:#1a2f6e;margin:0 0 10px 0;">📊 Server Resource Usage</p>
<p style="font-size:13px;color:#1a2f6e;font-weight:600;margin:0 0 4px 0;">🖥️ vCPU &nbsp;&nbsp; {used_cpu} / {total_cpu} cores ({'⚠️ Over!' if used_pct_cpu > 100 else str(used_pct_cpu)+'%'})</p>
<table width="100%" cellspacing="0" cellpadding="0"><tr>
<td width="{bar_cpu}%" style="background:{col_cpu};height:8px;border-radius:4px 0 0 4px;"></td>
<td width="{100-bar_cpu}%" style="background:#dce8ff;height:8px;border-radius:0 4px 4px 0;"></td>
</tr></table>
<p style="font-size:13px;color:#1a2f6e;font-weight:600;margin:10px 0 4px 0;">💾 RAM &nbsp;&nbsp; {used_ram} / {total_ram} GB ({'⚠️ Over!' if used_pct_ram > 100 else str(used_pct_ram)+'%'})</p>
<table width="100%" cellspacing="0" cellpadding="0"><tr>
<td width="{bar_ram}%" style="background:{col_ram};height:8px;border-radius:4px 0 0 4px;"></td>
<td width="{100-bar_ram}%" style="background:#dce8ff;height:8px;border-radius:0 4px 4px 0;"></td>
</tr></table>
<p style="font-size:13px;color:#1a2f6e;font-weight:600;margin:10px 0 4px 0;">💿 Disk &nbsp;&nbsp; {used_disk} / {total_disk} GB ({'⚠️ Over!' if used_pct_disk > 100 else str(used_pct_disk)+'%'})</p>
<table width="100%" cellspacing="0" cellpadding="0"><tr>
<td width="{bar_disk}%" style="background:{col_disk};height:8px;border-radius:4px 0 0 4px;"></td>
<td width="{100-bar_disk}%" style="background:#dce8ff;height:8px;border-radius:0 4px 4px 0;"></td>
</tr></table>
<p style="font-size:12px;color:#2952d9;font-weight:600;margin:10px 0 0 0;">✅ Available — CPU: {available_cpu} | RAM: {available_ram} GB | Disk: {available_disk} GB</p>
</div>""", unsafe_allow_html=True)
    purpose = st.sidebar.selectbox("Purpose", ["Development","Testing","R&D"])
    cpu  = st.sidebar.number_input("CPU Cores", min_value=1,  max_value=available_cpu,  value=min(2,  available_cpu))
    ram  = st.sidebar.number_input("RAM (GB)",  min_value=1,  max_value=available_ram,  value=min(4,  available_ram))
    disk = st.sidebar.number_input("Disk (GB)", min_value=10, max_value=available_disk, value=min(50, available_disk))
    st.sidebar.markdown("---")
    btn_cols = st.sidebar.columns(2)
    with btn_cols[0]:
        if st.button("💾 Create", use_container_width=True, key="create_vm_btn"):
            confirm_vm_dialog(owner_name, team_name, server_choice, ip_choice, cpu, ram, disk, purpose)
    with btn_cols[1]:
        if st.button("✖ Cancel", use_container_width=True, key="cancel_vm_btn"):
            st.session_state.open_vm_drawer = False; st.rerun()


for key,default in [
    ("editing_ip",None),("form_reset",0),("form_id",0),("show_form",False),
    ("edit_vm_ip",None),("ip_page",1),("open_host_drawer",False),
    ("open_vm_drawer",False),("show_host_csv",False),("confirm_vm_create",False),
    ("edit_ip_open",False),("edit_ip_data",None),("page","landing"),
    ("show_ip_records",False),("show_csv_uploader",False)
]:
    if key not in st.session_state: st.session_state[key]=default

_has_sidebar = (
    st.session_state.get("open_host_drawer") or
    st.session_state.get("open_vm_drawer") or
    st.session_state.get("edit_host_id") is not None or
    (st.session_state.get("edit_ip") is not None and st.session_state.get("page")=="IP Availability")
)
if _has_sidebar:
    st.markdown("""<style>div[data-testid="stAppViewContainer"] > section.main { margin-right:620px !important; }</style>""", unsafe_allow_html=True)

@st.dialog("Confirm VM Creation")
def confirm_vm_dialog(owner_name,team_name,server_choice,ip_choice,cpu,ram,disk,purpose):
    st.markdown("### ⚠️ Are you sure you want to create this VM?")
    st.write(f"**IP:** {ip_choice}")
    st.write(f"**CPU:** {cpu} cores | **RAM:** {ram} GB | **Disk:** {disk} GB")
    col1,col2=st.columns(2)
    with col1:
        if st.button("✅ Yes, Create",use_container_width=True):
            cur=conn.cursor()
            cur.execute("INSERT INTO vm_requests (vm_name,team_name,server_id,ip_address,cpu_required,ram_required,storage_required,purpose,approval_status) VALUES(?,?,?,?,?,?,?,?,?)",(owner_name,team_name,server_choice,ip_choice,cpu,ram,disk,purpose,"Pending"))
            cur.execute("UPDATE ip_pool SET ip_status='assigned' WHERE ip_address=?",(ip_choice,))
            conn.commit()
            log_action("CREATE_VM", "VM", resource_id=ip_choice,
                       details=f"Owner: {owner_name} | Team: {team_name} | CPU: {cpu} | RAM: {ram}GB | Disk: {disk}GB | Purpose: {purpose}")
            st.session_state.open_vm_drawer=False; st.rerun()
    with col2:
        if st.button("❌ Cancel",use_container_width=True): st.rerun()

# =====================================================
# CSV IMPORT DIALOG (popup)
# =====================================================
@st.dialog("📂 Import CSV")
def csv_import_dialog():
    template = "IP,HOST,TEAM NAME,USER NAME,CPU,RAM(GB),Disk(GB),VM Status,STATUS,PURPOSE\n10.0.4.1,10.0.0.1,DevOps,vm_dev_01,2,4,50,Running,assigned,Development\n10.0.4.2,10.0.0.1,QA,vm_test_01,2,4,50,Running,assigned,Testing\n10.0.4.3,10.0.0.1,Research,vm_rnd_01,4,8,100,Running,assigned,R&D\n"

    st.markdown("""
    <style>
    div[role="dialog"] > div { max-width: 560px !important; width: 560px !important; }
    div[role="dialog"] button:first-of-type { background: white !important; color: #1a2f6e !important; border: 1.5px solid #b3c2e8 !important; }
    div[role="dialog"] button:last-of-type { background: white !important; color: #1a2f6e !important; border: 1.5px solid #b3c2e8 !important; }
    div[data-testid="stDownloadButton"] > button { background: #f0f4ff !important; color: #2952d9 !important; border: 1.5px solid #b3c2e8 !important; border-radius: 10px !important; font-weight: 600 !important; height: 40px !important; }
    div[data-testid="stDownloadButton"] > button p { color: #2952d9 !important; }
    [data-testid="stFileUploader"] { background: #f8faff !important; border-radius: 12px !important; }
    [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] small, [data-testid="stFileUploader"] label { color: #1a2f6e !important; font-weight: 600 !important; }
    [data-testid="stFileUploader"] button { background: white !important; color: #1a2f6e !important; border: 1.5px solid #b3c2e8 !important; border-radius: 8px !important; font-weight: 600 !important; height: auto !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#6b7280;font-size:14px;margin:0 0 16px 0;'>Upload your infrastructure CSV. Download the template if needed.</p>", unsafe_allow_html=True)

    st.download_button(
        "⬇️ Download CSV Template", template,
        file_name="vm_import_template.csv", mime="text/csv",
        use_container_width=True
    )
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    csv_file = st.file_uploader("Upload CSV File", type=["csv"], key="landing_csv")

    if csv_file:
        df_preview = pd.read_csv(csv_file, encoding='latin1')
        required_columns = ["IP","HOST","TEAM NAME","USER NAME","CPU","RAM(GB)","Disk(GB)","VM Status","STATUS"]
        missing_cols = [col for col in required_columns if col not in df_preview.columns]
        if missing_cols:
            st.error(f"❌ Missing columns: {', '.join(missing_cols)}")
        else:
            st.markdown(f"""
            <div style="background:#f0f4ff;border-radius:10px;padding:10px 14px;
                border:1px solid #dce8ff;margin:10px 0;display:flex;align-items:center;gap:10px;">
                <span style="font-size:18px;">📄</span>
                <div>
                    <p style="color:#1a2f6e;font-weight:700;margin:0;font-size:13px;">{csv_file.name}</p>
                    <p style="color:#6b7280;font-size:12px;margin:2px 0 0 0;">{len(df_preview)} rows detected</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Import", use_container_width=True, key="confirm_import"):
                    with st.spinner("Importing..."):
                        ip_count, server_count, vm_count, filled_count = import_csv_data(df_preview, conn)
                    log_action("CSV_IMPORT", "BULK", details=f"File: {csv_file.name} | IPs: {ip_count}, Servers: {server_count}, VMs: {vm_count}")
                    st.session_state.show_csv_uploader = False
                    st.success(f"✅ Done — {ip_count} IPs, {server_count} Servers, {vm_count} VMs added.")
                    st.rerun()
            with c2:
                if st.button("✖ Cancel", use_container_width=True, key="cancel_import"):
                    st.session_state.show_csv_uploader = False
                    st.rerun()
    else:
        if st.button("✖ Cancel", key="cancel_import_empty", use_container_width=True):
            st.session_state.show_csv_uploader = False
            st.rerun()

if st.session_state.get("show_csv_uploader"):
    csv_import_dialog()

# =====================================================
# LANDING PAGE
# =====================================================
if st.session_state.page=="landing":
    st.markdown("""
        <div style="position:fixed;top:12px;right:16px;z-index:99999;">
            <a href="?logout=true" target="_self">
                <button style="background:#b3c2e8;color:#1a2f6e;border:none;border-radius:12px;font-weight:700;padding:8px 20px;cursor:pointer;font-size:14px;box-shadow:0 2px 8px rgba(0,0,0,0.08);">🔓 Logout</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

    if st.query_params.get("logout")=="true":
        st.session_state.logged_in=False; st.session_state.page="landing"
        st.query_params.clear(); st.rerun()

    st.markdown("""<style>
    section[data-testid="stMain"] { background:linear-gradient(145deg,#2952d9 0%,#1a3ab8 60%,#122a8a 100%) !important; min-height:100vh !important; }
    .stApp { background:linear-gradient(145deg,#2952d9 0%,#1a3ab8 60%,#122a8a 100%) !important; }
    div[data-testid="stButton"] > button { background:#b3c2e8 !important; color:#1a2f6e !important; border:none !important; border-radius:20px !important; box-shadow:0 2px 8px rgba(0,0,0,0.08) !important; font-weight:700 !important; height:130px !important; font-size:16px !important; }
    div[data-testid="stButton"] > button:hover { background:#c5d0f0 !important; }
    button p { color:#1a2f6e !important; font-weight:700 !important; }
    </style>""", unsafe_allow_html=True)

    st.markdown('<div class="landing-title"> IP Management Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="landing-sub">Server & VM Management System</div>', unsafe_allow_html=True)

    _,center_col,_=st.columns([3,2,3])
    with center_col:
        if st.button("📂  Import CSV", use_container_width=True):
            st.session_state.show_csv_uploader = True
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col1,col2,col3,col4=st.columns(4,gap="large")
    with col1:
        if st.button("📊\nDashboard",key="go_dashboard",use_container_width=True): go("Home")
    with col2:
        if st.button("🌐\nIP Availability",key="go_ip",use_container_width=True): go("IP Availability")
    with col3:
        if st.button("🖥️\nHost Grid",key="go_host",use_container_width=True): go("Host Grid")
    with col4:
        if st.button("📋\nAudit Log",key="go_audit",use_container_width=True): go("Audit Log")

    st.markdown("""<div style="position:fixed;bottom:20px;left:0;right:0;text-align:center;color:rgba(255,255,255,0.85);font-size:20px;font-weight:700;letter-spacing:1px;">© 2026 Infraon IT</div>""", unsafe_allow_html=True)

# =====================================================
# HOME PAGE
# =====================================================
elif st.session_state.page=="Home":

    colb1,colb2=st.columns([1,9])
    with colb1:
        if st.button("⬅ Home",key="back_home_dashboard"):
            st.session_state.page="landing"; st.rerun()

    st.markdown("""
    <div class="page-header">
        <h1>📊 Infrastructure Dashboard</h1>
        <p>Monitor and manage your infrastructure in real-time</p>
    </div>
    """, unsafe_allow_html=True)

    import plotly.express as px

    # ================= DATA =================
    ip_df=pd.read_sql("""
        SELECT ip_pool.ip_address,
               CASE WHEN vm_requests.ip_address IS NULL THEN 'free' ELSE 'assigned' END AS ip_status,
               vm_requests.vm_name,vm_requests.team_name,vm_requests.server_id,
               vm_requests.cpu_required,vm_requests.ram_required,vm_requests.storage_required,
               vm_requests.purpose,servers.server_name,servers.host_ip
        FROM ip_pool
        LEFT JOIN vm_requests ON ip_pool.ip_address=vm_requests.ip_address
        LEFT JOIN servers ON vm_requests.server_id=servers.server_id
        ORDER BY ip_pool.ip_address""",conn)

    servers_df=pd.read_sql("SELECT * FROM servers",conn)
    vm_df=pd.read_sql("SELECT * FROM vm_requests",conn)

    total_ips=len(ip_df)
    free_ips=len(ip_df[ip_df["ip_status"]=="free"])
    used_ips=total_ips-free_ips
    total_hosts=len(servers_df)
    total_vms=len(vm_df)

    # ================= CONFIG =================
    with st.expander("⚙️ Configure Dashboard", expanded=True):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            show_summary      = st.checkbox("📊 Summary Metrics",    value=True)
            show_ip_status    = st.checkbox("🥧 IP Status Chart",    value=True)
            show_team         = st.checkbox("👥 VMs by Team",        value=True)
        with col_b:
            show_subnet       = st.checkbox("🔀 Subnet Breakdown",   value=True)
            show_host_cap     = st.checkbox("🖥️ Host Capacity",      value=True)
        with col_c:
            show_ip_table     = st.checkbox("📋 IP Records Table",   value=True)
            show_vm_table     = st.checkbox("⚙️ VM Records Table",   value=True)
            show_host_table   = st.checkbox("🗄️ Host Records Table", value=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= SUMMARY CARDS =================
    if show_summary:
        st.markdown("### 📊 Overview")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("🌐 Total IPs", total_ips)
        m2.metric("✅ Free IPs", free_ips)
        m3.metric("🔴 Assigned IPs", used_ips)
        m4.metric("🖥️ Hosts", total_hosts)
        m5.metric("⚙️ VMs", total_vms)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ================= EMPTY STATE =================
    if vm_df.empty and ip_df.empty:
        st.markdown("""
        <div style="text-align:center;padding:50px;">
            <h3 style="color:#1a2f6e;">📭 No Data Available</h3>
            <p style="color:#6b7280;">Import CSV or create VM</p>
        </div>
        """, unsafe_allow_html=True)

    # ================= IP STATUS + VMs BY TEAM CHARTS =================
    chart_items = [show_ip_status, show_team]
    if any(chart_items):
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        chart_cols = st.columns(sum(1 for x in chart_items if x)); ci = 0

        if show_ip_status:
            pie_df = pd.DataFrame({"Status": ["Free","Assigned"], "Count": [free_ips, used_ips]})
            fig = px.pie(pie_df, names="Status", values="Count",
                         color="Status",
                         color_discrete_map={"Free":"#2952d9","Assigned":"#b3c2e8"},
                         title="IP Pool Status")
            fig.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                               title_font_color="#1a2f6e", margin=dict(t=40,b=10,l=10,r=10),
                               font=dict(family="Inter", size=12))
            chart_cols[ci].plotly_chart(fig, use_container_width=True, key="chart_ip_status")
            ci += 1

        if show_team and not vm_df.empty:
            team_counts = vm_df["team_name"].value_counts().reset_index()
            team_counts.columns = ["Team","VMs"]
            fig2 = px.bar(team_counts, x="Team", y="VMs",
                          color_discrete_sequence=["#2952d9"], title="VMs per Team")
            fig2.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                                title_font_color="#1a2f6e", margin=dict(t=40,b=10,l=10,r=10),
                                font=dict(family="Inter", size=12))
            chart_cols[ci].plotly_chart(fig2, use_container_width=True, key="chart_vms_team")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ================= SUBNET BREAKDOWN =================
    if show_subnet and not ip_df.empty:
        st.markdown("### 🔀 Subnet Breakdown")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        def get_subnet(ip):
            try:
                parts = ip.split(".")
                return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
            except:
                return "Unknown"

        ip_df["subnet"] = ip_df["ip_address"].apply(get_subnet)
        subnet_stats = ip_df.groupby("subnet").agg(
            Total=("ip_address","count"),
            Assigned=("ip_status", lambda x: (x=="assigned").sum()),
            Free=("ip_status", lambda x: (x=="free").sum())
        ).reset_index()
        subnet_stats["Utilization %"] = (subnet_stats["Assigned"] / subnet_stats["Total"] * 100).round(1)
        subnet_stats = subnet_stats.rename(columns={"subnet":"Subnet"})

        fig_sub = px.bar(
            subnet_stats.melt(id_vars="Subnet", value_vars=["Assigned","Free"],
                              var_name="Status", value_name="Count"),
            x="Subnet", y="Count", color="Status",
            color_discrete_map={"Assigned":"#2952d9","Free":"#b3c2e8"},
            barmode="stack", title="IP Distribution by Subnet"
        )
        fig_sub.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                               title_font_color="#1a2f6e", margin=dict(t=40,b=10,l=10,r=10),
                               font=dict(family="Inter", size=12))
        st.plotly_chart(fig_sub, use_container_width=True, key="chart_subnet")

        st.markdown("<br>", unsafe_allow_html=True)
        sh1,sh2,sh3,sh4,sh5 = st.columns([3,1.5,1.5,1.5,2])
        for col,lbl in zip([sh1,sh2,sh3,sh4,sh5],["**Subnet**","**Total IPs**","**Assigned**","**Free**","**Utilization %**"]):
            col.markdown(lbl)
        st.markdown("---")
        for _,row in subnet_stats.iterrows():
            c1,c2,c3,c4,c5 = st.columns([3,1.5,1.5,1.5,2])
            util_color = "#e11d48" if row["Utilization %"]>85 else "#f59e0b" if row["Utilization %"]>60 else "#166534"
            c1.write(row["Subnet"]); c2.write(int(row["Total"])); c3.write(int(row["Assigned"])); c4.write(int(row["Free"]))
            c5.markdown(f'<span style="color:{util_color};font-weight:700;">{row["Utilization %"]}%</span>', unsafe_allow_html=True)

        # ── DOWNLOAD: Subnet Breakdown ──
        st.markdown("<br>", unsafe_allow_html=True)
        subnet_csv = subnet_stats.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Subnet Breakdown CSV",
            subnet_csv,
            file_name="subnet_breakdown.csv",
            mime="text/csv",
            key="dl_subnet"
        )

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ================= HOST CAPACITY =================
    if show_host_cap and not servers_df.empty:
        st.markdown("### 🖥️ Host Capacity")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        vm_usage = pd.read_sql("""
            SELECT server_id,
                   COALESCE(SUM(cpu_required),0) AS used_cpu,
                   COALESCE(SUM(ram_required),0) AS used_ram,
                   COALESCE(SUM(storage_required),0) AS used_disk
            FROM vm_requests WHERE server_id IS NOT NULL GROUP BY server_id
        """, conn)
        vm_usage["server_id"] = pd.to_numeric(vm_usage["server_id"], errors="coerce").astype("Int64")
        servers_cap = servers_df.copy()
        servers_cap["server_id"] = pd.to_numeric(servers_cap["server_id"], errors="coerce").astype("Int64")
        cap_df = servers_cap.merge(vm_usage, on="server_id", how="left")
        cap_df["used_cpu"]  = cap_df["used_cpu"].fillna(0).astype(int)
        cap_df["used_ram"]  = cap_df["used_ram"].fillna(0).astype(int)
        cap_df["used_disk"] = cap_df["used_disk"].fillna(0).astype(int)
        cap_df["cpu_pct"]  = (cap_df["used_cpu"]  / cap_df["total_cpu"].replace(0,1)  * 100).round(1)
        cap_df["ram_pct"]  = (cap_df["used_ram"]  / cap_df["total_ram"].replace(0,1)  * 100).round(1)
        cap_df["disk_pct"] = (cap_df["used_disk"] / cap_df["total_storage"].replace(0,1) * 100).round(1)

        def bar_html(pct):
            pct_clamped = min(int(pct), 100)
            color = "#e11d48" if pct > 85 else "#f59e0b" if pct > 60 else "#2952d9"
            label = "⚠️ Over!" if pct > 100 else f"{pct}%"
            return f"""<div style="display:flex;align-items:center;gap:8px;">
<div style="flex:1;background:#dce8ff;border-radius:4px;height:10px;">
  <div style="width:{pct_clamped}%;background:{color};height:10px;border-radius:4px;"></div>
</div>
<span style="font-size:12px;font-weight:700;color:{color};min-width:48px;">{label}</span></div>"""

        hc1,hc2,hc3,hc4,hc5 = st.columns([2,2,3,3,3])
        for col,lbl in zip([hc1,hc2,hc3,hc4,hc5],["**Host**","**IP**","**CPU Usage**","**RAM Usage**","**Disk Usage**"]):
            col.markdown(lbl)
        st.markdown("---")
        for _,row in cap_df.iterrows():
            c1,c2,c3,c4,c5 = st.columns([2,2,3,3,3])
            c1.write(row["server_name"]); c2.write(row["host_ip"])
            c3.markdown(bar_html(row["cpu_pct"]),  unsafe_allow_html=True)
            c4.markdown(bar_html(row["ram_pct"]),  unsafe_allow_html=True)
            c5.markdown(bar_html(row["disk_pct"]), unsafe_allow_html=True)

        # ── DOWNLOAD: Host Capacity ──
        st.markdown("<br>", unsafe_allow_html=True)
        host_cap_export = cap_df[["server_name","host_ip","total_cpu","total_ram","total_storage",
                                   "used_cpu","used_ram","used_disk","cpu_pct","ram_pct","disk_pct"]].copy()
        host_cap_export.columns = ["Host Name","Host IP","Total CPU","Total RAM (GB)","Total Storage (GB)",
                                    "Used CPU","Used RAM (GB)","Used Disk (GB)","CPU %","RAM %","Disk %"]
        host_cap_csv = host_cap_export.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Host Capacity CSV",
            host_cap_csv,
            file_name="host_capacity.csv",
            mime="text/csv",
            key="dl_host_cap"
        )

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ================= IP RECORDS TABLE =================
    if show_ip_table and not ip_df.empty:
        st.markdown("### 📋 IP Records")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        ip_tbl = ip_df[["ip_address","ip_status","vm_name","team_name","server_name","host_ip","cpu_required","ram_required","storage_required","purpose"]].copy()
        ip_tbl = ip_tbl.fillna("—").replace("None","—")
        ip_tbl.columns = ["IP Address","Status","Owner","Team","Server","Host IP","CPU","RAM (GB)","Disk (GB)","Purpose"]
        st.dataframe(ip_tbl, use_container_width=True, hide_index=True,
                     column_config={"Status": st.column_config.TextColumn("Status")})

        # ── DOWNLOAD: IP Records ──
        ip_csv = ip_tbl.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download IP Records CSV",
            ip_csv,
            file_name="ip_records.csv",
            mime="text/csv",
            key="dl_ip"
        )

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ================= VM RECORDS TABLE =================
    if show_vm_table and not vm_df.empty:
        st.markdown("### ⚙️ VM Records")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        vm_tbl = pd.read_sql("""
            SELECT vm_requests.vm_name, vm_requests.team_name, vm_requests.ip_address,
                   servers.server_name, servers.host_ip,
                   vm_requests.cpu_required, vm_requests.ram_required, vm_requests.storage_required,
                   vm_requests.purpose, vm_requests.approval_status
            FROM vm_requests
            LEFT JOIN servers ON vm_requests.server_id = servers.server_id
            ORDER BY vm_requests.vm_name
        """, conn)
        vm_tbl = vm_tbl.fillna("—").replace("None","—")
        vm_tbl.columns = ["VM Name","Team","IP Address","Server","Host IP","CPU","RAM (GB)","Disk (GB)","Purpose","Status"]
        st.dataframe(vm_tbl, use_container_width=True, hide_index=True)

        # ── DOWNLOAD: VM Records ──
        vm_csv = vm_tbl.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download VM Records CSV",
            vm_csv,
            file_name="vm_records.csv",
            mime="text/csv",
            key="dl_vm"
        )

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ================= HOST RECORDS TABLE =================
    if show_host_table and not servers_df.empty:
        st.markdown("### 🗄️ Host Records")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        host_tbl = servers_df[["server_name","host_ip","server_type","total_cpu","total_ram","total_storage","status"]].copy()
        host_tbl.columns = ["Host Name","Host IP","Type","Total CPU","Total RAM (GB)","Total Storage (GB)","Status"]
        st.dataframe(host_tbl, use_container_width=True, hide_index=True)

        # ── DOWNLOAD: Host Records ──
        host_rec_csv = host_tbl.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Host Records CSV",
            host_rec_csv,
            file_name="host_records.csv",
            mime="text/csv",
            key="dl_host"
        )

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# IP AVAILABILITY PAGE
# =====================================================
elif st.session_state.page=="IP Availability":
    colb1,colb2=st.columns([1,9])
    with colb1:
        if st.button("⬅ Home",key="back_home_ip"):
            st.session_state.page="landing"; st.rerun()

    st.markdown("""
    <div class="page-header">
        <h1>🌐 IP Availability Grid</h1>
        <p>Manage and monitor your IP address pool</p>
    </div>
    """, unsafe_allow_html=True)

    ip_data=pd.read_sql("""
        SELECT ip_pool.ip_address,
            CASE WHEN vm_requests.ip_address IS NULL THEN 'free' ELSE 'assigned' END AS ip_status,
            vm_requests.vm_name,vm_requests.team_name,vm_requests.server_id,
            vm_requests.cpu_required,vm_requests.ram_required,vm_requests.storage_required,
            vm_requests.purpose,servers.server_name,servers.host_ip
        FROM ip_pool
        LEFT JOIN vm_requests ON ip_pool.ip_address=vm_requests.ip_address
        LEFT JOIN servers ON vm_requests.server_id=servers.server_id
        ORDER BY ip_pool.ip_address""",conn)

    ip_data["ip_sort"]=ip_data["ip_address"].apply(lambda ip:int(ipaddress.IPv4Address(ip)))
    ip_data=ip_data.sort_values("ip_sort").drop(columns=["ip_sort"])
    ip_display=ip_data.rename(columns={"vm_name":"Owner","host_ip":"Host IP","team_name":"Team","server_name":"Server","cpu_required":"CPU","ram_required":"RAM","storage_required":"Disk","purpose":"Purpose","ip_address":"IP Address","ip_status":"Status"})
    ip_display=ip_display.fillna("—"); ip_display.replace("None","—",inplace=True)
    ip_display["Host IP"]=ip_display["Host IP"].replace("None","—")
    ip_display["Server"]=ip_display["Server"].replace("None","—")

    @st.dialog("Confirm IP Release")
    def confirm_delete_dialog(ip_address):
        st.markdown(f"### ⚠️ Release IP: `{ip_address}`")
        st.write("This will remove the VM assignment and return the IP to the pool.")
        col1,col2=st.columns(2)
        with col1:
            if st.button("Yes, Release",use_container_width=True):
                cur=conn.cursor()
                cur.execute("DELETE FROM vm_requests WHERE ip_address=?",(ip_address,))
                cur.execute("UPDATE ip_pool SET ip_status='free' WHERE ip_address=?",(ip_address,))
                conn.commit()
                log_action("RELEASE_IP", "IP", resource_id=ip_address, details=f"IP released back to pool")
                st.session_state.ip_deleted=True; st.rerun()
        with col2:
            if st.button("Cancel",use_container_width=True): st.rerun()

    rows_per_page=10; total_rows=len(ip_display)
    total_pages=max(1,(total_rows-1)//rows_per_page+1)
    if st.session_state.ip_page>total_pages: st.session_state.ip_page=total_pages
    start=(st.session_state.ip_page-1)*rows_per_page
    page_df=ip_display.iloc[start:start+rows_per_page]

    st.markdown("<br>", unsafe_allow_html=True)

    toggle_label = "🔼 Hide IP Records" if st.session_state.get("show_ip_records", False) else "📋 Show IP Records"
    btn_col1, btn_col2, _ = st.columns([2, 2, 8])
    with btn_col1:
        if st.button(toggle_label, key="toggle_ip_records", use_container_width=True):
            st.session_state["show_ip_records"] = not st.session_state.get("show_ip_records", False)
            st.rerun()
    with btn_col2:
        if st.button("➕ New VM Request", key="ip_page_new_vm", use_container_width=True):
            st.session_state.open_vm_drawer = True
            st.session_state.open_host_drawer = False
            st.rerun()

    render_vm_drawer()

    if st.session_state.get("show_ip_records", False):
        st.markdown('<div class="section-title">📋 IP Records</div>', unsafe_allow_html=True)

        h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11=st.columns([1.3,1.3,1.4,1.4,1,1,1.2,1.3,1.2,1,1.4])
        for col,label in zip([h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11],["**IP Address**","**Host IP**","**Owner**","**Team**","**CPU**","**RAM**","**Disk**","**Purpose**","**Server**","**Status**","**Actions**"]):
            col.markdown(label)
        st.markdown("---")

        for i,row in page_df.iterrows():
            c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11=st.columns([1.3,1.3,1.4,1.4,1,1,1.2,1.3,1.2,1,1.4])
            status_badge = f'<span style="background:#dcfce7;color:#166534;border-radius:6px;padding:2px 8px;font-size:12px;font-weight:600;">free</span>' if row["Status"]=="free" else f'<span style="background:#dbeafe;color:#1d4ed8;border-radius:6px;padding:2px 8px;font-size:12px;font-weight:600;">assigned</span>'
            c1.write(row["IP Address"]); c2.write(row["Host IP"]); c3.write(row["Owner"]); c4.write(row["Team"])
            c5.write(row["CPU"]); c6.write(row["RAM"]); c7.write(row["Disk"]); c8.write(row["Purpose"])
            c9.write(row["Server"]); c10.markdown(status_badge,unsafe_allow_html=True)
            with c11:
                a1,a2=st.columns([1,1],gap="small")
                with a1:
                    if st.button("✏️",key=f"edit_{i}"):
                        st.session_state.edit_ip=row["IP Address"]
                        st.session_state.open_host_drawer=False; st.session_state.open_vm_drawer=False; st.rerun()
                with a2:
                    if st.button("🗑️",key=f"delete_{i}"): confirm_delete_dialog(row["IP Address"])

        st.markdown("<br>", unsafe_allow_html=True)
        if "ip_deleted" in st.session_state: del st.session_state["ip_deleted"]; st.rerun()

        left,mid,right=st.columns([2,11,1])
        with left:
            if st.button("⬅ Prev",disabled=st.session_state.ip_page==1):
                st.session_state.ip_page-=1; st.rerun()
        with mid:
            st.markdown(f"<div style='text-align:center;font-weight:600;color:#1a2f6e;'>Page {st.session_state.ip_page} of {total_pages}</div>",unsafe_allow_html=True)
        with right:
            if st.button("Next ➡",disabled=st.session_state.ip_page>=total_pages):
                st.session_state.ip_page+=1; st.rerun()

# =====================================================
# HOST GRID PAGE
# =====================================================
elif st.session_state.page=="Host Grid":
    colb1,colb2=st.columns([1,9])
    with colb1:
        if st.button("⬅ Home",key="back_home_host"):
            st.session_state.page="landing"; st.session_state.open_host_drawer=False
            st.session_state.open_vm_drawer=False; st.session_state.edit_host_id=None; st.rerun()

    st.markdown("""
    <div class="page-header">
        <h1>🖥️ Host Grid & VM Inventory</h1>
        <p>Manage servers, hosts and virtual machines</p>
    </div>
    """, unsafe_allow_html=True)

    title_col,btn_col1,btn_col2=st.columns([6,2,2])
    with btn_col1:
        if st.button("➕ New Host",use_container_width=True):
            st.session_state.open_host_drawer=True; st.session_state.open_vm_drawer=False; st.rerun()
    with btn_col2:
        if st.button("📂 Import Hosts CSV",use_container_width=True):
            st.session_state.show_host_csv=True; st.rerun()

    host_template="HOST IP,HOST NAME,SERVER TYPE,CPU,RAM(GB),STORAGE(GB)\n192.168.1.10,Host-01,KVM,32,128,2000\n192.168.1.11,Host-02,VMware,64,256,4000\n"

    if st.session_state.get("show_host_csv"):
        st.markdown("---")
        dl_col,_=st.columns([2,8])
        with dl_col: st.download_button("⬇ Download Host Template",host_template,file_name="host_import_template.csv",mime="text/csv",use_container_width=True)
        host_csv=st.file_uploader("Upload Hosts CSV",type=["csv"],key="host_csv_upload")
        if host_csv:
            df_hosts=pd.read_csv(host_csv,encoding="latin1"); df_hosts.columns=df_hosts.columns.str.strip()
            required_host_cols=["HOST IP","HOST NAME","SERVER TYPE","CPU","RAM(GB)","STORAGE(GB)"]
            missing=[c for c in required_host_cols if c not in df_hosts.columns]
            if missing: st.error(f"❌ Missing columns: {', '.join(missing)}")
            else:
                st.info(f"📄 {host_csv.name} — {len(df_hosts)} rows detected.")
                c1,c2=st.columns(2)
                with c1:
                    if st.button("✅ Import Hosts",use_container_width=True,key="confirm_host_import"):
                        cur=conn.cursor(); added=0; skipped=0
                        for _,row in df_hosts.iterrows():
                            host_ip=str(row["HOST IP"]).strip(); host_name=str(row["HOST NAME"]).strip(); srv_type=str(row["SERVER TYPE"]).strip()
                            try: cpu=int(float(row["CPU"]))
                            except: cpu=0
                            try: ram=int(float(row["RAM(GB)"]))
                            except: ram=0
                            try: storage=int(float(row["STORAGE(GB)"]))
                            except: storage=0
                            if not validate_ip(host_ip): skipped+=1; continue
                            existing=cur.execute("SELECT server_id FROM servers WHERE host_ip=?",(host_ip,)).fetchone()
                            if existing: cur.execute("UPDATE servers SET server_name=?,server_type=?,total_cpu=?,total_ram=?,total_storage=? WHERE host_ip=?",(host_name,srv_type,cpu,ram,storage,host_ip))
                            else: cur.execute("INSERT INTO servers (host_ip,server_name,server_type,total_cpu,total_ram,total_storage,status) VALUES (?,?,?,?,?,?,'active')",(host_ip,host_name,srv_type,cpu,ram,storage)); added+=1
                        conn.commit(); st.session_state.show_host_csv=False
                        log_action("CSV_IMPORT_HOSTS", "BULK", details=f"File: {host_csv.name} | Added: {added}, Skipped: {skipped}")
                        st.success(f"✅ Import done — {added} hosts added, {skipped} skipped."); st.rerun()
                with c2:
                    if st.button("✖ Cancel",use_container_width=True,key="cancel_host_import"):
                        st.session_state.show_host_csv=False; st.rerun()
        else:
            if st.button("✖ Cancel",key="cancel_host_csv_empty"):
                st.session_state.show_host_csv=False; st.rerun()
        st.markdown("---")

    if st.session_state.open_host_drawer:
        st.sidebar.markdown("## ➕ New Host"); st.sidebar.markdown("---")
        new_host_ip    =st.sidebar.text_input("Host IP Address",placeholder="e.g. 192.168.1.20")
        new_host_name  =st.sidebar.text_input("Host Name",placeholder="e.g. Host-04")
        new_server_type=st.sidebar.selectbox("Server Type",["KVM","VMware","Hypervisor","Proxmox","Other"])
        new_cpu        =st.sidebar.number_input("CPU Cores",min_value=1,max_value=512,value=16)
        new_ram        =st.sidebar.number_input("RAM (GB)",min_value=1,max_value=4096,value=64)
        new_storage    =st.sidebar.number_input("Storage (GB)",min_value=0,max_value=100000,value=500)
        st.sidebar.markdown("---")
        sb1,sb2=st.sidebar.columns(2)
        with sb1:
            if st.button("💾 Save Host",use_container_width=True,key="save_new_host"):
                if not validate_ip(new_host_ip): st.sidebar.error("Invalid Host IP address"); st.stop()
                if not new_host_name.strip(): st.sidebar.error("Host name is required"); st.stop()
                cur=conn.cursor()
                cur.execute("INSERT INTO servers (host_ip,server_name,server_type,total_cpu,total_ram,total_storage,status) VALUES (?,?,?,?,?,?,?)",(new_host_ip.strip(),new_host_name.strip(),new_server_type,new_cpu,new_ram,new_storage,'active'))
                conn.commit()
                log_action("CREATE_HOST", "HOST", resource_id=new_host_ip,
                           details=f"Name: {new_host_name} | Type: {new_server_type} | CPU: {new_cpu} | RAM: {new_ram}GB | Storage: {new_storage}GB")
                st.sidebar.success(f"✅ Host '{new_host_name}' added!"); st.session_state.open_host_drawer=False; st.rerun()
        with sb2:
            if st.button("✖ Cancel",use_container_width=True,key="cancel_new_host"):
                st.session_state.open_host_drawer=False; st.rerun()

    render_vm_drawer()

    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Server Capacity Overview</div>',unsafe_allow_html=True)
    vm_count=pd.read_sql("SELECT server_id,COUNT(*) as running_vms FROM vm_requests WHERE server_id IS NOT NULL GROUP BY server_id",conn)
    servers_df=pd.read_sql("SELECT * FROM servers",conn)
    servers_df["server_id"]=pd.to_numeric(servers_df["server_id"],errors="coerce").astype("Int64")
    vm_count["server_id"]=pd.to_numeric(vm_count["server_id"],errors="coerce").astype("Int64")
    capacity_df=servers_df.merge(vm_count,on="server_id",how="left"); capacity_df["running_vms"]=capacity_df["running_vms"].fillna(0).astype(int)

    if "edit_host_id" not in st.session_state: st.session_state.edit_host_id=None

    h1,h2,h3,h4,h5,h6,h7,h8,h9=st.columns([1.5,1.5,1.5,1,1,1.5,1,1.2,1])
    for col,label in zip([h1,h2,h3,h4,h5,h6,h7,h8,h9],["**Host IP**","**Host Name**","**Server Type**","**CPU**","**RAM (GB)**","**Storage (GB)**","**Status**","**Running VMs**","**Actions**"]):
        col.markdown(label)
    st.markdown("---")

    for i,row in capacity_df.iterrows():
        sid=int(row["server_id"])
        c1,c2,c3,c4,c5,c6,c7,c8,c9=st.columns([1.5,1.5,1.5,1,1,1.5,1,1.2,1])
        status_badge=f'<span style="background:#dcfce7;color:#166534;border-radius:6px;padding:2px 8px;font-size:12px;font-weight:600;">{row["status"]}</span>' if row["status"]=="active" else f'<span style="background:#fee2e2;color:#991b1b;border-radius:6px;padding:2px 8px;font-size:12px;font-weight:600;">{row["status"]}</span>'
        c1.write(row["host_ip"]); c2.write(row["server_name"]); c3.write(row["server_type"])
        c4.write(int(row["total_cpu"])); c5.write(int(row["total_ram"])); c6.write(int(row["total_storage"]))
        c7.markdown(status_badge,unsafe_allow_html=True); c8.write(int(row["running_vms"]))
        with c9:
            if st.button("✏️",key=f"edit_host_{sid}"):
                st.session_state.edit_host_id=sid; st.session_state.open_host_drawer=False; st.session_state.open_vm_drawer=False; st.rerun()

    if st.session_state.edit_host_id is not None:
        host_row=pd.read_sql("SELECT * FROM servers WHERE server_id=?",conn,params=(st.session_state.edit_host_id,))
        if len(host_row)>0:
            hd=host_row.iloc[0]
            st.sidebar.title("✏️ Edit Host"); st.sidebar.markdown(f"### {hd['server_name']}"); st.sidebar.markdown("---")
            st.sidebar.text_input("Host IP",value=hd["host_ip"],disabled=True)
            new_name  =st.sidebar.text_input("Host Name",value=hd["server_name"],key="eh_name")
            type_opts =["KVM","VMware","Hypervisor","Proxmox","Unknown","Other"]
            new_type  =st.sidebar.selectbox("Server Type",type_opts,index=type_opts.index(hd["server_type"] if hd["server_type"] in type_opts else "Unknown"),key="eh_type")
            new_cpu   =st.sidebar.number_input("CPU Cores",   min_value=0,max_value=512,   value=int(hd["total_cpu"]),    key="eh_cpu")
            new_ram   =st.sidebar.number_input("RAM (GB)",    min_value=0,max_value=4096,  value=int(hd["total_ram"]),    key="eh_ram")
            new_disk  =st.sidebar.number_input("Storage (GB)",min_value=0,max_value=100000,value=int(hd["total_storage"]),key="eh_disk")
            new_status=st.sidebar.selectbox("Status",["active","inactive"],index=0 if hd["status"]=="active" else 1,key="eh_status")
            st.sidebar.markdown("---")
            sb1,sb2=st.sidebar.columns(2)
            with sb1:
                if st.button("💾 Save",use_container_width=True,key="save_host_edit"):
                    cur=conn.cursor()
                    cur.execute("UPDATE servers SET server_name=?,server_type=?,total_cpu=?,total_ram=?,total_storage=?,status=? WHERE server_id=?",(new_name,new_type,new_cpu,new_ram,new_disk,new_status,st.session_state.edit_host_id))
                    conn.commit()
                    log_action("EDIT_HOST", "HOST", resource_id=hd["host_ip"],
                               details=f"Name: {new_name} | Type: {new_type} | CPU: {new_cpu} | RAM: {new_ram}GB | Storage: {new_disk}GB | Status: {new_status}")
                    st.session_state.edit_host_id=None; st.rerun()
            with sb2:
                if st.button("✖ Cancel",use_container_width=True,key="cancel_host_edit"):
                    st.session_state.edit_host_id=None; st.rerun()

    edit_data=None
    if st.session_state.edit_vm_ip:
        df=pd.read_sql("SELECT * FROM vm_requests WHERE ip_address=?",conn,params=(st.session_state.edit_vm_ip,))
        if len(df)>0: edit_data=df.iloc[0]

# =====================================================
# SIDEBAR EDIT PANEL (IP Availability)
# =====================================================
if "edit_ip" in st.session_state and st.session_state.edit_ip is not None and st.session_state.page=="IP Availability":
    st.session_state.open_host_drawer=False; st.session_state.open_vm_drawer=False
    ip_address=st.session_state.edit_ip

    df=pd.read_sql("""
        SELECT ip_pool.ip_address,ip_pool.ip_status,
               vm_requests.vm_name,vm_requests.team_name,
               vm_requests.server_id,vm_requests.cpu_required,
               vm_requests.ram_required,vm_requests.storage_required,vm_requests.purpose
        FROM ip_pool
        LEFT JOIN vm_requests ON ip_pool.ip_address=vm_requests.ip_address
        WHERE ip_pool.ip_address=?""",conn,params=(ip_address,))

    if len(df)==0: st.session_state.edit_ip=None; st.rerun()
    data=df.iloc[0]

    if "edit_server" not in st.session_state and pd.notna(data["server_id"]):
        st.session_state.edit_server=int(data["server_id"])

    servers_list=pd.read_sql("SELECT server_id,server_name FROM servers",conn)
    server_ids=list(servers_list["server_id"])
    if "edit_server" not in st.session_state: st.session_state.edit_server=server_ids[0]

    st.sidebar.title("✏️ Edit IP"); st.sidebar.markdown(f"### {ip_address}")
    server_choice=st.sidebar.selectbox("Server Name",options=server_ids,index=server_ids.index(st.session_state.edit_server),format_func=lambda x:servers_list.loc[servers_list["server_id"]==x,"server_name"].values[0],key="edit_server")

    server_cap=pd.read_sql("SELECT total_cpu,total_ram,total_storage FROM servers WHERE server_id=?",conn,params=(server_choice,))
    total_cpu=int(server_cap.iloc[0]["total_cpu"]); total_ram=int(server_cap.iloc[0]["total_ram"]); total_disk=int(server_cap.iloc[0]["total_storage"])
    used=pd.read_sql("SELECT COALESCE(SUM(cpu_required),0) AS used_cpu,COALESCE(SUM(ram_required),0) AS used_ram,COALESCE(SUM(storage_required),0) AS used_disk FROM vm_requests WHERE server_id=? AND ip_address!=?",conn,params=(server_choice,ip_address))
    used_cpu=int(used.iloc[0]["used_cpu"]); used_ram=int(used.iloc[0]["used_ram"]); used_disk=int(used.iloc[0]["used_disk"])

    current_cpu =int(data["cpu_required"])     if pd.notna(data["cpu_required"])     else 1
    current_ram =int(data["ram_required"])     if pd.notna(data["ram_required"])     else 1
    current_disk=int(data["storage_required"]) if pd.notna(data["storage_required"]) else 10

    available_cpu  = max(total_cpu - used_cpu,  current_cpu)
    available_ram  = max(total_ram - used_ram,  current_ram)
    available_disk = max(total_disk - used_disk, current_disk)

    used_pct_cpu  = round((used_cpu  / total_cpu  * 100), 1) if total_cpu  > 0 else 0
    used_pct_ram  = round((used_ram  / total_ram  * 100), 1) if total_ram  > 0 else 0
    used_pct_disk = round((used_disk / total_disk * 100), 1) if total_disk > 0 else 0

    bar_cpu  = min(int(used_pct_cpu),  100)
    bar_ram  = min(int(used_pct_ram),  100)
    bar_disk = min(int(used_pct_disk), 100)
    col_cpu  = '#e11d48' if bar_cpu  > 85 else '#f59e0b' if bar_cpu  > 60 else '#2952d9'
    col_ram  = '#e11d48' if bar_ram  > 85 else '#f59e0b' if bar_ram  > 60 else '#2952d9'
    col_disk = '#e11d48' if bar_disk > 85 else '#f59e0b' if bar_disk > 60 else '#2952d9'

    st.sidebar.markdown(f"""
<div style="background:#f0f4ff;border-radius:10px;padding:14px 16px;border:1px solid #dce8ff;margin:8px 0;">
<p style="font-weight:700;color:#1a2f6e;margin:0 0 10px 0;">📊 Server Resource Usage</p>
<p style="font-size:13px;color:#1a2f6e;font-weight:600;margin:0 0 4px 0;">🖥️ vCPU &nbsp;&nbsp; {used_cpu} / {total_cpu} cores ({'⚠️ Over!' if used_pct_cpu > 100 else str(used_pct_cpu)+'%'})</p>    
<table width="100%" cellspacing="0" cellpadding="0"><tr>
<td width="{bar_cpu}%" style="background:{col_cpu};height:8px;border-radius:4px 0 0 4px;"></td>
<td width="{100-bar_cpu}%" style="background:#dce8ff;height:8px;border-radius:0 4px 4px 0;"></td>
</tr></table>
<p style="font-size:13px;color:#1a2f6e;font-weight:600;margin:10px 0 4px 0;">💾 RAM &nbsp;&nbsp; {used_ram} / {total_ram} GB ({'⚠️ Over!' if used_pct_ram > 100 else str(used_pct_ram)+'%'})</p>
<table width="100%" cellspacing="0" cellpadding="0"><tr>
<td width="{bar_ram}%" style="background:{col_ram};height:8px;border-radius:4px 0 0 4px;"></td>
<td width="{100-bar_ram}%" style="background:#dce8ff;height:8px;border-radius:0 4px 4px 0;"></td>
</tr></table>
<p style="font-size:13px;color:#1a2f6e;font-weight:600;margin:10px 0 4px 0;">💿 Disk &nbsp;&nbsp; {used_disk} / {total_disk} GB ({'⚠️ Over!' if used_pct_disk > 100 else str(used_pct_disk)+'%'})</p>
<table width="100%" cellspacing="0" cellpadding="0"><tr>
<td width="{bar_disk}%" style="background:{col_disk};height:8px;border-radius:4px 0 0 4px;"></td>
<td width="{100-bar_disk}%" style="background:#dce8ff;height:8px;border-radius:0 4px 4px 0;"></td>
</tr></table>
<p style="font-size:12px;color:#2952d9;font-weight:600;margin:10px 0 0 0;">✅ Available — CPU: {available_cpu} | RAM: {available_ram} GB | Disk: {available_disk} GB</p>
</div>""", unsafe_allow_html=True)
    owner=st.sidebar.text_input("Owner Name",value=data["vm_name"]   if pd.notna(data["vm_name"])   else "")
    team =st.sidebar.text_input("Team Name", value=data["team_name"] if pd.notna(data["team_name"]) else "")
    if not owner.strip(): st.sidebar.error("Owner name required"); st.stop()
    if not team.strip():  st.sidebar.error("Team name required");  st.stop()

    purpose_options=["Development","Testing","R&D"]
    purpose_idx=purpose_options.index(data["purpose"]) if pd.notna(data["purpose"]) and data["purpose"] in purpose_options else 0
    purpose=st.sidebar.selectbox("Purpose",purpose_options,index=purpose_idx)

    cpu =st.sidebar.number_input("CPU Cores",min_value=1,max_value=int(available_cpu), value=min(int(data["cpu_required"]) if pd.notna(data["cpu_required"]) else 1,int(available_cpu)))
    ram =st.sidebar.number_input("RAM (GB)", min_value=1,max_value=int(available_ram), value=min(int(data["ram_required"]) if pd.notna(data["ram_required"]) else 1,int(available_ram)))
    disk_min=min(10,int(available_disk)); disk_value=int(data["storage_required"]) if pd.notna(data["storage_required"]) else 10
    disk_value=max(disk_min,min(disk_value,int(available_disk)))
    disk  =st.sidebar.number_input("Disk (GB)",min_value=disk_min,max_value=int(available_disk),value=disk_value)
    status=st.sidebar.selectbox("Status",["free","assigned"],index=0 if data["ip_status"]=="free" else 1)

    c1,c2=st.sidebar.columns(2)
    with c1:
        if st.button("💾 Save",use_container_width=True):
            if not owner.strip(): st.sidebar.error("Owner name required"); st.stop()
            if not team.strip():  st.sidebar.error("Team name required");  st.stop()
            cur=conn.cursor()
            existing=cur.execute("SELECT * FROM vm_requests WHERE ip_address=?",(ip_address,)).fetchone()
            if existing:
                cur.execute("UPDATE vm_requests SET vm_name=?,team_name=?,server_id=?,cpu_required=?,ram_required=?,storage_required=?,purpose=? WHERE ip_address=?",(owner,team,server_choice,cpu,ram,disk,purpose,ip_address))
                action_label = "EDIT_VM"
            else:
                cur.execute("INSERT INTO vm_requests (ip_address,vm_name,team_name,server_id,cpu_required,ram_required,storage_required,purpose) VALUES(?,?,?,?,?,?,?,?)",(ip_address,owner,team,server_choice,cpu,ram,disk,purpose))
                action_label = "CREATE_VM"
            cur.execute("UPDATE ip_pool SET ip_status=? WHERE ip_address=?",(status,ip_address))
            conn.commit()
            log_action(action_label, "VM", resource_id=ip_address,
                       details=f"Owner: {owner} | Team: {team} | CPU: {cpu} | RAM: {ram}GB | Disk: {disk}GB | Status: {status} | Purpose: {purpose}")
            st.session_state.edit_ip=None; st.rerun()
    with c2:
        if st.button("Cancel",use_container_width=True):
            st.session_state.edit_ip=None
            if "edit_server" in st.session_state: del st.session_state.edit_server
            st.rerun()

# =====================================================
# AUDIT LOG PAGE
# =====================================================
elif st.session_state.page=="Audit Log":
    colb1,_=st.columns([1,9])
    with colb1:
        if st.button("⬅ Home",key="back_home_audit"):
            st.session_state.page="landing"; st.rerun()

    st.markdown("""
    <div class="page-header">
        <h1>📋 Audit Log</h1>
        <p>Track all infrastructure actions with timestamps and user details</p>
    </div>
    """, unsafe_allow_html=True)

    audit_df = pd.read_sql(
        "SELECT timestamp, user, action, resource, resource_id, details, status FROM audit_log ORDER BY id DESC",
        conn
    )

    if audit_df.empty:
        st.markdown("""
        <div style="text-align:center;padding:60px;">
            <h3 style="color:#1a2f6e;">📭 No audit records yet</h3>
            <p style="color:#6b7280;">Actions like creating VMs, editing hosts, and importing CSVs will appear here.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        total_actions  = len(audit_df)
        unique_users   = audit_df["user"].nunique()
        action_types   = audit_df["action"].nunique()
        failed_actions = len(audit_df[audit_df["status"]=="error"])

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("📋 Total Actions",  total_actions)
        m2.metric("👤 Unique Users",   unique_users)
        m3.metric("🔖 Action Types",   action_types)
        m4.metric("❌ Failed Actions", failed_actions)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔍 Filter Logs</div>', unsafe_allow_html=True)
        fc1,fc2,fc3,fc4 = st.columns(4)
        with fc1:
            all_users = ["All"] + sorted(audit_df["user"].unique().tolist())
            sel_user = st.selectbox("User", all_users, key="audit_user_filter")
        with fc2:
            all_actions = ["All"] + sorted(audit_df["action"].unique().tolist())
            sel_action = st.selectbox("Action", all_actions, key="audit_action_filter")
        with fc3:
            all_resources = ["All"] + sorted(audit_df["resource"].unique().tolist())
            sel_resource = st.selectbox("Resource", all_resources, key="audit_resource_filter")
        with fc4:
            all_statuses = ["All"] + sorted(audit_df["status"].unique().tolist())
            sel_status = st.selectbox("Status", all_statuses, key="audit_status_filter")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        filtered = audit_df.copy()
        if sel_user     != "All": filtered = filtered[filtered["user"]     == sel_user]
        if sel_action   != "All": filtered = filtered[filtered["action"]   == sel_action]
        if sel_resource != "All": filtered = filtered[filtered["resource"] == sel_resource]
        if sel_status   != "All": filtered = filtered[filtered["status"]   == sel_status]

        action_colours = {
            "CREATE_VM":          ("#dcfce7","#166534"),
            "EDIT_VM":            ("#dbeafe","#1d4ed8"),
            "RELEASE_IP":         ("#fef9c3","#854d0e"),
            "CREATE_HOST":        ("#f3e8ff","#6b21a8"),
            "EDIT_HOST":          ("#e0f2fe","#0369a1"),
            "CSV_IMPORT":         ("#fce7f3","#9d174d"),
            "CSV_IMPORT_HOSTS":   ("#fce7f3","#9d174d"),
        }

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">📋 {len(filtered)} Records</div>', unsafe_allow_html=True)

        ah1,ah2,ah3,ah4,ah5,ah6,ah7 = st.columns([2,2,2,1.5,1.5,3.5,1.2])
        for col,lbl in zip([ah1,ah2,ah3,ah4,ah5,ah6,ah7],
                           ["**Timestamp**","**User**","**Action**","**Resource**","**Resource ID**","**Details**","**Status**"]):
            col.markdown(lbl)
        st.markdown("---")

        for _,row in filtered.iterrows():
            a_bg, a_fg = action_colours.get(row["action"], ("#f0f4ff","#1a2f6e"))
            s_bg  = "#dcfce7" if row["status"]=="success" else "#fee2e2"
            s_fg  = "#166534" if row["status"]=="success" else "#991b1b"
            s_ico = "✅" if row["status"]=="success" else "❌"

            r1,r2,r3,r4,r5,r6,r7 = st.columns([2,2,2,1.5,1.5,3.5,1.2])
            r1.markdown(f'<span style="font-size:12px;color:#6b7280;">{row["timestamp"]}</span>', unsafe_allow_html=True)
            r2.markdown(f'<span style="font-size:13px;font-weight:600;color:#1a2f6e;">👤 {row["user"]}</span>', unsafe_allow_html=True)
            r3.markdown(f'<span style="background:{a_bg};color:{a_fg};border-radius:6px;padding:2px 8px;font-size:12px;font-weight:700;">{row["action"]}</span>', unsafe_allow_html=True)
            r4.markdown(f'<span style="font-size:12px;font-weight:600;color:#2952d9;">{row["resource"]}</span>', unsafe_allow_html=True)
            r5.markdown(f'<span style="font-size:12px;color:#374151;">{row["resource_id"] or "—"}</span>', unsafe_allow_html=True)
            r6.markdown(f'<span style="font-size:12px;color:#374151;">{row["details"] or "—"}</span>', unsafe_allow_html=True)
            r7.markdown(f'<span style="background:{s_bg};color:{s_fg};border-radius:6px;padding:2px 8px;font-size:12px;font-weight:600;">{s_ico} {row["status"]}</span>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        csv_export = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Export Audit Log as CSV", csv_export,
            file_name="audit_log_export.csv", mime="text/csv"
        )