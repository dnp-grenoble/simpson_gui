#%% Header files
import re
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import os

def zcw_sequence(n, zcw_type = 1) :
    """
    Generates ZCW sequence and computes orientation angles.
    Takes N (number of orientations) directly as input.

    Parameters:
        n (int): Number of orientations (direct input).
        zcw_type (float): Type parameter which modifies behavior (1, 0.5, or 0.25).

    Returns:
        tuple: (alpha, beta, gamma) NumPy arrays of angles.
    """
    # Match the `type` parameter
    if zcw_type == 1 :
        c = [ 1 , 2 , 1 ]
    elif zcw_type == 0.5 :
        c = [ -1 , 1 , 1 ]
    elif zcw_type == 0.25 :
        c = [ -1 , 1 , 4 ]
    else :
        raise ValueError ( "Unsupported ZCW type. Use 1, 0.5, or 0.25." )

    # Use an approximate Fibonacci value for g2
    # g2 is typically g(M-2), but we use N to calculate an estimate
    g2 = int ( n / 2.618 )  # Use the golden ratio approximation for a balanced g2

    # Initialize output arrays
    beta = np.zeros ( n )
    alpha = np.zeros ( n )
    gamma = np.zeros ( n )  # Gamma is always 0.0

    # Loop to calculate alpha, beta, and gamma
    for m in range ( 1 , n + 1 ) :  # Loop from 1 to n (inclusive)
        beta[ m - 1 ] = (180 / np.pi) * np.arccos ( c[ 0 ] * (c[ 1 ] * ((m / n) % 1.0) - 1.0) )
        alpha[ m - 1 ] = (180 / np.pi) * 2.0 * np.pi * ((m * g2 / n) % 1.0) / c[ 2 ]
        gamma[ m - 1 ] = 0.0  # Gamma is always 0 in the original logic

    return alpha , beta


def repulsion_sequence(n) :
    script_dir = os.path.dirname ( __file__ )
    num_orientations_file = os.path.join ( script_dir , '../resources/repangles_num.txt' )
    num_orientations = np.loadtxt( num_orientations_file , dtype=float )

    alpha_file = os.path.join ( script_dir , '../resources/repangles_alpha.txt' )
    alpha_angles = np.loadtxt( alpha_file , dtype=float )

    beta_file = os.path.join ( script_dir , '../resources/repangles_beta.txt' )
    beta_angles = np.loadtxt ( beta_file , dtype=float )
    idx = np.where(num_orientations == n)[0]

    alpha_rep = alpha_angles[:, idx].flatten()
    beta_rep = beta_angles[:, idx].flatten()

    alpha_rep = alpha_rep[ np.flatnonzero( alpha_rep ) ]
    beta_rep = beta_rep[(np.flatnonzero(beta_rep))]

    alpha_rep = np.where( alpha_rep < 0 , alpha_rep , 360.0 + alpha_rep )
    beta_rep = np.where( beta_rep < 0 , beta_rep , 360.0 + beta_rep )

    return alpha_rep, beta_rep





def bcr_sequence(n) :
    """
    Generate BCR (Backus-Collins-Reinisch) sequence for powder averaging.

    Parameters:
        n (int): Number of orientations.

    Returns:
        np.ndarray: Array of angles (alpha, beta) in radians.
    """
    indices = np.arange ( 0 , n , dtype=float ) + 0.5
    phi = 2 * np.pi * indices / n  # Uniform distribution of azimuthal angle
    theta = np.arccos ( 1 - 2 * indices / n )  # Uniform distribution of polar angle
    return phi*180./np.pi , theta * 180./np.pi





