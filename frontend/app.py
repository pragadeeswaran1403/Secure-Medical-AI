import streamlit as st
import cv2
import numpy as np
import hashlib
import time
from datetime import datetime
import os
import sys
import random
import matplotlib.pyplot as plt
import pyttsx3



def get_confidence():
    return round(random.uniform(80, 98), 2)

def show_graph(conf):
    labels = ['Confidence']
    values = [conf]

def show_graph(conf):
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 0px 20px rgba(0,255,255,0.3);
    ">
        <h3 style="color:#00e6e6;">AI Confidence Level</h3>
        <div style="
            font-size: 50px;
            font-weight: bold;
            color: #00ffcc;
            text-shadow: 0px 0px 15px #00ffcc;
        ">
            {conf}%
        </div>
        <div style="margin-top:10px;">
            {"🟢 Excellent" if conf > 90 else "🟡 Good" if conf > 80 else "🔴 Low"}
        </div>
    </div>
    """, unsafe_allow_html=True)


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)
from PIL import Image

from database import delete_record
from model.segmentation_model import segment_tumor


from model.multi_model import predict_image
from utils.chatbot import get_bot_response
from utils.access_logger import log_access, get_logs
from utils.risk import get_risk_level


from utils.email_utils import send_email

from blockchain.blockchain_utils import store_hash, is_connected
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from database import add_patient_record, get_patient_records, get_stats
from crypto_utils import encrypt_data
from crypto.aes_utils import encrypt_aes
from frontend import decrypt_page
from frontend.gallery_page import show_gallery


from auth import register_user, login_user

from crypto.dna_crypto import dna_encode
from ipfs.ipfs_utils import upload_to_ipfs
from utils.heatmap import apply_heatmap
from utils.risk import get_risk_level



st.set_page_config(page_title="Medical System", layout="wide")
engine = pyttsx3.init()
# 🎨 UI
st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at top, #1f1c2c, #928dab);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Title */
h1 {
    text-align: center;
    font-size: 44px;
    font-weight: bold;
    background: linear-gradient(90deg, #00f2fe, #4facfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Glass Card */
.card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 25px;
    margin: 20px 0;
    backdrop-filter: blur(15px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 30px;
    padding: 10px 25px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
}

/* Inputs */
.stTextInput>div>div>input {
    border-radius: 15px;
    background: rgba(255,255,255,0.1);
    color: white;
    border: 1px solid #aaa;
}

/* Metrics */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 15px;
}

/* Alerts */
.stSuccess, .stError, .stWarning {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1>🧬 SECURE MEDICAL DATA SHARING SYSTEM</h1>
<p style='text-align:center; color:#ddd;'>
Intelligent Diagnosis • Secure Sharing • Blockchain Integrity
</p>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.stSpinner > div {
    border-top-color: #00e6e6 !important;
}
</style>
""", unsafe_allow_html=True)

    
# ---------------- LOGIN SYSTEM ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged" not in st.session_state:
    st.session_state.logged = False

if "otp" not in st.session_state:
    st.session_state.otp = None

