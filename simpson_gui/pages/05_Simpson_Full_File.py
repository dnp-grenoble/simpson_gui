import streamlit as st

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
    st.code(simpson_file_contents, language="tcl")
    st.download_button(label="Download SIMPSON file",
                       data = simpson_file_contents,
                       file_name = "simpson_file.in",
                       mime="in")

if __name__ == '__main__' :
    main()