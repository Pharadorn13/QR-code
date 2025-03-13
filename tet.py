import streamlit as st
import pymysql
import io
import base64

# Create MySQL Connection
def create_connection():
    return pymysql.connect(
        host="10.207.1.84",
        port=3306,
        user="root",
        password="admin",
        database="raw",
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to Save PDF to MySQL
def save_pdf_to_mysql(file):
    conn = create_connection()
    cursor = conn.cursor()
    binary_data = file.read()
    query = "INSERT INTO pdf_files (filename, file_data) VALUES (%s, %s)"
    cursor.execute(query, (file.name, binary_data))
    conn.commit()
    cursor.close()
    conn.close()
    return f"{file.name} uploaded successfully!"

# Function to Retrieve PDF from MySQL
def retrieve_pdf_from_mysql(pdf_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT filename, file_data FROM pdf_files WHERE id = %s"
    cursor.execute(query, (pdf_id,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    return record

# Streamlit UI
st.title("PDF Storage in MySQL")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_file:
    message = save_pdf_to_mysql(uploaded_file)
    st.success(message)

# Retrieve PDFs
st.subheader("Retrieve PDF from MySQL")
pdf_id = st.number_input("Enter PDF ID:", min_value=1, step=1)
if st.button("Retrieve PDF"):
    record = retrieve_pdf_from_mysql(pdf_id)
    if record:
        filename, binary_data = record["filename"], record["file_data"]
        
        # Show Download Button
        st.download_button(
            label="Download PDF",
            data=binary_data,
            file_name=filename,
            mime="application/pdf"
        )
        
        # Display PDF using iframe
        st.write("### PDF Preview:")
        base64_pdf = base64.b64encode(binary_data).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.error("PDF not found!")
