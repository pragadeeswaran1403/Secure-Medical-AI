import streamlit as st
import os

def show_gallery():

    st.subheader("🔐 Encrypted Storage Gallery")

    folder = "encrypted_storage"

    if not os.path.exists(folder):

        st.warning("No encrypted files found")

        return

    files = os.listdir(folder)

    if not files:

        st.warning("Gallery Empty")

        return

    cols = st.columns(3)

    for i, file in enumerate(files):

        with cols[i % 3]:

            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.08);
                padding:20px;
                border-radius:20px;
                text-align:center;
                box-shadow:0 0 15px cyan;
            ">
                <h3>🔒 Encrypted File</h3>
                <p>{file}</p>
            </div>
            """, unsafe_allow_html=True)