def plot_points_on_sphere_with_plotly(theta , phi) :
    """
    Plot points on a sphere using Plotly based on theta and phi angles.
    """
    theta = theta * np.pi / 180.
    phi = phi * np.pi / 180.
    # Convert spherical coordinates to Cartesian
    x = np.sin ( theta ) * np.cos ( phi )
    y = np.sin ( theta ) * np.sin ( phi )
    z = np.cos ( theta )

    # Create sphere surface
    u = np.linspace ( 0 , 2 * np.pi , 100 )  # Azimuthal angles
    v = np.linspace ( 0 , np.pi , 100 )  # Polar angles
    x_sphere = np.outer ( np.sin ( v ) , np.cos ( u ) )
    y_sphere = np.outer ( np.sin ( v ) , np.sin ( u ) )
    z_sphere = np.outer ( np.cos ( v ) , np.ones_like ( u ) )

    # Create Plotly figure
    fig = go.Figure ()

    # Add the sphere surface
    fig.add_trace ( go.Surface (
        x=x_sphere ,
        y=y_sphere ,
        z=z_sphere ,
        colorscale='Blues' ,
        opacity=0.5 ,
        showscale=False
    ))
    # Add the plane (let's say at z=0.5, define its size)
    plane_z = 0.  # The Z-value where the plane will be placed
    plane_x , plane_y = np.meshgrid ( np.linspace ( -1 , 1 , 100 ) , np.linspace ( -1 , 1 , 100 ) )  # Define a meshgrid
    plane_z_values = np.full ( plane_x.shape , plane_z )  # All Z-values will have the value 0.5

    # Add the plane to the figure
    fig.add_trace ( go.Surface (
        x=plane_x ,
        y=plane_y ,
        z=plane_z_values ,
        colorscale='Reds' ,  # Give a different color to the plane
        opacity=0.2 ,
        showscale=False
    ) )

    # Add the plane (let's say at z=0.5, define its size)
    plane_y = 0.  # The y-value where the plane will be placed
    plane_x , plane_z = np.meshgrid ( np.linspace ( -1 , 1 , 100 ) , np.linspace ( -1 , 1 , 100 ) )  # Define a meshgrid
    plane_y_values = np.full ( plane_x.shape , plane_y )  # All Z-values will have the value 0.5

    # Add the plane to the figure
    fig.add_trace ( go.Surface (
        x=plane_x ,
        z=plane_z ,
        y=plane_y_values ,
        colorscale='Reds' ,  # Give a different color to the plane
        opacity=0.2 ,
        showscale=False
    ) )

    # Add data points on the sphere
    fig.add_trace ( go.Scatter3d (
        x=x ,
        y=y ,
        z=z ,
        mode='markers' ,
        marker=dict ( size=3 , color='MediumPurple' ) ,
        name='Points'
    ) )



    # Update layout
    fig.update_layout ( scene=dict (
        xaxis=dict ( visible=False ) ,
        yaxis=dict ( visible=False ) ,
        zaxis=dict ( visible=False ) ,
        aspectmode='data'
    ) )

    # Show plot
    st.plotly_chart ( fig )


