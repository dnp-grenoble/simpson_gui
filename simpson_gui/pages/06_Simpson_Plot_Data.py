import streamlit as st
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def plot_data() :
    file_uploaded = st.file_uploader ( "Upload the data file" )
    if file_uploaded is not None :
        time_or_freq = st.selectbox ( "Time domain or frequency domain?" , [ "freq" , "time" ] , index=None )
        data = np.loadtxt ( file_uploaded )

        plot_options = st.multiselect ( "Plot options" , [ "Real", "Imaginary"] , default=None )


        x = data[ : , 0 ]
        re = data[ : , 1 ]
        im = data[ : , 2 ]
        if plot_options is not None :
            # Determine how many rows we need based on selection
            cols = len(plot_options)

            # Create subplots dynamically based on rows
            fig = make_subplots (
                rows=1 , cols=cols , shared_xaxes=True ,
                subplot_titles=plot_options
            )

            # Two boolean flags for displaying Real/Imaginary parts
            display_real = "Real" in plot_options
            display_imag = "Imaginary" in plot_options

            # Plot Real Part (if selected)
            if display_real :
                fig.add_trace (
                    go.Scatter ( x=x , y=re , mode="lines" , name="Real" ) ,
                    row=1 , col=1
                )

            # Plot Imaginary Part (if selected)
            if display_imag :
                fig.add_trace (
                    go.Scatter ( x=x , y=im , mode="lines" , name="Imaginary" ) ,
                    col=(2 if display_real else 1) , row=1
                )

            # Update layout for "time" or "freq"
            fig.update_layout (
                title="Time Domain Plot" if time_or_freq == "time" else "Frequency Domain Plot" ,
                xaxis_title="Time (s)" if time_or_freq == "time" else "Frequency (Hz)" ,
                yaxis_title="Amplitude" ,
                showlegend=False
            )

            # Reverse x-axis for frequency domain (if frequency selected)
            if time_or_freq == "freq" :
                fig.update_xaxes ( autorange="reversed" )

            # Display the plot
            st.plotly_chart ( fig , use_container_width=True )







def main():
    st.title("Plot Data")
    plot_data()
    st.divider()

if __name__ == '__main__' :
    main()