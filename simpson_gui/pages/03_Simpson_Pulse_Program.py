import streamlit as st

def generate_recoupling(type):

    def recoupling_s3():
        recoupling_code = f"""
        set rf [expr 0.5*$par(spin_rate)]
        set t90 [expr 0.25e6/$rf]
        set t270 [expr 0.75e6/$rf]
        set t360 [expr 1e6/$rf]
        set par(sw) [expr $par(spin_rate)/16]
        set ph 90
        for {{set i 1}} {{$i <= 2}} {{incr i}} {{
            pulse $t360 $rf [expr $ph+fmod($i,2)*180]
            pulse $t270 $rf [expr $ph+fmod($i,2)*180+180]
            pulse $t90  $rf [expr $ph+fmod($i,2)*180]
        }}
        for {{set i 1}} {{$i <= 2}} {{incr i}} {{
            pulse $t360 $rf [expr $ph+fmod($i,2)*180+180]
            pulse $t270 $rf [expr $ph+fmod($i,2)*180]
            pulse $t90  $rf [expr $ph+fmod($i,2)*180+180]
        }}
        """
        return recoupling_code

    def recoupling_brs3():
        recoupling_code = f"""
        set rf [expr 0.5*$par(spin_rate)]
        set t90 [expr 0.25e6/$rf]
        set t270 [expr 0.75e6/$rf]
        set t360 [expr 1e6/$rf]
        set par(sw) [expr $par(spin_rate)/16]
        set ph 90
        pulseid 1 250000 x
        for {{set i 1}} {{$i <= 2}} {{incr i}} {{
            pulse $t360 $rf [expr $ph+fmod($i,2)*180]
            pulse $t270 $rf [expr $ph+fmod($i,2)*180+180]
            pulse $t90  $rf [expr $ph+fmod($i,2)*180]
        }}
        for {{set i 1}} {{$i <= 2}} {{incr i}} {{
            pulse $t360 $rf [expr $ph+fmod($i,2)*180+180]
            pulse $t270 $rf [expr $ph+fmod($i,2)*180]
            pulse $t90  $rf [expr $ph+fmod($i,2)*180+180]
        }}
        pulseid 1 250000 -x
        """
        return recoupling_code

    def recoupling_sr26():
        recoupling_code = f"""
        set rf [expr 6.5*$par(spin_rate)]
        set t90 [expr 0.25e6/$rf]
        set t270 [expr 0.75e6/$rf]
        set ph [expr 180*11/26]
        set ph1 [expr $ph+180]
        set ph2 [expr -$ph+180]

        for {{set k 1}} {{$k <= 2}} {{incr k}} {{
            for {{set j 1}} {{$j <= 2}} {{incr j}} {{
                for {{set i 1}} {{$i <= 13}} {{incr i}} {{
                    pulse $t90  $rf [expr pow(-1,$k-1)*pow(-1,$j-1)*$ph+fmod($k+1,2)*180]
                    pulse $t270 $rf [expr pow(-1,$k-1)*pow(-1,$j-1)*$ph+fmod($k,2)*180]
                    pulse $t90  $rf [expr -pow(-1,$k-1)*pow(-1,$j-1)*$ph+fmod($k+1,2)*180]
                    pulse $t270 $rf [expr -pow(-1,$k-1)*pow(-1,$j-1)*$ph+fmod($k,2)*180]
                }}
            }}
        }}
        """
        return recoupling_code

    def recoupling_postc7():
        recoupling_code = f"""
        set rf [expr 7*$par(spin_rate)]
        set t90 [expr 0.25e6/$rf]
        for {{set i 1}} {{$i <= 7}} {{incr i}} {{
            set phase [expr $i*360.0/7.0]
            pulse $t90 $rf $phase
            pulse [expr 4.0*$t90] $rf [expr $phase+180]
            pulse [expr 3.0*$t90] $rf $phase
        }}
        """
        return recoupling_code

    def recoupling_rseq():
        recoupling_code = f"""
        # e.g. for R20_2^9
        set N 20
        set nsub 2
        set nusub 9
        set rf [expr ($N/$nsub*$par(spin_rate)]
        set t90 [expr 0.25e6/$rf]
        set phase [expr 180*$nusup/$par(N)]
        set loops [expr $par(N)/2]
        for {{set i 1}} {{$i <= $loops}} {{incr i}} {{
            pulse $t90 $rf $phase
            pulse [expr 3.0*$t90] $rf [expr $phase+180]
            pulse $t90 $rf -$phase
            pulse [expr 3.0*$t90] $rf [expr -($phase+180)]
        }}
        """
        return recoupling_code

    def recoupling_baba():
        recoupling_code = f"""
        set rf [expr 10*$par(spin_rate)]
        set t90 [expr 0.25e6/$rf]
        set td [expr (0.5e6/$par(spin_rate))-(2*$t90)]
        pulse $t90 $rf x
        delay $td
        pulse $t90 $rf x
        pulse $t90 $rf y
        delay $td
        pulse $t90 $rf -y
        pulse $t90 $rf x
        # Additional steps are omitted for brevity
        """
        return recoupling_code

    # Map type to corresponding TCL string generator
    recoupling_generators = {
        "s3": recoupling_s3,
        "brs3": recoupling_brs3,
        "sr26": recoupling_sr26,
        "postc7": recoupling_postc7,
        "rseq": recoupling_rseq,
        "baba": recoupling_baba,
    }

    if type in recoupling_generators:
        return recoupling_generators[type]()
    else:
        raise ValueError(f"Unknown pulse type: {type}")


