import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# --- Page Config ---
st.set_page_config(
    page_title="Digital Trust Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initialize Session State ---
if 'decoys_used' not in st.session_state:
    st.session_state.decoys_used = 14
if 'threats_blocked' not in st.session_state:
    st.session_state.threats_blocked = 1422
if 'is_ghost_mode' not in st.session_state:
    st.session_state.is_ghost_mode = False
if 'is_shield_active' not in st.session_state:
    st.session_state.is_shield_active = True
if 'decoy_info' not in st.session_state:
    st.session_state.decoy_info = {
        'name': 'Alex Rivera',
        'email': 'a.rivera@privacymail.io',
        'location': 'Central Park, NY, USA',
        'id': 'GEN-12-AND-991'
    }
if 'services' not in st.session_state:
    st.session_state.services = [
        {'id': 1, 'name': 'MediCare Plus (Health)', 'ghosted': True, 'permissions': {'Heart Rate': True, 'Location': False}},
        {'id': 2, 'name': 'FinTrack Pro (Finance)', 'ghosted': False, 'permissions': {'Transactions': True, 'Contacts': False}},
        {'id': 3, 'name': 'SocialSphere (Social)', 'ghosted': False, 'permissions': {'Camera': False, 'Mic': False}}
    ]

# --- Dynamic State Calculation ---
if st.session_state.is_ghost_mode and st.session_state.is_shield_active:
    trust_score = 99
elif st.session_state.is_ghost_mode:
    trust_score = 96
elif st.session_state.is_shield_active:
    trust_score = 90
else:
    trust_score = 65

# --- Forecast Logic ---
def get_forecast(score):
    if score >= 95:
        return "Stealth Mode 👻", "Invisible to trackers", "Protocol: Advanced Masking Active"
    elif score >= 85:
        return "Clear Skies 🌤️", "Environment Secure", "Protocol: Shield Integrity Normal"
    else:
        return "Digital Drizzle 🌧️", "Some Tracking Active", "Warning: Metadata Leakage Possible"

forecast_label, forecast_sub, forecast_log = get_forecast(trust_score)

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("🛡️ TrustGuard")
    st.markdown("---")
    active_tab = st.radio(
        "Navigation",
        ["Dashboard", "Identity Vault", "Data Nodes", "Audit Logs", "SDK Integration"]
    )
    st.markdown("---")
    st.caption("Protocol Guard: **Active** 🟢")

# --- Views ---
st.title("Digital Trust Dashboard")

if active_tab == "Dashboard":
    st.markdown("### 📊 System Overview")
    
    # Top Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Digital Forecast", value=forecast_label, delta=forecast_sub, delta_color="off")
    with col2:
        st.metric(label="System Trust Integrity", value=f"{trust_score} / 100")
    with col3:
        st.metric(label="Decoys Active 👻", value=st.session_state.decoys_used if st.session_state.is_ghost_mode else 0)
        st.metric(label="Threats Filtered 🛡️", value=st.session_state.threats_blocked)

    st.markdown("---")
    
    # Active Protocols
    st.markdown("### ⚙️ Active Protocols")
    p_col1, p_col2 = st.columns(2)
    
    with p_col1:
        st.info("**Silent Shield**\n\nAutomatically blocks risky trackers in the background without pestering you.")
        st.session_state.is_shield_active = st.toggle("Activate Silent Shield", value=st.session_state.is_shield_active)
        
    with p_col2:
        st.info(f"**Ghost Mode**\n\nGenerates a disposable identity to confuse trackers. Climate: {'Stealth' if st.session_state.is_ghost_mode else 'Exposed'}.")
        st.session_state.is_ghost_mode = st.toggle("Activate Ghost Mode", value=st.session_state.is_ghost_mode)

    st.markdown("---")
    
    # Bottom Section
    b_col1, b_col2 = st.columns(2)
    
    with b_col1:
        st.markdown("### 📱 Linked Devices & Apps")
        for idx, service in enumerate(st.session_state.services):
            with st.expander(service['name'], expanded=(idx == 0)):
                for perm, is_active in service['permissions'].items():
                    # Streamlit checkboxes to manage permissions
                    new_val = st.checkbox(perm, value=is_active, key=f"perm_{service['id']}_{perm}")
                    st.session_state.services[idx]['permissions'][perm] = new_val
                
                if st.button("Revoke Access", key=f"revoke_{service['id']}", type="primary"):
                    for perm in service['permissions']:
                        st.session_state.services[idx]['permissions'][perm] = False
                    st.rerun()

    with b_col2:
        st.markdown("### 📝 Live Audit Trail")
        
        logs = [
            {"app": "System Shield", "action": forecast_log, "time": "Just now", "status": "✅"},
            {"app": "AdTracker.io", "action": "Silent Block" if st.session_state.is_shield_active else "Data Leaking", "time": "2m ago", "status": "🛡️" if st.session_state.is_shield_active else "⚠️"},
            {"app": "Location Node", "action": "Spoofed Identity" if st.session_state.is_ghost_mode else "Real IP Exposed", "time": "13m ago", "status": "👻" if st.session_state.is_ghost_mode else "📍"}
        ]
        
        for log in logs:
            st.markdown(f"**{log['status']} {log['app']}**")
            st.caption(f"{log['action']} • {log['time']}")
            st.divider()

elif active_tab == "Identity Vault":
    st.markdown("### 👻 Identity Masking Vault")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("🔒 **Real Identity (Hidden)**")
        st.markdown("Data heavily encrypted and obfuscated from external trackers.")
        st.progress(100)
        
    with col2:
        st.success("✨ **Decoy Identity (Broadcasting)**")
        
        # Updating Identity State
        st.session_state.decoy_info['name'] = st.text_input("Active Alias", value=st.session_state.decoy_info['name'])
        st.session_state.decoy_info['email'] = st.text_input("Masked Email", value=st.session_state.decoy_info['email'])
        st.session_state.decoy_info['location'] = st.text_input("Spoofed Origin", value=st.session_state.decoy_info['location'])
        st.session_state.decoy_info['id'] = st.text_input("Synthetic ID", value=st.session_state.decoy_info['id'])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔀 Refresh Synthetic Identity", use_container_width=True):
        names = ['Jordan Smith', 'Casey Vales', 'Riley Quinn', 'Morgan Lee']
        locations = ['Shibuya, Tokyo', 'Kreuzberg, Berlin', 'Brooklyn, NY', 'Hackney, London']
        rand_num = random.randint(100, 999)
        
        st.session_state.decoy_info = {
            'name': random.choice(names),
            'email': f'anon_{rand_num}@shield.net',
            'location': random.choice(locations),
            'id': f'SYN-{rand_num}-USR-X'
        }
        st.session_state.decoys_used += 1
        st.rerun()

elif active_tab == "Data Nodes":
    st.markdown("### 🌐 Connected Data Nodes")
    
    # Transform session state services into a dataframe
    table_data = []
    for s in st.session_state.services:
        active_perms = sum(1 for v in s['permissions'].values() if v)
        category = 'Health / Confidential' if 'Health' in s['name'] else 'Finance / Sensitive' if 'Finance' in s['name'] else 'Social / Public'
        
        table_data.append({
            "Node Name": s['name'],
            "Security Category": category,
            "Permission State": f"{active_perms} Active" if active_perms > 0 else "Access Revoked",
            "Ghost Masking": "Active 👻" if s['ghosted'] else "Inactive ⚠️"
        })
        
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.warning("🚨 **Emergency Kill-Switch** - Revoke all permissions across every linked device instantly.")
    if st.button("Revoke All Permissions", type="primary"):
        for idx in range(len(st.session_state.services)):
            for perm in st.session_state.services[idx]['permissions']:
                st.session_state.services[idx]['permissions'][perm] = False
        st.success("All permissions revoked successfully.")
        st.rerun()

elif active_tab == "Audit Logs":
    st.markdown("### 📜 Immutable Audit Log")
    
    # Static mock data reflecting actions
    log_data = [
        {"Event": "Silent Block", "Source": "AdTracker.io", "Timestamp": "18:01:02", "Result": "Filtered"},
        {"Event": "Identity Rotation", "Source": "Ghost Mode", "Timestamp": "17:55:14", "Result": "Successful"},
        {"Event": "Permission Revoked", "Source": "Manual Override", "Timestamp": "17:30:00", "Result": "Hard-Blocked"},
        {"Event": "Node Connected", "Source": "MediCare Plus", "Timestamp": "16:45:22", "Result": "Masked"},
    ]
    
    df_logs = pd.DataFrame(log_data)
    st.dataframe(df_logs, use_container_width=True, hide_index=True)

elif active_tab == "SDK Integration":
    st.markdown("### 💻 SDK Integration")
    st.markdown("Integrate TrustGuard directly into your application stack.")
    
    code = '''# Python SDK Initialization
import trustvault
client = trustvault.Client(api_key="tv_sk_demo")

# Request Secure Consent
response = client.request_consent(
    user_id="u_99",
    scope=["heart_rate", "location"]
)

if response.status == "approved":
    print("Masked data access granted.")
else:
    print("Access blocked by TrustGuard.")
'''
    st.code(code, language='python')