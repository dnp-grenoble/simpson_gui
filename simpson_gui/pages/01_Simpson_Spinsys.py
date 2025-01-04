#%% Header files
import numpy as np
import streamlit as st
import os
import pandas as pd
from scipy.spatial.transform import Rotation as Rot



#%% Functions
def dist2dipole(choice_nuc1 , choice_nuc2 , distance, table_of_nuclei) :
    """
    The function calculates the dipolar coupling in
    Hz for two nuclei
    :param table_of_nuclei:
    :param choice_nuc1: The nucleus should be of the format 1H, 13C etc.
    :param choice_nuc2: The nucleus should be of the format 1H, 13C etc.
    :param distance: The distance should be in Angstrom
    :return: Dipolar coupling between the two nuclei in Hz
    """
    gyr_ratio_m_hz_t = table_of_nuclei[ "GyrHz" ]
    name_nuc = table_of_nuclei[ "Name" ]
    pl = 6.62607015e-34 # Planck's constant
    nuc1idx = name_nuc[ name_nuc.str.match ( choice_nuc1 ) ].index
    nuc2idx = name_nuc[ name_nuc.str.match ( choice_nuc2 ) ].index

    gyr1 = gyr_ratio_m_hz_t[ nuc1idx[ 0 ] ] * 1e6
    gyr2 = gyr_ratio_m_hz_t[ nuc2idx[ 0 ] ] * 1e6

    dip = -1.0e-7 * (gyr1 * gyr2 * pl) / ((float ( distance ) * 1.0e-10) ** 3.0)
    return round ( dip , 2 )


# noinspection PyArgumentList
def angle_between_vectors(vec1 , vec2) :
    """
    The function calculates the Euler angles between two vectors
    in the zyz convention. The conventions can be found in scipy's transform module
    :param vec1: a vector of the format [i1, j1, k1]
    :param vec2: b vector of the format [i2, j2, k2]
    :return: a vector of three Euler angles connecting the two vectors
    """
    vec1 = vec1 / np.linalg.norm ( vec1 )
    vec2 = vec2 / np.linalg.norm ( vec2 )
    cp = np.cross ( vec1 , vec2 )
    dp = np.dot ( vec1 , vec2 )
    cosine_ang = dp
    ssc = np.array ( [ [ 0 , -cp[ 2 ] , cp[ 1 ] ] , [ cp[ 2 ] , 0 , -cp[ 0 ] ] , [ -cp[ 1 ] , cp[ 0 ] , 0 ] ] )
    rot_mat = np.identity ( 3 ) + ssc + np.dot ( ssc , ssc ) / (1 + cosine_ang)
    ff = Rot.from_matrix ( rot_mat )
    euler_angles = ff.as_euler ( 'zyz' , degrees='True' )
    return euler_angles

def xyz_file_to_dipolar_data(xyzfile , nuc, num_nuc_func, table_of_nuclei) :
    """
    The function takes an .xyz file of a molecular structure and calculates the
    dipolar coupling and Euler angle between the different nuclei in the principal axis frame.
    :param nuc: the list of nuclei chosen
    :param table_of_nuclei: The table containing all nuclear parameters
    :param xyzfile: Molecular structure file of the format .xyz
    :param num_nuc_func: nuber of nuclei
    :return: a pandas Dataframe containing the pair of nuclei, the dipolar coupling in Hz,
    and the Euler angles between the two tensors.
    """

    mol = pd.read_csv ( xyzfile , sep='\s+' , skiprows=2 , names=[ 'atom' , 'x' , 'y' , 'z' ] , index_col=False )
    if len ( mol ) != num_nuc_func :
        raise ValueError ( "The number of Nuclei do not match" )
    coord_xyz = mol[ [ 'x' , 'y' , 'z' ] ].to_numpy ()
    pl = 6.62607015e-34
    df_xyz_to_dip = pd.DataFrame ( columns=[ 'i' , 'j' , 'dip' , 'alpha' , 'beta' , 'gamma' ] )

    gyr_atom = np.zeros(len(nuc))

    for idx, nucleus in enumerate(nuc):
        gyr_atom[idx] = table_of_nuclei[table_of_nuclei.Name.isin([nucleus]) == True]['GyrHz'].values



    dist = np.zeros ( [ np.shape ( coord_xyz )[ 0 ] , np.shape ( coord_xyz )[ 0 ] ] )
    dip = np.zeros ( [ np.shape ( coord_xyz )[ 0 ] , np.shape ( coord_xyz )[ 0 ] ] )
    for idx in range ( 0 , np.shape ( coord_xyz )[ 0 ] ) :
        gyr1 = gyr_atom[ idx ] * 1e6
        for j in range ( idx + 1 , np.shape ( coord_xyz )[ 0 ] ) :
            dist[ idx ][ j ] = np.sqrt ( np.sum ( (coord_xyz[ idx ] - coord_xyz[ j ]) ** 2 ) )
            gyr2 = gyr_atom[ j ] * 1e6
            dip[ idx ][ j ] = -1e-7 * (gyr1 * gyr2 * pl) / ((dist[ idx ][ j ] * 1e-10) ** 3)

    for idx in range ( 0 , np.shape ( coord_xyz )[ 0 ] ) :
        for j in range ( idx + 1 , np.shape ( coord_xyz )[ 0 ] ) :
            euler_angles = np.round ( angle_between_vectors ( coord_xyz[ idx ] , coord_xyz[ j ] ) , 2 )
            df_xyz_to_dip.loc[ idx * np.shape ( coord_xyz )[ 0 ] + j ] = [ idx + 1 , j + 1 ,
                                                                           np.round ( dip[ idx ][ j ] , 2 ) ,
                                                                           *euler_angles ]

    return df_xyz_to_dip