def generate_decoupling(type) :
    def decoupling_cw() :
        decoupling_code = f"""
        acq_block {{
            pulse $par(tdec) 0 x $par(rf) 0
            pulse $par(tdec) 0 x $par(rf) 0
        }}
        """
        return decoupling_code

    def decoupling_tppm() :
        decoupling_code = f"""
        acq_block {{
            pulse $par(tdec) 0 x $par(rf) $par(ph)
            pulse $par(tdec) 0 x $par(rf) -$par(ph)
        }}
        """
        return decoupling_code

    def decoupling_swftppm() :
        decoupling_code = f"""
        acq_block {{
            foreach mul [list 0.78 0.86 0.94 0.96 0.98 1 1.02 1.04 1.06 1.14 1.22] {{
                pulse [expr $mul*$par(tdec)] 0 0 $par(rf) $par(ph)
                pulse [expr $mul*$par(tdec)] 0 0 $par(rf) -$par(ph)
            }}
        }}
        """
        return decoupling_code

    def decoupling_xix() :
        decoupling_code = f"""
        acq_block {{
            pulse [expr $par(tr)*$par(xix)] 0 x $par(rf) x
            pulse [expr $par(tr)*$par(xix)] 0 x $par(rf) -x
        }}
        """
        return decoupling_code

    def decoupling_spinal64() :
        decoupling_code = f"""
        acq_block {{
            foreach sup [list 1 -1 -1 1 -1 1 1 -1] {{
                pulse $par(tdec) 0 x $par(rf) [expr $sup*$par(ph)]
                pulse $par(tdec) 0 x $par(rf) [expr -$sup*$par(ph)]
                pulse $par(tdec) 0 x $par(rf) [expr $sup*($par(ph)+5)]
                pulse $par(tdec) 0 x $par(rf) [expr $sup*(-$par(ph)-5)]
                pulse $par(tdec) 0 x $par(rf) [expr $sup*($par(ph)+10)]
                pulse $par(tdec) 0 x $par(rf) [expr $sup*(-$par(ph)-10)]
                pulse $par(tdec) 0 x $par(rf) [expr $sup*($par(ph)+5)]
                pulse $par(tdec) 0 x $par(rf) [expr $sup*(-$par(ph)-5)]
            }}
        }}
        """
        return decoupling_code

    def decoupling_rcw() :
        decoupling_code = f"""
        acq_block {{
            pulse [expr $par(tr)-0.5*$par(t180)] 0 0 $par(rf) 0
            pulse $par(t180) 0 0 $par(rf) 90
            pulse [expr $par(tr)-$par(t180)] 0 0 $par(rf) 0
            pulse $par(t180) 0 0 $par(rf) 0
            pulse [expr $par(tr)-$par(t180)] 0 0 $par(rf) 0
            pulse $par(t180) 0 0 $par(rf) 90
            pulse [expr $par(tr)-0.5*$par(t180)] 0 0 $par(rf) 0
        }}
        """
        return decoupling_code

    def decoupling_wpmlg() :
        decoupling_code = f"""
            
            proc generate_wpmlgm {{N rfk sup}} {{
                global par
                set rf [expr $rfk*1000]
                set lgoffset [expr $rf/sqrt(2.0)] ;# calculation of the LG offset
                set taulg [expr 1.0/sqrt(pow($rf,2)+pow($lgoffset,2))] ;# calculation of the total length of the LG pulse
                set wpmlgph [expr $taulg*$lgoffset*360/$N] ;# calculates the phase of the first pulse of wPMLG
                set phshift [expr $wpmlgph/2] ;# this is a half phase increment/decrement shift in the first pulse of PMLG
                set taupmlg [expr $taulg*1.0e6/$N] ;# calculates the length of each pulse of pmlg
                set window 4.6
                set phpmlg [expr 180.0 - $phshift]
                
                for {{set i 1}} {{$i <= $N}} {{incr i}} {{
                    pulse $taupmlg $rf [expr fmod($phpmlg + $sup, 360)]
                    # puts "pulse $taupmlg $rf [expr fmod($phpmlg + $sup, 360)]"
                    set phpmlg [expr {{$phpmlg - $wpmlgph}}] 
                }}
                set phpmlg [expr {{$phpmlg + $wpmlgph + 180}}]
                for {{set i 1}} {{$i <= $N}} {{incr i}} {{
                    pulse $taupmlg $rf [expr fmod($phpmlg + $sup, 360)]
                    # puts "pulse $taupmlg $rf [expr fmod($phpmlg + $sup, 360)]"
                    set phpmlg [expr {{$phpmlg + $wpmlgph}}] 
                }}
                delay $window
            }}
            
            proc pulseq {{}} {{
               global par
               
               for {{set i 1}} {{$i <= $par(np)/2}} {{incr i}} {{
                acq
                generate_wpmlgm 5 100 0
                acq
                generate_wpmlgm 5 100 180
               }}
            }}
        """

    # Map decoupling sequences to their corresponding functions
    decoupling_generators = {
        "cw" : decoupling_cw ,
        "tppm" : decoupling_tppm ,
        "swftppm" : decoupling_swftppm ,
        "xix" : decoupling_xix ,
        "spinal64" : decoupling_spinal64 ,
        "rcw" : decoupling_rcw ,
        "wpmlg" : decoupling_wpmlg,
    }


    # Return the corresponding code for the given type
    if type in decoupling_generators :
        return decoupling_generators[ type ] ()
    else :
        raise ValueError ( f"Unknown decoupling type: {type}" )

