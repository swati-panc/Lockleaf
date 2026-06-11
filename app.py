import streamlit as st
import random
import string
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="LockLeaf", page_icon="🔒", layout="centered")

# --- FUNCTIONS ---
def load_passwords():
    """File se passwords load karne ke liye"""
    passwords = {}
    if os.path.exists("passwords.txt"):
        with open("passwords.txt", "r") as file:
            for line in file:
                if ":" in line:
                    website, pwd = line.strip().split(":", 1)
                    passwords[website] = pwd
    return passwords

def save_password(site, pwd):
    """Naya password file mein save karne ke liye"""
    with open("passwords.txt", "a") as file:
        file.write(f"{site}:{pwd}\n")

def generate_password():
    """Random strong password banane ke liye"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+=-"
    return "".join(random.choice(chars) for _ in range(12)) # 12 chars for better security

# --- APP HEADER ---
st.title("🔒 LOCKLEAF")
st.caption("Your Personal Password Manager")
st.markdown("---")

# Passwords load karein
passwords = load_passwords()

# --- STREAMLIT TABS (UI Navigation) ---
tab1, tab2, tab3 = st.tabs(["📝 Save Password", "👁️ View Passwords", "⚡ Generate Password"])

# TAB 1: Save Password
with tab1:
    st.subheader("Save a New Password")
    site_input = st.text_input("Enter Website Name", placeholder="e.g., google.com")
    pwd_input = st.text_input("Enter Password", type="password", placeholder="Enter secret password")
    
    if st.button("Save Password", type="primary"):
        if site_input and pwd_input:
            save_password(site_input, pwd_input)
            st.success(f"Success: Password for **{site_input}** saved successfully!")
            st.rerun() # UI ko refresh karne ke liye taaki view tab me turant dikhe
        else:
            st.error("Please fill in both fields!")

# TAB 2: View Passwords
with tab2:
    st.subheader("Your Saved Passwords")
    if not passwords:
        st.info("No data found. Start by saving a password!")
    else:
        # Data ko acche format me table ya key-value me dikhane ke liye
        for site, pwd in passwords.items():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**Website:** {site}")
            with col2:
                # Password ko copy karne ka option streamlit automatically deta hai text_input me
                st.text_input("Password", value=pwd, type="password", disabled=True, label_visibility="collapsed", key=f"pwd_{site}")
        
        # Ek clear button data delete karne ke liye (Optional)
        if st.button("Clear All Logs (Reset File)"):
            if os.path.exists("passwords.txt"):
                os.remove("passwords.txt")
                st.warning("All passwords deleted!")
                st.rerun()

# TAB 3: Generate Password
with tab3:
    st.subheader("Generate a Strong Password")
    
    # Session state use kar rahe hain taaki button click par password bar-bar change na ho jab tak user na chahe
    if 'gen_pwd' not in st.session_state:
        st.session_state.gen_pwd = ""

    if st.button("Generate"):
        st.session_state.gen_pwd = generate_password()
        
    if st.session_state.gen_pwd:
        st.code(st.session_state.gen_pwd, language="") # code block me daala taaki user 1-click me copy kar sake
        st.info("💡 You can copy this password and use it in the 'Save Password' tab.")