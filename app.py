import streamlit as st
import pandas as pd
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import sys
import os


st.set_page_config(page_title='Data Profiler', layout='wide')
def validate_file(file):
    filename = file.name
    name, ext = os.path.splitext(filename)
    if ext in ('.csv', '.xlsx'):
        return ext
    else:
        return False
def get_filesize(file):
    
    sz_bytes = sys.getsizeof(file)
    sz_mb = sz_bytes/(1024**2)
    return sz_mb
# sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload .csv, .xlsx files < 10 MB")
    if uploaded_file is not None:
        st.write('Modes of Operation')
        minimal  = st.checkbox('Do you want minimal report?')
        display_mode = st.radio('Display Mode:',options=('Primary', 'Dark', 'Orange'))
        if display_mode == 'Dark':
            dark = True
            org = False
        elif display_mode == 'Orange':
            dark = False
            org = True
        else:
            dark = False
            org = False

if uploaded_file is not None:
    ext = validate_file(uploaded_file)
    if ext:
        filesize = get_filesize(uploaded_file)
        st.info(filesize)
        if filesize <= 8:

            if ext == '.csv':
                df = pd.read_csv( uploaded_file)
            else:
                xl_fl = pd.ExcelFile(uploaded_file)
                sheet_tuple = tuple(xl_fl.sheet_names)
                sheet_name = st.sidebar.selectbox('select the sheet', sheet_tuple)
                df = xl_fl.parse(sheet_name)

        # st.dataframe(df.head())
        #generate report
            with st.spinner('Generating Report'):
                pr = ProfileReport(df, minimal= minimal, dark_mode=dark, orange_mode=org)

            st_profile_report(pr)
        else:
            st.error('Max file size exceeded (> 8 MB)')
    else:
        st.error("Only csv and excel file permitted")
else:
    st.title('Data Profiler')
    st.info('Uplaod your data using the panel on the left to get started!')