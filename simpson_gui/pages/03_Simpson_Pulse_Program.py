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


def heteronuclear_decoupling(type):
    def tppm():


option_homonuclear_recoupling = ["s3", "brs3", "sr26", "postc7", "rseq", "baba"]
homonuclear_rec = st.selectbox("Homonuclear Recoupling Sequence:", option_homonuclear_recoupling, index=None)
st.code(generate_recoupling(homonuclear_rec), language='tcl')

