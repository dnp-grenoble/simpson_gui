import streamlit as st

st.title("Main Section of SIMPSON")
st.divider()

time_or_frequency = st.selectbox("Frequency domain or time domain?", ["fft", "time"], index = None)
save_option = st.selectbox("Save as .txt or .spe", ["txt", "spe"], index=None)

if time_or_frequency == "fft":
    text_time_or_frequency = "fft $f"
else:
    text_time_or_frequency = " "

if save_option == "txt":
    save_text_option = "fsave $f $par(name).txt -xreim"
elif save_option == "spe":
    save_text_option = "fsave $f $par(name).spe"
else:
    save_text_option = "    "

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