def generate_heteronuclear_recoupling(type) :

    def zftedor():
        recoupling_code = f"""
            set rfC  150000
            set rfP  150000
            set tr    [expr 1.0e6/$par(spin_rate)]
            set t90C  [expr 0.25e6/$rfC]
            set t180C [expr 2.0*$t90C]
            set t90P  [expr 0.25e6/$rfP]
            set t180P [expr 2.0*$t90P]
            
            
            reset
            delay [expr $tr/2.0-$t180P]
            pulse $t180P 0 x $rfP x    
            delay [expr $tr/2.0-$t180P]
            pulse $t180P 0 x $rfP y
            store 1
            
            reset
            delay [expr 1*$tr-$t180C/2]
            pulse $t180C $rfC x 0 x
            delay [expr 1*$tr-$t180C/2]
            store 2
            reset
            
            reset
            pulse $t180P 0 x $rfP x  
            delay [expr $tr/2.0-$t180P]
            pulse $t180P 0 x $rfP y  
            delay [expr $tr/2.0-$t180P]
            store 3
            
            
            for {{set s 0}}{{$s < $par(np)}} {{incr s}} {{
            reset
            
            prop 1 $s
            prop 2
            prop 3 $s
            
            
            pulseid 1 250000 x 250000 x
            pulseid 1 250000 x 250000 $par(ph)
            
            
            prop 1 $s
            prop 2
            prop 3 $s
            
            acq $par(
            }}"""
        return recoupling_code

    def redor():
        recoupling_code = f"""
            
            set rf 100000
            set t180 pr 0.5e6/$rf]
            set tr   [expr 1.0e6/$par(spin_rate)]
            set tr2  [expr $tr-$t180]   
            
            reset
            delay $tr2
            pulse $t180 0 x $rf x
            delay $tr2
            pulse $t180 0 x $rf y
            store 1
            
            reset
            acq
            delay $tr2
            pulse $t180 0 x $rf x
            delay $tr2
            pulse $t180 $rf x 0 x
            prop 1
            store 2
            acq
            
            for {{set i 2}} {{$i < $par(np)}} {{incr i}} {{
            reset
            prop 1
            prop 2
            prop 1
            store 2
            acq
            }}
            """
        return recoupling_code

    recoupling_generators = {
        "tedor" : zftedor ,
        "redor" : redor ,
        }

    # Return the corresponding code for the given type
    if type in recoupling_generators :
        return recoupling_generators[ type ] ()
    else :
        raise ValueError ( f"Unknown decoupling type: {type}" )

