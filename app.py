import streamlit as st
from zipfile import ZipFile
import io
import difflib
from zip_comparator import compare_zips

st.set_page_config(page_title="ZIP File Comparison Tool", layout="wide")
st.title("ZIP File Comparison Tool")
st.write("Upload two ZIP files to compare their contents and structure.")

col1, col2 = st.columns(2)
with col1:
    zip1_file = st.file_uploader("Upload First ZIP File", type=['zip'], key='zip1')
with col2:
    zip2_file = st.file_uploader("Upload Second ZIP File", type=['zip'], key='zip2')

if zip1_file and zip2_file:
    st.subheader("Comparison Results")
    
    zip1_bytes = io.BytesIO(zip1_file.read())
    zip2_bytes = io.BytesIO(zip2_file.read())
    
    results = compare_zips(zip1_bytes, zip2_bytes)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Files only in ZIP 1", len(results['files_only_in_zip1']))
    col2.metric("Files only in ZIP 2", len(results['files_only_in_zip2']))
    col3.metric("Common Files", len(results['common_files']))
    col4.metric("Files with Different Content", len(results['files_with_different_content']))
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"ZIP 1: {zip1_file.name}")
        st.write(f"Total Files: {results['zip1_total_files']}")
        st.write(f"Total Directories: {results['zip1_total_dirs']}")
        
        with st.expander(f"Files only in ZIP 1 ({len(results['files_only_in_zip1'])})"):
            for file in results['files_only_in_zip1']:
                st.text(file)
        
        with st.expander(f"Directories only in ZIP 1 ({len(results['dirs_only_in_zip1'])})"):
            for dir in results['dirs_only_in_zip1']:
                st.text(dir)
    
    with col2:
        st.subheader(f"ZIP 2: {zip2_file.name}")
        st.write(f"Total Files: {results['zip2_total_files']}")
        st.write(f"Total Directories: {results['zip2_total_dirs']}")
        
        with st.expander(f"Files only in ZIP 2 ({len(results['files_only_in_zip2'])})"):
            for file in results['files_only_in_zip2']:
                st.text(file)
        
        with st.expander(f"Directories only in ZIP 2 ({len(results['dirs_only_in_zip2'])})"):
            for dir in results['dirs_only_in_zip2']:
                st.text(dir)
    
    st.markdown("---")
    st.subheader(f"Common Files ({len(results['common_files'])})")
    with st.expander("View all common files"):
        for file in results['common_files']:
            st.text(file)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Files with Identical Content ({len(results['files_with_identical_content'])})")
        with st.expander("View files with identical content"):
            for file in results['files_with_identical_content']:
                st.text(file)

    with col2:
        st.subheader(f"Files with Different Content ({len(results['files_with_different_content'])})")
        with st.expander("View files with different content"):
            for file in results['files_with_different_content']:
                if st.button(f"📄 {file}", key=f"diff_{file}"):
                    st.session_state['selected_file'] = file
                    st.session_state['zip1_name'] = zip1_file.name
                    st.session_state['zip2_name'] = zip2_file.name
                    st.session_state['zip1_bytes'] = zip1_bytes
                    st.session_state['zip2_bytes'] = zip2_bytes
                    st.rerun()

    # Show diff if a file is selected
    if 'selected_file' in st.session_state and st.session_state['selected_file']:
        st.markdown("---")
        st.subheader(f"File Comparison: {st.session_state['selected_file']}")

        try:
            # Read file contents from both zips
            with ZipFile(st.session_state['zip1_bytes'], 'r') as zip1_ref, \
                 ZipFile(st.session_state['zip2_bytes'], 'r') as zip2_ref:

                with zip1_ref.open(st.session_state['selected_file']) as file1, \
                     zip2_ref.open(st.session_state['selected_file']) as file2:

                    content1 = file1.read().decode('utf-8', errors='replace')
                    content2 = file2.read().decode('utf-8', errors='replace')

                    # Try to display as text diff
                    lines1 = content1.splitlines(keepends=True)
                    lines2 = content2.splitlines(keepends=True)

                    diff = difflib.unified_diff(
                        lines1,
                        lines2,
                        fromfile=f"{st.session_state['zip1_name']}/{st.session_state['selected_file']}",
                        tofile=f"{st.session_state['zip2_name']}/{st.session_state['selected_file']}",
                        lineterm=''
                    )

                    diff_text = ''.join(diff)

                    st.subheader("Unified Diff")
                    st.code(diff_text, language='diff')

                    if st.button("Close Diff View"):
                        st.session_state.pop('selected_file', None)
                        st.session_state.pop('zip1_bytes', None)
                        st.session_state.pop('zip2_bytes', None)
                        st.rerun()

        except Exception as e:
            st.error(f"Error reading file contents: {str(e)}")
            if st.button("Close"):
                st.session_state.pop('selected_file', None)
                st.rerun()

st.markdown("---")
st.write("Ready to use on Streamlit Community Cloud!")
