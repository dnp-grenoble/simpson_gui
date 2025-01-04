import streamlit as st

col1, col2, col3 = st.columns(3,vertical_alignment="bottom", gap="medium")
with col1:
    st.image('resources/dnp_grenoble_logo.png', use_container_width=True)
with col2:
    st.image('resources/python.png', use_container_width=True)
with col3:
    st.image('resources/streamlit.png', use_container_width=True)


st.markdown('''**Welcome to the SIMPSON GUI**  

This interface is designed to help generate SIMPSON simulation files. 

*Helpful Features*


- You can input distances for dipoles. 
- Use an XYZ file for generating dipolar coupling. 
- It provides functionality to visualize powder files.
- Multi select method for propagators.

Please note that the generated simulation files serve as guides. You are encouraged to modify them as needed to suit your requirements. If you encounter any errors, feel free to reach out. However, I cannot take responsibility for simulations not working as intended. For the best experience, consider following official courses or tutorials available on the [SIMPSON website]().
### Helpful Publications:


1. Bak, Mads, Jimmy T. Rasmussen, and Niels Chr Nielsen. ‘SIMPSON: A General Simulation Program for Solid-State NMR Spectroscopy’. Journal of Magnetic Resonance 147, no. 2 (December 2000): 296–330. https://doi.org/10.1006/jmre.2000.2179.
2. Juhl, Dennis W., Zdeněk Tošner, and Thomas Vosegaard. ‘Versatile NMR Simulations Using SIMPSON’. In Annual Reports on NMR Spectroscopy, 100:1–59. Elsevier, 2020. https://doi.org/10.1016/bs.arnmr.2019.12.001.
3. Tošner, Zdeněk, Rasmus Andersen, Baltzar Stevensson, Mattias Edén, Niels Chr Nielsen, and Thomas Vosegaard. ‘Computer-Intensive Simulation of Solid-State NMR Experiments Using SIMPSON’. Journal of Magnetic Resonance 246 (September 2014): 79–93. https://doi.org/10.1016/j.jmr.2014.07.002.
4. Vosegaard, Thomas, Anders Malmendal, and Niels C Nielsen. ‘The Flexibility of SIMPSON and SIMMOL for Numerical Simulations in Solid-and Liquid-State NMR Spectroscopy’. Monatshefte f?R Chemie / Chemical Monthly 133, no. 12 (1 December 2002): 1555–74. https://doi.org/10.1007/s00706-002-0519-2.

### Upcoming Features:
The pulse sequence and main section will be added soon.
### Additional Resources:
You can explore more SIMPSON-related files in our GitHub repository:
[SIMPSON GitHub Repository](https://github.com/dnp-grenoble/simpson)
''')