st.header('Recoupling')
st.divider()
st.subheader('Homonuclear Recoupling')
option_homonuclear_recoupling = ["s3", "brs3", "sr26", "postc7", "rseq", "baba"]
homonuclear_recoupling = st.selectbox("Homonuclear Recoupling Sequence:", option_homonuclear_recoupling, index=None)
if homonuclear_recoupling is not None:
    max_delta_time = st.number_input('Time over which Hamiltonian is time independent', format='%.1f', value = 1.0)
    dq_filter_choice = st.toggle("Double Quantum Filter")
    if dq_filter_choice:
        dq_filter = "matrix set 2 totalcoherence {2 -2} "
        filter_dq = "filter 2"
    else:
        dq_filter = " "
        filter_dq = " "
    pulse_sequence = f"""
                    proc pulseq {{}}  {{
        maxdt {max_delta_time}
        {dq_filter}
        
        {generate_recoupling(homonuclear_recoupling)}
        store 1 ; #stores the propagator for 1 block of S3
        reset ; # resets the density matrix to rho0
        store 3 ; # identity prop
        acq ; # take first data point i.e. zero

        # loop below reuses stored propagators for the rest of acq
        for {{set j 1}} {{$j < $par(np)}} {{incr j}} {{
        reset
        prop 3 ; # call the identity propagator for the first time and then calls 1 to j-1 S3's
        prop 1 ; # call jth S3
        store 3 ; # store it in 3 and reused later
        {filter_dq}
        prop 3 ; # reconversion
        acq ; # detect 1 point
        }}
        }}
        """
    st.code(pulse_sequence, language='tcl')

st.subheader('Heteronuclear Recoupling')
option_heteronuclear_recoupling = ["tedor", "redor"]
heteronuclear_recoupling = st.selectbox("Heteronuclear Recoupling Sequence:", option_heteronuclear_recoupling, index=None)
if heteronuclear_recoupling is not None:
    st.code(generate_heteronuclear_recoupling(heteronuclear_recoupling), language='tcl')


st.header('Decoupling')
st.divider()
st.subheader('Heteronuclear Decoupling')
option_heteronuclear_decoupling = ["cw", "tppm", "swftppm", "xix", "spinal64", "rcw"]
heteronuclear_decoupling = st.selectbox("Heteronuclear Decoupling Sequence:", option_heteronuclear_decoupling, index=None)
if heteronuclear_decoupling is not None:
    max_delta_time = st.number_input('Time over which Hamiltonian is time independent', format='%.1f', value=1.0)
    pulse_sequence = f"""
    proc pulseq{{}} {{
    maxdt {max_delta_time}
    {generate_decoupling(heteronuclear_decoupling)}
    }}
    """
    st.code(pulse_sequence, language='tcl')


st.subheader('Homonuclear Decoupling')
option_homonuclear_decoupling = ["LG", "FSLG", "wPMLGmmbar", "LG4"]

homonuclear_decoupling = st.selectbox("Homonuclear Decoupling Sequence:", option_homonuclear_decoupling, index=None)
if homonuclear_decoupling is not None:
    st.code(generate_decoupling(homonuclear_decoupling), language='tcl')
