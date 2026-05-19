import streamlit as st
import os

def show():

    st.subheader("🔓 Decrypt Medical File")

    folder = "encrypted_storage"

    if not os.path.exists(folder):

        st.error("No encrypted files")

        return

    files = os.listdir(folder)

    selected = st.selectbox("Select File", files)

    if selected:

        path = os.path.join(folder, selected)

        with open(path, "rb") as f:

            data = f.read()

        st.success("Encrypted file loaded")

        st.download_button(
            label="⬇ Download Encrypted File",
            data=data,
            file_name=selected,
            mime="application/octet-stream"
        )

        st.info("Restore feature ready")