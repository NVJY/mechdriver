"""
  Get frequencies
"""

import os
import autofile
import projrot_io
from lib.submission import run_script
from lib.submission import DEFAULT_SCRIPT_DCT


def projrot_freqs(geo, hess, thy_info, thy_run_fs,
                  grad=(), rotors_str='', coord_proj='cartesian',
                  script_str=DEFAULT_SCRIPT_DCT['projrot']):
    """ Get the projected frequencies from projrot code
    """

    # Build the filesystem objects needed for running ProjRot
    thy_run_fs[-1].create(thy_info[1:4])
    thy_run_path = thy_run_fs[-1].path(thy_info[1:4])

    bld_locs = ['PROJROT', 0]
    bld_run_fs = autofile.fs.build(thy_run_path)
    bld_run_fs[-1].create(bld_locs)
    projrot_path = bld_run_fs[-1].path(bld_locs)
    print('Build Path for ProjRot calls')
    print(projrot_path)

    # Write the ProjRot input file
    projrot_inp_str = projrot_io.writer.rpht_input(
        geo, grad, hess, rotors_str=rotors_str,
        coord_proj=coord_proj)
    proj_file_path = os.path.join(projrot_path, 'RPHt_input_data.dat')
    with open(proj_file_path, 'w') as proj_file:
        proj_file.write(projrot_inp_str)

    # Run ProjRot
    run_script(script_str, projrot_path)

    # Read vibrational frequencies from ProjRot output
    if os.path.exists(projrot_path+'/hrproj_freq.dat'):
        with open(projrot_path+'/hrproj_freq.dat', 'r') as projfile:
            hrproj_str = projfile.read()
        hrproj_freqs, hr_imag_freq = projrot_io.reader.rpht_output(
            hrproj_str)
    else:
        hrproj_freqs, hr_imag_freq = [], None

    if os.path.exists(projrot_path+'/RTproj_freq.dat'):
        with open(projrot_path+'/RTproj_freq.dat', 'r') as projfile:
            rtproj_str = projfile.read()
        rtproj_freqs, rt_imag_freq = projrot_io.reader.rpht_output(
            rtproj_str)
    else:
        rtproj_freqs, rt_imag_freq = [], None

    return rtproj_freqs, hrproj_freqs, rt_imag_freq, hr_imag_freq
