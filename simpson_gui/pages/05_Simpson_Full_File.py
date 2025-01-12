import streamlit as st
from streamlit_ace import st_ace

def full_file():
    full_file = " "
    if "simpson_spinsys" in st.session_state :
        full_file = st.session_state[ 'simpson_spinsys' ] + "\n\n"

    if "par_code" in st.session_state :
        full_file += st.session_state[ 'par_code' ] + "\n\n"

    if "pulse_sequence" in st.session_state :
        full_file += st.session_state[ 'pulse_sequence' ] + "\n\n"

    if "main_code" in st.session_state :
        full_file += st.session_state[ 'main_code' ] + "\n\n"

    return full_file

def main():
    st.title("Full Simulation File")
    st.divider()
    simpson_file_contents = full_file()
    response_code = st_ace(simpson_file_contents, language="tcl", height=400, theme="solarized_dark")
    st.code(response_code, language="tcl")

    st.download_button(
        label="Download File",
        data=response_code,
        file_name="simpson_file.in",
        mime="in")



if __name__ == '__main__' :
    main()