# ---------------- LOGIN ----------------
if st.session_state.page == "login":

    # role = st.selectbox("Role", ["Doctor", "Patient", "Admin"])
    with st.form("login_form"):
        role = st.selectbox("Role", ["Doctor", "Patient", "Admin"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

    #if st.button("Login"):
    if login_btn:
        with st.spinner("Authenticating... 🔐"):
            time.sleep(2)
        if role == "Admin":
            if username == "admin" and password == "admin123":
                st.session_state.logged = True
                st.session_state.role = "Admin"
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error("Invalid Admin Credentials")
        user_role = login_user(username, password)
        if user_role == role:
            st.session_state.logged = True
            st.session_state.role = role
            st.session_state.username = username
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Invalid Credentials")

           

    if st.button("Register"):
        st.session_state.page = "register"
        st.rerun()

# ---------------- REGISTER ----------------
elif st.session_state.page == "register":

    role = st.selectbox("Role", ["Doctor", "Patient", "Admin"])
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")

    if st.button("Send OTP"):
        import random
        otp = random.randint(1000,9999)
        st.session_state.otp = otp
        st.success(f"OTP: {otp}")

    entered = st.text_input("Enter OTP")

    if st.button("Register"):
        if str(st.session_state.otp) == entered:
            register_user(username, password, role)
            st.success("Registered")
        else:
            st.error("Wrong OTP")

    if st.button("Back"):
        st.session_state.page = "login"
        st.rerun()

# ---------------- HOME ----------------
elif st.session_state.logged:
    menu = st.sidebar.selectbox("Navigation", ["Dashboard", "Upload", "Records", "Decrypt", "Gallery"])
    if menu == "Decrypt":
        decrypt_page.show()
        st.stop()

    if menu == "Gallery":
        show_gallery()
        st.stop()

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

    role = st.session_state.role

    # ---------------- PATIENT ----------------
    if role == "Patient":
        st.subheader("Patient Dashboard")

        pid = st.session_state.username
        st.write("Logged in as:", pid)

        
        st.subheader("👨‍⚕️ Doctor Visit History")
        logs = get_logs()
        found = False
        for log in logs:
            if pid in log:
                st.info(log)
                found = True
                if not found:
                    st.warning("No doctor visits yet")

        st.subheader("📅 Medical Timeline")
        recs = get_patient_records(pid)
        if recs:
            for r in recs:
                st.markdown(f"""
                            <div class="card">
                            <b>📅 Date:</b> {r.get('date','')} <br>
                            <b>👨‍⚕️ Doctor:</b> {r.get('doctor','')} <br>
                            <b>🧠 Diagnosis:</b> {r.get('scan','')} <br>
                            <b>⚠️ Risk:</b> {r.get('risk','')}
                            </div>
                            """, unsafe_allow_html=True)
            st.warning("No history found")
        st.subheader("🤖 AI Medical Assistant")
        user_msg = st.text_input("Ask Medical Question")
        if st.button("Ask AI"):
            reply = get_bot_response(user_msg)
            st.success(reply)

        if st.button("Fetch"):
            recs = get_patient_records(pid)

            if not recs:
                st.error("No records found")
            else:
                for r in recs:
                    st.write("IPFS Hash:", r["ipfs_hash"])
                    st.write("Transaction:", r["transaction"])
    

    # ---------------- ADMIN ----------------                
    elif role == "Admin":

        st.subheader("📊 Analytics")
        recs = get_patient_records("all")

        search = st.text_input("Search Patient ID", key="admin_search")
        if search:
            recs = [r for r in recs if r['pid'].lower() == search.lower()]


        risk_count = {"Low":0, "Medium":0, "High":0}
        for r in recs:
            risk = r.get("risk", "Low")
            if "Low" in risk:
                risk_count["Low"] += 1
            elif "Medium" in risk:
                risk_count["Medium"] += 1
            else:
                risk_count["High"] += 1
        st.bar_chart(risk_count)



        st.warning("Admin Access Only 🔐")
        
        st.subheader("📜 Access Logs")
        logs = get_logs()
        if logs:
            for log in logs:
                st.code(log)
        else:
            st.warning("No logs found")

        st.subheader("👑 Admin Dashboard")
        patients, records = get_stats()
        c1, c2 = st.columns(2)
        c1.metric("Total Patients", patients)
        c2.metric("Total Records", records)
        
        st.success("System Running Securely ✅")
        
        st.subheader("All Records")
        
        recs = get_patient_records("all")
        search = st.text_input("Search Patient ID")
        filtered = recs
        if search.strip() != "":
            filtered = [r for r in recs if search.lower() in r['pid'].lower()]
            if not recs:
                st.warning("No records in database")
            elif not filtered:
                st.warning("No matching records found")
            else:
                for r in filtered:
                    

                    st.markdown(f"""
                    <div class="card">
                                <b>👤 Patient:</b> {r['pid']} <br>
                                <b>👨‍⚕️ Doctor:</b> {r.get('doctor','')} <br>
                                <b>📅 Date:</b> {r.get('date','')} <br>
                                <b>🧠 Scan:</b> {r.get('scan','')} <br>
                                <b>⚠️ Risk:</b> {r.get('risk','')} <br>
                                <b>🌐 IPFS:</b> {r.get('ipfs_hash','')} <br>
                                <b>⛓ TX:</b> {r.get('transaction','')}
                     </div>
                    """, unsafe_allow_html=True)

                    st.write(f"IPFS: {r['ipfs_hash']}")
                    st.write(f"TX: {r['transaction']}")
                    st.write("---")   

        if filtered:
            for i, r in enumerate(filtered):
                st.write(f"Patient: {r['pid']}")
                st.write(f"IPFS: {r['ipfs_hash']}")
                st.write(f"TX: {r['transaction']}")

        # 🔥 IMPORTANT FIX (unique key)
                if st.button(f"Delete {r['pid']}", key=f"delete_{r['pid']}_{i}"):
                    delete_record(r['pid'])
                    st.success(f"{r['pid']} deleted successfully")
                    st.rerun()
                st.write("---")

          # confirmation UI
                if "delete_id" in st.session_state:
                    st.warning(f"Are you sure to delete {st.session_state['delete_id']}?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Yes Delete"):
                            delete_record(st.session_state["delete_id"])
                            st.success("Deleted Successfully ✅")
                            del st.session_state["delete_id"]
                            st.rerun()
                    with col2:
                        if st.button("Cancel"):
                            del st.session_state["delete_id"]
                        else:
                            st.warning("No records found")
    
    # ---------------- DOCTOR ----------------
    elif role == "Doctor":

        # ---------------- DASHBOARD ----------------
        if menu == "Dashboard":
            st.subheader("📊 Doctor Dashboard")
            patients, records = get_stats()
            st.bar_chart([patients, records])
            c1, c2 = st.columns(2)
            c1.metric("Patients", patients)
            c2.metric("Records", records)
            if is_connected():
                st.success("✅ Blockchain Connected")
            else:
                st.error("❌ Blockchain Not Connected")

# ---------------- UPLOAD ----------------

        elif menu == "Upload":
            st.subheader("📤 Upload Scan")

# ---------------- RECORDS ----------------

        elif menu == "Records":
            st.subheader("📁 Patient Records")
            recs = get_patient_records("all")
            for r in recs:
                for r in recs:
                    st.write(f"👤 {r.get('pid', 'Unknown')}")
                    st.write(f"🧠 {r.get('scan', 'No Scan Data')}")
                    st.write(f"⚠️ {r.get('risk', 'No Risk Data')}")
                    st.write("---")

# ---------------- DECRYPT ----------------
        elif menu == "Decrypt":
            decrypt_page.show()
            st.stop()        

        # PDF
        def generate_pdf(pid, scan, hashv, tx, risk):
            file = "report.pdf"
            doc = SimpleDocTemplate(file)
            styles = getSampleStyleSheet()
            content = []
            # HEADER
            content.append(Paragraph(
                "🧬 SECURE MEDICAL DIAGNOSTIC REPORT",
                styles["Title"]
                ))

            content.append(Spacer(1, 20))
            # HOSPITAL DETAILS
            content.append(Paragraph(
                "<b>Hospital:</b> TRICHY MHPR HOSPITAL",
                styles["Normal"]
                ))
            content.append(Paragraph(
                "<b>Doctor Name:</b> Dr. Prasanth",
                styles["Normal"]
                ))
            content.append(Paragraph(
                f"<b>Generated Date:</b> {datetime.now().strftime('%d-%m-%Y')}",
                styles["Normal"]
                ))
            content.append(Paragraph(
                f"<b>Generated Time:</b> {datetime.now().strftime('%I:%M %p')}",
                styles["Normal"]
                ))
            content.append(Spacer(1, 15))
            # PATIENT DETAILS
            content.append(Paragraph(
                "<b>========= PATIENT DETAILS =========</b>",
                styles["Heading2"]
                ))
            content.append(Paragraph(
                f"<b>Patient ID:</b> {pid}",
                styles["Normal"]
                ))
            content.append(Paragraph(
                f"<b>Scan Result:</b> {scan}",
                styles["Normal"]
                ))
            content.append(Paragraph(
                f"<b>Risk Level:</b> {risk}",
                styles["Normal"]
                ))
            content.append(Spacer(1, 15))
              # SECURITY DETAILS
            content.append(Paragraph(
                "<b>========= SECURITY DETAILS =========</b>",
                styles["Heading2"]
                ))
            content.append(Paragraph(
                f"<b>IPFS Hash:</b> {hashv}",
                styles["Normal"]
                ))
            content.append(Paragraph(
                f"<b>Blockchain Transaction:</b> {tx}",
                styles["Normal"]
                ))
            content.append(Spacer(1, 20))
            # FINAL STATUS
            content.append(Paragraph(
                "✅ Report Verified and Secured using Blockchain + AES Encryption",
                styles["Normal"]
                ))

            content.append(Spacer(1, 25))

    # FOOTER
            content.append(Paragraph(
                "Doctor Signature: ____________________",
                styles["Normal"]
                ))

            content.append(Paragraph(
                "Authorized Medical AI System",
                styles["Italic"]
                ))
            doc.build(content)
            with open(file, "rb") as f:
                return f.read()

        # ROI DETECTION (UNCHANGED)
        def detect_brain(path):
            img = cv2.imread(path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            thresh = cv2.adaptiveThreshold(
                blur, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV,
                11, 2
                )
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            print("Contours:", len(contours))
            found = False
            for cnt in contours:
                area = cv2.contourArea(cnt)
                print("Area:", area)
                if area > 150:   # 🔥 very important change
                    found = True
                    x,y,w,h = cv2.boundingRect(cnt)
                    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
                    (cx, cy), radius = cv2.minEnclosingCircle(cnt)
                    cv2.circle(img, (int(cx), int(cy)), int(radius), (0,0,255), 2)
                    cv2.putText(img, "Tumor", (x,y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
            if not found:
                print("⚠️ No tumor region detected")
            return img, thresh
            
            


        def detect_chest(path):
            img = cv2.imread(path)
            original = img.copy()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            edges = cv2.Canny(blur, 30, 120)
            kernel = np.ones((3,3), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=2)
            
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                print("Area:", area)
                if area > 800:
                    x,y,w,h = cv2.boundingRect(cnt)
                    
                    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
                    cv2.putText(img, "Lung Region", (x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
                    
                    return img


        def detect_bone(path):
            img = cv2.imread(path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 80, 200)
            kernel = np.ones((3,3), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=1)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                print("Area:", area)
                if area > 300:
                    x,y,w,h = cv2.boundingRect(cnt)
                    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                    cv2.putText(img, "Bone Area", (x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                    
                    return img

        # UPLOAD
        
        pid = st.text_input("Patient ID")
        file = st.file_uploader("Upload Image")
        

        if file and pid:
            doctor_name = st.session_state.username
            log_access(doctor_name, pid)

            path = "temp.jpg"
            with open(path,"wb") as f:
                f.write(file.read())

            
            st.image(path)
            
            

            #  NEW AI DETECTION
        
            result_label, confidence = predict_image(path)
            scan = result_label
            st.success(f"🧠 Result: {scan}")
            try:
                engine.say(scan)
                engine.startLoop(False)
            except:
                pass

            st.info(f"📊 Confidence: {round(confidence*100,2)}%")
          
            confidence = float(confidence) * 100
            st.write(f"Confidence: {round(confidence,2)}%")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.bar(["Confidence"], [confidence])
            ax.set_ylim(0,100)
            st.pyplot(fig)

            result = None
            data = None
            
            if "Brain" in scan:
                result = segment_tumor(path)
                data = result.tobytes()
            
            elif "Chest" in scan:
                result = detect_chest(path)
                data = result.tobytes()
                st.success("🫁 Lung region highlighted")
            
            elif "Bone" in scan:
                result = detect_bone(path)
                data = result.tobytes()
                st.success("🦴 Bone structure highlighted")
            
            elif "Skin" in scan:
                result = cv2.imread(path)
                data = result.tobytes()
                st.success("🧴 Skin analysis done")


            if result is None:
                result = cv2.imread(path)
            if data is None:
                data = result.tobytes()
            
            heatmap_img = apply_heatmap(result.copy())
            result = heatmap_img
            
            
            #  redraw contours AFTER heatmap (IMPORTANT FIX)
            gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) > 0:
                largest = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest)
                if area > 300:   #  only big tumor
                    x,y,w,h = cv2.boundingRect(largest)
                    cv2.rectangle(result, (x,y), (x+w,y+h), (0,255,255), 4)
                    (cx, cy), r = cv2.minEnclosingCircle(largest)
                    cv2.circle(result, (int(cx), int(cy)), int(r), (0,0,255), 4)
            

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original Image")
                st.image(path)
            
            with col2:
                st.subheader("Processed Image")
                st.image(result)
            heatmap_img = apply_heatmap(result)
            st.subheader(" Heatmap View")
            st.image(heatmap_img)
            
            st.image(result)
            st.success("🔴 Tumor region highlighted")
        
            # ENCRYPT
            dna = dna_encode(data)
            
            password = str(random.randint(100000,999999))
            aes_encrypted = encrypt_aes(dna.encode(), password)
            enc2 = encrypt_data(aes_encrypted)

            enc_path = f"encrypted_storage/{pid}_encrypted.bin"
            with open(enc_path, "wb") as f:
                f.write(enc2)

            # create encrypted preview image
            enc_array = np.frombuffer(enc2[:30000], dtype=np.uint8)

            size = int(np.sqrt(len(enc_array)))
            enc_array = enc_array[:size*size]
            enc_img = enc_array.reshape((size, size))
            st.subheader("🔐 Encrypted Image Preview")
            st.image(enc_img, clamp=True)

            # create encrypted filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            enc_filename = f"encrypted_files/{pid}_{timestamp}.bin"

            # save encrypted file
            with open(enc_filename, "wb") as f:
                f.write(enc2)
            st.success("🔐 Encrypted file stored successfully!")
            st.info(f"📁 Stored at: {enc_filename}")

            st.warning(f"🔑 Save this Key: {password}")
            with open(enc_filename, "rb") as f:
                st.download_button(
                    label="⬇ Download Encrypted File",
                    data=f,
                    file_name=os.path.basename(enc_filename),
                    mime="application/octet-stream"
                )
                st.subheader("🔒 Encrypted Preview")
                st.code(enc2[:200])

            final_hash = hashlib.sha256(enc2).hexdigest()

            tx = store_hash(final_hash)
            #ipfs_hash = upload_to_ipfs(path)
            ipfs_hash = upload_to_ipfs(enc_filename)

            st.success(f"IPFS: {ipfs_hash}")

            if "Abnormal" in scan:
                st.error("⚠️ Possible abnormality detected!")
                risk = "High Risk 🔴"
            else:
                risk = "Low Risk 🟢"
            st.warning(f"Risk: {risk}")

            doctor = st.session_state.username
            date = datetime.now().strftime("%Y-%m-%d %H:%M")
            add_patient_record(pid, ipfs_hash, tx, scan, risk, doctor, date)


            st.success("Encrypted + Stored")
            st.subheader("🔐 Encrypted File Preview")
            st.code(enc_path)
            st.info("Encrypted medical data stored securely")
            

            # 🔥 NEW FEATURE ADDED (ENCRYPTED PDF)
            def generate_encrypted_pdf(enc_data):
                file = "encrypted_report.pdf"
                doc = SimpleDocTemplate(file)
                styles = getSampleStyleSheet()

                content = []
                content.append(Paragraph("ENCRYPTED MEDICAL DATA", styles["Title"]))

                enc_text = str(enc_data[:500])
                content.append(Paragraph(enc_text, styles["Normal"]))

                doc.build(content)

                with open(file, "rb") as f:
                    return f.read()

            enc_pdf = generate_encrypted_pdf(enc2)

            st.download_button(
                label="⬇ Download Encrypted PDF",
                data=enc_pdf,
                file_name="encrypted_data.pdf",
                mime="application/pdf"
            )

            

            pdf = generate_pdf(pid, scan, ipfs_hash, tx, risk)

            email = st.text_input("Enter Patient Email")
            if st.button("📧 Send Report Email"):
                if email:
                    send_email(
                        to_email=email,
                        subject="Your Medical Report",
                        body=f"Hello {pid}, your medical report is ready.",
                        attachment=pdf
                        )
                    st.success("Email Sent Successfully ✅")
                else:
                    st.error("Enter email first")


            st.download_button(
                label="📄 Download Medical Report",
                data=pdf,
                file_name="medical_report.pdf",
                mime="application/pdf"
                )
            
            
else:
    st.warning("Please login first")