### Functions for the different Interactions

#%%% Chemical Shift
def chemical_shift_tensor(num_nuc_cs):
    """
    lets you fill in the chemical shift parameters of different nuclei
    :param num_nuc_cs: number of nuclei input by the user
    :return: chemical shift dataframe
    """
    st.subheader ( 'Chemical Shift' , divider=True )
    chemical_shift_df = pd.DataFrame ( columns=[ 'i' , 'csiso' , 'csaniso' , 'eta' , 'alpha' , 'beta' , 'gamma' ] )
    config_cs = {
        'i' : st.column_config.NumberColumn ( 'Nucleus i' , min_value=1 , max_value=num_nuc_cs , required=True ) ,
        'csiso' : st.column_config.NumberColumn ( 'Isotropic CS (ppm)' , required=True ) ,
        'csaniso' : st.column_config.NumberColumn ( 'Anisotropic CS (ppm)' , default=0.0 ) ,
        'eta' : st.column_config.NumberColumn ( 'Asymmetry' , min_value=0. , max_value=1. , default=0.0 ) ,
        'alpha' : st.column_config.NumberColumn ( 'alpha' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
        'beta' : st.column_config.NumberColumn ( 'beta' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
        'gamma' : st.column_config.NumberColumn ( 'gamma' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
    }
    result_df_cs_fn = st.data_editor ( chemical_shift_df , column_config=config_cs , num_rows='dynamic' )
    result_df_cs_fn[ 'csiso' ] = result_df_cs_fn[ 'csiso' ].astype( str ) + 'p'
    result_df_cs_fn[ 'csaniso' ] = result_df_cs_fn[ 'csaniso' ].astype( str ) + 'p'
    result_df_cs_fn.insert ( 0 , 'Interaction' , "shift" )
    return result_df_cs_fn

#%%% J-coupling

def j_coupling_tensor(num_nuc_j):
    st.subheader ( "J-coupling" , divider=True )
    j_coupling_df = pd.DataFrame ( columns=[ 'i' , 'j' , 'jiso' , 'janiso' , 'eta' , 'alpha' , 'beta' , 'gamma' ] )
    config = {
        'i' : st.column_config.NumberColumn ( 'Nucleus i' , min_value=1 , max_value=num_nuc_j + 1 , required=True ) ,
        'j' : st.column_config.NumberColumn ( 'Nucleus j > i' , min_value=1 , max_value=num_nuc_j + 1 , required=True ) ,
        'jiso' : st.column_config.NumberColumn ( 'Isotropic J (Hz)' , required=True ) ,
        'janiso' : st.column_config.NumberColumn ( 'Anisotropic J (Hz)' , default=0.0 ) ,
        'eta' : st.column_config.NumberColumn ( 'Asymmetry' , min_value=0. , max_value=1. , default=0.0 ) ,
        'alpha' : st.column_config.NumberColumn ( 'alpha' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
        'beta' : st.column_config.NumberColumn ( 'beta' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
        'gamma' : st.column_config.NumberColumn ( 'gamma' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
    }
    st.markdown ( "**J coupling**" )
    result_df_j_fn = st.data_editor ( j_coupling_df , column_config=config , num_rows='dynamic' )
    result_df_j_fn.insert ( 0 , 'Interaction' , "jcoupling" )
    return result_df_j_fn

#%%% Dipolar coupling

def dipolar_coupling_tensor(num_nuc_d, nuc, table_of_nuclei):
    """
    Calculates the dipolar coupling for a given distance or a .xyz file
    :param num_nuc_d: number of nuclei
    :param nuc: name of nuclei to look for from the table
    :param table_of_nuclei: database of nuclei
    :return: dataframe containing the dipolar coupling, euler angles and the nuclei numbers.
    """
    result_df_d_fn = None
    st.subheader ( "Dipolar Coupling" , divider=True )
    # if 'select_dipolar_method' not in st.session_state :
    st.session_state.select_dipolar_method = "None"
    select_dipolar_method = st.segmented_control ( "Method" , options=[ "Direct" , "Distance" , "File" ] , selection_mode="single")
    if select_dipolar_method == 'Direct' :
        d_coupling_df = pd.DataFrame ( columns=[ 'i' , 'j' , 'dip' , 'alpha' , 'beta' , 'gamma' ] )
        config_d = {
            'i' : st.column_config.NumberColumn ( 'Nucleus i' , min_value=1 , max_value=num_nuc_d + 1 , required=True ) ,
            'j' : st.column_config.NumberColumn ( 'Nucleus j > i' , min_value=1 , max_value=num_nuc_d + 1 ,
                                                  required=True ) ,
            'dip' : st.column_config.NumberColumn ( 'Coupling strength (Hz)' , required=True ) ,
            'alpha' : st.column_config.NumberColumn ( 'alpha' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
            'beta' : st.column_config.NumberColumn ( 'beta' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
            'gamma' : st.column_config.NumberColumn ( 'gamma' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
        }
        st.markdown ( "**Dipolar coupling**" )
        result_df_d_fn = st.data_editor ( d_coupling_df , column_config=config_d , num_rows='dynamic' )
        result_df_d_fn.insert ( 0 , 'Interaction' , "dipole" )
    elif select_dipolar_method == "Distance" :
        d_coupling_df = pd.DataFrame ( columns=[ 'i' , 'j' , 'dist' , 'alpha' , 'beta' , 'gamma' ] )
        config_d = {
            'i' : st.column_config.NumberColumn ( 'Nucleus i' , min_value=1 , max_value=num_nuc_d + 1 , required=True ) ,
            'j' : st.column_config.NumberColumn ( 'Nucleus j > i' , min_value=1 , max_value=num_nuc_d + 1 ,
                                                  required=True ) ,
            'dist' : st.column_config.NumberColumn ( 'Distance (A)' , required=True , format='%.2f' ) ,
            'alpha' : st.column_config.NumberColumn ( 'alpha' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
            'beta' : st.column_config.NumberColumn ( 'beta' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
            'gamma' : st.column_config.NumberColumn ( 'gamma' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
        }
        st.markdown ( "**Dipolar coupling**" )
        result_df_d_fn = st.data_editor ( d_coupling_df , column_config=config_d , num_rows='dynamic' )
        for index , row in result_df_d_fn.iterrows () :
            # result_df_d(3, 'Dipolar Coupling (Hz)', dist2dipole(nuc[row['i']-1], nuc[row['j']-1], row['dist']))
            result_df_d_fn.at[ index , 'dist' ] = dist2dipole ( nuc[ row[ 'i' ] - 1 ] ,
                                                                nuc[ row[ 'j' ] - 1 ] , row[ 'dist' ] , table_of_nuclei)
        result_df_d_fn.insert ( 0 , 'Interaction' , "dipole" )
    elif select_dipolar_method == "File" :
        st.session_state.select_dipolar_method = "File"
        mdown_text = ''' The file must be an *.xyz file of the following format:   
             Number of atoms  
             Name &mdash; *can be anything*  
             :red[Nucleus-Name]     :orange[x-coordinate]   :green[y-coordinate]    :blue[z-coordinate]  
             e.g. Glycine can be written as:     
             10  
             2-Aminoacetic acid    
             H      0.1622     -1.0628      1.5533  
             C      0.3567     -0.0905      1.0501  
             H     -0.0181      0.6975      1.7355  
             N      1.7875      0.1811      0.7976  
             H      2.2858      0.1158      1.6592  
             H      2.1579     -0.4801      0.1480  
             C     -0.4086     -0.0874     -0.2553  
             O     -0.1765     -0.7075     -1.2773  
             O     -1.5162      0.6883     -0.2681  
             H     -1.9411      0.6382     -1.1188   '''
        st.markdown ( mdown_text )
        st.divider ()
        xyz_file = st.file_uploader ( 'xyz file' , type=[ 'xyz' ] )
        if xyz_file is not None :
            result_df_d_fn = xyz_file_to_dipolar_data ( xyz_file , nuc, num_nuc_d, table_of_nuclei )
            result_df_d_fn.insert ( 0 , 'Interaction' , "dipole" )

    return result_df_d_fn

#%%% Quadrupolar coupling

def quadrupolar_coupling_tensor(num_nuc_q):
    """
    :param num_nuc_q: number of the quadrupolar nuclei
    :return: returns the database containing the quadrupolar paramaters of the given nuclei as entered by user.
    """
    st.subheader ( "Q-interaction" , divider=True )
    quadrupole_df = pd.DataFrame ( columns=[ 'i' , 'order' , 'cq' , 'eta' , 'alpha' , 'beta' , 'gamma' ] )
    config_q = {
        'i' : st.column_config.NumberColumn ( 'Nucleus i' , min_value=1 , max_value=num_nuc_q , required=True ) ,
        'order' : st.column_config.NumberColumn ( 'order' , min_value=1 , max_value=2 , required=True , format='%d' ) ,
        'cq' : st.column_config.NumberColumn ( 'Cq (Hz)' , default=0.0 ) ,
        'eta' : st.column_config.NumberColumn ( 'Asymmetry' , min_value=0. , max_value=1. , default=0.0 ) ,
        'alpha' : st.column_config.NumberColumn ( 'alpha' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
        'beta' : st.column_config.NumberColumn ( 'beta' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
        'gamma' : st.column_config.NumberColumn ( 'gamma' , min_value=-360.0 , max_value=360.0 , default=0.0 ) ,
    }
    result_df_q_fn = st.data_editor ( quadrupole_df , column_config=config_q , num_rows='dynamic' )
    result_df_q_fn.insert ( 0 , 'Interaction' , "quadrupole" )
    return result_df_q_fn



def main():
    """
    :return: spinsys section of the SIMPSON file.
    """
    #%% Load nuclei data from file
    script_dir = os.path.dirname ( __file__ )
    csv_file = os.path.join ( script_dir, '../resources/NMR_freq_table.csv' )


    table_of_nuclei = pd.read_csv ( csv_file )


    #%% Spin System Inputs

    st.header ( '*Choice of Nucleus*' , divider=True )
    num_nuc = st.number_input ( "How many nuclei?" , min_value=1 , max_value=10 , value=1 , step=1 , format='%d' )
    nuc = [ ]
    for i in range ( num_nuc ) :
        nuc.append ( st.selectbox ( f"Nucleus {i + 1} : " , table_of_nuclei.Name.values.tolist () , index=2 ) )

    channels = list ( {k : None for k in nuc}.keys () )

    #%% Interactions

    st.header ( "*Interactions*" , divider=True )
    result_df_cs = None
    result_df_j = None
    result_df_d = None
    result_df_q = None


    if st.checkbox("Chemical Shift"):
        result_df_cs = chemical_shift_tensor(num_nuc)

    if num_nuc > 1:
        if st.checkbox("J - Coupling"):
            result_df_j = j_coupling_tensor(num_nuc)

        if st.checkbox("Dipolar Coupling") :
            st.session_state.select_dipolar_method = "None"
            result_df_d = dipolar_coupling_tensor(num_nuc, nuc, table_of_nuclei)


    mask = table_of_nuclei[ "Name" ].isin ( nuc )
    spin_num = table_of_nuclei[ mask ][ "Spin" ]
    if spin_num.gt ( 0.5 ).any () and st.checkbox("Quadrupolar Interaction"):
        result_df_q = quadrupolar_coupling_tensor(num_nuc)


    #%%%% Final Output


    options = ['CS', 'J', 'dip', 'quad']

    if result_df_cs is not None:
        str_cs = result_df_cs.to_string(index=False, header=False)
    else:
        str_cs = " "

    if result_df_d is not None:
        str_d = result_df_d.to_string(index=False, header=False)
    else:
        str_d = " "

    if result_df_j is not None:
        str_j = result_df_j.to_string(index=False, header=False)
    else:
        str_j = " "

    if result_df_q is not None:
        str_q = result_df_q.to_string(index=False, header=False)
    else:
        str_q = " "

    st.subheader ("Click on the interactions that you want")

    dict_interaction = {'CS': str_cs ,
                        'J': str_j,
                        'dip': str_d,
                        'quad': str_q}
    list_of_interactions = st.segmented_control("Interactions", options, selection_mode="multi")

    code_text = ""

    for interactions in list_of_interactions:
        code_text = code_text + dict_interaction[interactions] + "\n"

    st.divider()
    st.subheader ( 'Please press generate to get the code for SIMPSON file:' )

    if st.button("Generate"):
        spinsys_code = ("spinsys { \n"
                        + '\t nuclei    ' + ' '.join ( nuc ) + '\n'
                        + '\t channels  ' + '   ' + ' '.join ( channels ) + '\n'
                        + "\t " + code_text + '\n'
                        + "}")
        st.code(spinsys_code, language='tcl')

if __name__ == '__main__':
    st.title("To generate spinsys section of SIMPSON")
    st.divider()
    main()