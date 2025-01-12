import streamlit as st
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def plot_data() :
    file_uploaded = st.file_uploader ( "Upload the data file" )
    if file_uploaded is not None :
        time_or_freq = st.selectbox ( "Time domain or frequency domain?" , [ "freq" , "time" ] , index=0 )
        data = np.loadtxt ( file_uploaded )

        x = data[ : , 0 ]
        re = data[ : , 1 ]
        im = data[ : , 2 ]

        # Create subplots with 2 rows and 1 column
        fig = make_subplots ( rows=1 , cols=2 , shared_xaxes=True ,
                              subplot_titles=("Real" , "Imaginary") )

        # Add Real part to the first row
        fig.add_trace ( go.Scatter ( x=x , y=re , mode="lines" , name="Real" ) , row=1 , col=1 )

        # Add Imaginary part to the second row
        fig.add_trace ( go.Scatter ( x=x , y=im , mode="lines" , name="Imaginary" ) , row=1 , col=2 )

        # Update layout for time or frequency domain
        if time_or_freq == "time" :
            fig.update_layout (
                title="Time Domain Plot" ,
                xaxis_title="Time (s)" ,
                yaxis_title="Amplitude" ,
                showlegend=False
            )
        elif time_or_freq == "freq" :
            fig.update_layout (
                title="Frequency Domain Plot" ,
                xaxis_title="Frequency (Hz)" ,
                yaxis_title="Amplitude" ,
                showlegend=False
            )
            fig.update_xaxes ( autorange="reversed" )  # Reverse x-axis for frequency domain

        # Update axis labels for the subplots
        fig.update_xaxes ( title_text="Time (s)" if time_or_freq == "time" else "Frequency (Hz)" , row=2 , col=1 )
        fig.update_yaxes ( title_text="Amplitude (Real)" , row=1 , col=1 )
        fig.update_yaxes ( title_text="Amplitude (Imaginary)" , row=2 , col=1 )

        # Display the plot in Streamlit
        st.plotly_chart ( fig )







def main():
    st.title("Plot Data")
    plot_data()
    st.divider()

if __name__ == '__main__' :
    main()