import streamlit as st
import pdfplumber
import pandas as pd
from io import StringIO
from Extractor_ import extract_data_from_pdf


def extract_images_from_pdf(file):
    images = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            im = page.to_image(resolution=300)
            images.append(im)
    return images

def set_page_title(title):
    st.sidebar.markdown(unsafe_allow_html=True, body=f"""
        <iframe height=0 srcdoc="<script>
            const title = window.parent.document.querySelector('title') \
                
            const oldObserver = window.parent.titleObserver
            if (oldObserver) {{
                oldObserver.disconnect()
            }} \

            const newObserver = new MutationObserver(function(mutations) {{
                const target = mutations[0].target
                if (target.text !== '{title}') {{
                    target.text = '{title}'
                }}
            }}) \

            newObserver.observe(title, {{ childList: true }})
            window.parent.titleObserver = newObserver \

            title.text = '{title}'
        </script>" />
    """)

def main():
    st.set_page_config(layout="wide")
    set_page_title("PDF Extractor")
    st.title("PDF Extractor")
    # hide_steamlit_style = "<style>[data-testid='stToolbar']{visibility:hidden !important} footer{visibility: hidden !important}</style>"
    # st.write(hide_steamlit_style)
    col1, col2 = st.columns([1, 1])

    with col1.container(height=800, border=False):
        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
        if uploaded_file is not None:
            data = extract_data_from_pdf(uploaded_file)
            pdf_images = extract_images_from_pdf(uploaded_file)
            st.subheader("Edited Text for the PDF:")

            # Beautify data dictionary in form format
            with st.container(border=True):
                for key, value in data.items():
                    # print(f"{key}:{type(value)}")
                    if isinstance(value, list):
                        data[key] = st.selectbox(key, value)
                    else:
                        data[key] = st.text_area(key, value=value, height=2)
            # form_submit_button = st.form_submit_button(label='Submit')

            # Download button for the data
            csv_data = pd.DataFrame(data.items(), columns=['Page', 'Text'])
            csv_data_io = StringIO()
            csv_data.to_csv(csv_data_io, index=False)
            csv_data_io.seek(0)
            st.download_button(
                label="Download Data as CSV",
                data=csv_data_io.getvalue(),
                file_name='pdf_data.csv',
                mime='text/csv'
            )

    with col2.container(height=900, border=False):
        if uploaded_file is not None and len(pdf_images) > 0:
            # Convert PageImage to PIL Image
            for i, image in enumerate(pdf_images, start=1):
                st.image(
                    image.original, caption=f"Page {i}", width=720)


if __name__ == "__main__":
    main()
