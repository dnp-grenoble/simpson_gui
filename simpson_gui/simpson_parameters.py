#%% Header files
import numpy as np
import streamlit as st

with st.container () :
    option_of_field = st.selectbox ( "Field in MHz (1H) or T" ,
                                     ("MHz" , "Tesla") ,
                                     )
    if option_of_field == "MHz" :
        field = st.number_input ( "Enter the field in MHz" )
    else :
        field = st.number_input ( "Enter the field in T" )

    spinning_frequency = st.number_input ( "Spinning Frequency in Hz" , min_value=1 , max_value=500000 , value=10000 )

    options_crystal_file = [ "LEBoct31" , "alpha0beta0" , "alpha0beta90" , "bcr10" ,
                             "bcr100" , "bcr20" , "bcr200" , "bcr30" , "bcr40" , "bcr400" ,
                             "bcr50" , "bcr80" , "rep10" , "rep100" , "rep144" , "rep168" ,
                             "rep20" , "rep2000" , "rep256" , "rep30" , "rep320" , "rep66" ,
                             "rep678" , "repoct41" , "zcw143" , "zcw20" , "zcw232" , "zcw33" ,
                             "zcw376" , "zcw4180" , "zcw54" , "zcw615" , "zcw88" , "zcw986" ,
                             "zcw28656" ]
    powder_file = st.selectbox ( "Which powder averaging scheme?" , options_crystal_file ,
                                 )