def main () :
    option_of_field = st.selectbox ( "Field in MHz (1H) or T" ,
                                     ("MHz" , "Tesla") ,
                                     )
    if option_of_field == "MHz" :
        field = st.number_input ( "Enter the field in MHz" , value=400.0)
        latex_expr = "\\times 10^6"
        st.write(f"Proton Frequency = ${field}$ ${latex_expr}$ Hz")
    else :
        field = st.number_input ( "Enter the field in T" , value=9.4)
        latex_expr = "\\times 10^6"
        field = field * 42.58
        st.write ( f"Proton Frequency = ${field}$ ${latex_expr}$ Hz" )

    spinning_frequency = st.number_input ( "Spinning Frequency in Hz" , min_value=1 , max_value=500000 , value=10000 )

    options_crystal_file = [ "LEBoct31" , "alpha0beta0" , "alpha0beta90" , "bcr10" ,
                             "bcr100" , "bcr20" , "bcr200" , "bcr30" , "bcr40" , "bcr400" ,
                             "bcr50" , "bcr80" , "rep10" , "rep100" , "rep144" , "rep168" ,
                             "rep20" , "rep2000" , "rep256" , "rep30" , "rep320" , "rep66" ,
                             "rep678" , "repoct41" , "zcw143" , "zcw20" , "zcw232" , "zcw33" ,
                             "zcw376" , "zcw4180" , "zcw54" , "zcw615" , "zcw88" , "zcw986" ,
                             "zcw28656" ]
    powder_file = st.selectbox ( "Which powder averaging scheme?" , options_crystal_file ,
                                 index=None )
    if powder_file is not None :
        match = re.split ( r"([A-Za-z]+)([0-9]+)" , powder_file )
        if match[ 1 ] == 'bcr' :
            alpha , beta = bcr_sequence ( int ( match[ 2 ] ) )
            plot_points_on_sphere_with_plotly ( alpha , beta )
        elif match[ 1 ] == 'zcw' :
            alpha , beta = zcw_sequence ( int ( match[ 2 ] ) )
            plot_points_on_sphere_with_plotly ( alpha , beta )
        elif match[ 1 ] == 'rep' :
            alpha , beta = repulsion_sequence ( float ( match[ 2 ] ) )
            plot_points_on_sphere_with_plotly ( alpha , beta )
        elif powder_file == "alpha0beta0":
            plot_points_on_sphere_with_plotly ( np.zeros(100) , np.zeros(100))
        elif powder_file == "alpha0beta90":
            plot_points_on_sphere_with_plotly ( 90.0 * np.ones ( 100 ), np.zeros ( 100 )  )
        else :
            st.write ( 'Cannot generate figure'
                       )

    gamma_angles = st.number_input ("Number of gamma angles", min_value=0, max_value=512, value=8, format='%d')

    start_operator = st.text_input("Start Operator, can be In{p} p = x, y, z, p, m, c", value = "I1x")

    detect_operator = st.text_input("Detect Operator, can be In{p} p = x, y, z, p, m, c", value = "I1p")


    verbose = st.number_input("Verbose for the simulation", format='%d', value=1101)
    vb_text = '''
    The verbose entry takes up to eight zeroes or ones instructing SIMPSON to provide output about  
    1. The spin system
    2. The simulation progress
    3. Simulation information
    4. Start and detect operators
    5. Powder angles
    6. The rf averaging profile
    7. The acquisition block
    8. The averaging file.
    
    
    The above value 1101 asks SIMPSON to provide output about the spin system, the simulation progress, and the start- and detect operators
    '''
    st.markdown(vb_text)

    number_of_acq_points = st.number_input("Number of points to be detected", value=16, format='%d')

    sw = st.text_input("Spectral window", value="spin_rate")

    conjugate_fid = st.checkbox("Conjugate FID?", value=False)

    value_methods = ["direct", "freq", "gcompute", "dysev", "dysevr", "pade", "taylor", "cheby1", "cheby2"]
    method_of_sim = st.pills("Method of propagation", value_methods, selection_mode="multi")

    gen_str_method = ""
    for methods in method_of_sim:
        gen_str_method = gen_str_method + methods + " "

    script_dir = os.path.dirname ( __file__ )
    prop_image_file = os.path.join ( script_dir , '../resources/prop_methods.jpg' )


    st.image( prop_image_file, width=256, caption="Performance comparison of different strategies implemented in "
                                                              "SIMPSON for propagator calculation for one carbon and 1–9 protons"
                                                              "Tošner, Z. ‘Computer-Intensive Simulation of Solid-State NMR Experiments Using SIMPSON’. JMR 246 (2014): 79–93. https://doi.org/10.1016/j.jmr.2014.07.002."
             )

    par_code = (" par {  \n \t proton_frequency \t" + f"{float ( field ) * (10.0 ** 6):.4e} \n"
                "\t spinning_rate \t" + f"{spinning_frequency} \n"
                "\t crystal_file \t" + f"{powder_file} \n"
                "\t gamma_angles \t" + f"{gamma_angles} \n"
                "\t start_operator \t" + f"{start_operator} \n"
                "\t detect_operator \t" + f"{detect_operator} \n"
                "\t verbose \t" + f"{verbose} \n"
                "\t np \t" + f"{number_of_acq_points} \n"
                "\t sw \t" + f"{sw} \n"
                "\t conjugate_fid \t" + f"{conjugate_fid} \n"
                "\t method \t" + f"{gen_str_method} \n"
                "}"
                )
    st.divider()
    if st.button("Generate code"):
        st.code(par_code, language="Tcl")

if __name__ == '__main__':
    st.title("To generate par section of SIMPSON")
    st.divider()
    main()