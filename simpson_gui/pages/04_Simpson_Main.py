import streamlit as st

def main():



    time_or_frequency = st.selectbox("Frequency domain or time domain?", ["fft", "time"], index = None)

    if time_or_frequency == "fft":
        text_time_or_frequency = " "
        zero_fill = st.number_input("Zero-filling factor", format="%d", value=1)
        lb = st.number_input("Line Broadening in Hz", format="%f", value=0.0)
        ratio_gaussian_lorentzian = st.number_input("Gaussian/Lorentzian Ratio", format="%d", max_value=1, min_value=0, value=0)
        text_time_or_frequency += f" fzerofill $f {zero_fill} \n \tfaddlb $f {lb} {ratio_gaussian_lorentzian}"
        text_time_or_frequency += "\n \t fft $f"
    else:
        text_time_or_frequency = " "

    save_text_option = "fsave $f $par(name).txt -xreim"

    main_code = f"""
        proc main {{}} {{
        global par
        set f [fsimpson]
        {text_time_or_frequency}
        {save_text_option}
        funload $f
        }}
    """

    st.code(main_code, language="tcl")

    st.session_state['main_code'] = main_code

if __name__ == '__main__' :
    st.title("Main Section of SIMPSON")
    st.divider()

    main()
    main_code_txt = st.text_area("Paste the main code here:", value=None)

    if st.button("Add to full code"):
        st.session_state['main_code'] = main_code_txt