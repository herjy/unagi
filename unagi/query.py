#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SQL search related functions"""

from .hsc import Hsc

__all__ = ['HELP_BASIC', 'COLUMNS_CONTAIN', 'TABLE_SCHEMA', 'PATCH_CONTAIN',
           'basic_forced_photometry', 'column_dict_to_str']

HELP_BASIC = "SELECT * FROM help('{0}');"

TABLE_SCHEMA = "SELECT * FROM help('{0}.{1}');"

COLUMNS_CONTAIN = "SELECT * FROM help('{0}.%{1}%');"

PATCH_CONTAIN = """
    --- Find coadded patch images
    SELECT
        mosaic.tract,
        mosaic.patch,
        mosaic.filter01
    FROM
        {0}.mosaic JOIN public.skymap USING (skymap_id)
    WHERE
        patch_contains(patch_area, wcs, {1}, {2})
    ;
    """

def basic_forced_photometry(rerun, psf=True, cmodel=True, aper=False,
                            shape=False, flux=False, aper_type='3_20'):
    """
    Return a dict of column names for basic photometric measurements.
    """
    # Basic information
    basic_dict = {
        'object_id': 'forced.object_id', 'ra': 'forced.ra', 'dec': 'forced.dec',
        'tract': 'forced.tract', 'patch': 'forced.patch',
        'a_g': 'forced.a_g', 'a_r': 'forced.a_r', 'a_i': 'forced.a_i',
        'a_z': 'forced.a_z', 'a_y': 'forced.a_y',
    }

    if 'pdr2' in rerun:
        # This is for the columns in PDR2 rerun
        # Flag
        meta_dict = {
            'merge_peak_sky': 'forced.merge_peak_sky',
            'g_inputcount': 'forced.g_inputcount_value',
            'r_inputcount': 'forced.r_inputcount_value',
            'i_inputcount': 'forced.i_inputcount_value',
            'z_inputcount': 'forced.z_inputcount_value',
            'y_inputcount': 'forced.y_inputcount_value',
            'g_flag_edge': 'forced.g_pixelflags_edge',
            'r_flag_edge': 'forced.r_pixelflags_edge',
            'i_flag_edge': 'forced.i_pixelflags_edge',
            'z_flag_edge': 'forced.z_pixelflags_edge',
            'y_flag_edge': 'forced.y_pixelflags_edge',
            'g_flag_saturated': 'forced.g_pixelflags_saturated',
            'r_flag_saturated': 'forced.r_pixelflags_saturated',
            'i_flag_saturated': 'forced.i_pixelflags_saturated',
            'z_flag_saturated': 'forced.z_pixelflags_saturated',
            'y_flag_saturated': 'forced.y_pixelflags_saturated',
            'g_flag_interpolated': 'forced.g_pixelflags_interpolated',
            'r_flag_interpolated': 'forced.r_pixelflags_interpolated',
            'i_flag_interpolated': 'forced.i_pixelflags_interpolated',
            'z_flag_interpolated': 'forced.z_pixelflags_interpolated',
            'y_flag_interpolated': 'forced.y_pixelflags_interpolated',
            'g_flag_saturated_cen': 'forced.g_pixelflags_saturatedcenter',
            'r_flag_saturated_cen': 'forced.r_pixelflags_saturatedcenter',
            'i_flag_saturated_cen': 'forced.i_pixelflags_saturatedcenter',
            'z_flag_saturated_cen': 'forced.z_pixelflags_saturatedcenter',
            'y_flag_saturated_cen': 'forced.y_pixelflags_saturatedcenter',
            'g_flag_interpolated_cen': 'forced.g_pixelflags_interpolatedcenter',
            'r_flag_interpolated_cen': 'forced.r_pixelflags_interpolatedcenter',
            'i_flag_interpolated_cen': 'forced.i_pixelflags_interpolatedcenter',
            'z_flag_interpolated_cen': 'forced.z_pixelflags_interpolatedcenter',
            'y_flag_interpolated_cen': 'forced.y_pixelflags_interpolatedcenter',
            'g_extendedness': 'g_extendedness_value',
            'r_extendedness': 'r_extendedness_value',
            'i_extendedness': 'i_extendedness_value',
            'z_extendedness': 'z_extendedness_value',
            'y_extendedness': 'y_extendedness_value'
        }

        # CModel photometry
        if cmodel:
            cmodel_flag = {
                'g_cmodel_flag': 'forced.g_cmodel_flag',
                'r_cmodel_flag': 'forced.r_cmodel_flag',
                'i_cmodel_flag': 'forced.i_cmodel_flag',
                'z_cmodel_flag': 'forced.z_cmodel_flag',
                'y_cmodel_flag': 'forced.y_cmodel_flag'
            }
            if flux:
                cmodel_dict = {
                    'g_cmodel_flux': 'forced.g_cmodel_flux',
                    'r_cmodel_flux': 'forced.r_cmodel_flux',
                    'i_cmodel_flux': 'forced.i_cmodel_flux',
                    'z_cmodel_flux': 'forced.z_cmodel_flux',
                    'y_cmodel_flux': 'forced.y_cmodel_flux',
                    'g_cmodel_flux_err': 'forced.g_cmodel_fluxsigma',
                    'r_cmodel_flux_err': 'forced.r_cmodel_fluxsigma',
                    'i_cmodel_flux_err': 'forced.i_cmodel_fluxsigma',
                    'z_cmodel_flux_err': 'forced.z_cmodel_fluxsigma',
                    'y_cmodel_flux_err': 'forced.y_cmodel_fluxsigma'
                }
            else:
                cmodel_dict = {
                    'g_cmodel_mag': 'forced.g_cmodel_mag',
                    'r_cmodel_mag': 'forced.r_cmodel_mag',
                    'i_cmodel_mag': 'forced.i_cmodel_mag',
                    'z_cmodel_mag': 'forced.z_cmodel_mag',
                    'y_cmodel_mag': 'forced.y_cmodel_mag',
                    'g_cmodel_flux_err': 'forced.g_cmodel_fluxsigma',
                    'r_cmodel_flux_err': 'forced.r_cmodel_fluxsigma',
                    'i_cmodel_flux_err': 'forced.i_cmodel_fluxsigma',
                    'z_cmodel_flux_err': 'forced.z_cmodel_fluxsigma',
                    'y_cmodel_flux_err': 'forced.y_cmodel_fluxsigma'
                }
            # Put the CModel flag
            cmodel_dict.update(cmodel_flag)
        else:
            cmodel_dict = {}

        # PSF photometry
        if psf:
            psf_flag = {
                'g_psf_flag': 'forced2.g_psfflux_flag',
                'r_psf_flag': 'forced2.r_psfflux_flag',
                'i_psf_flag': 'forced2.i_psfflux_flag',
                'z_psf_flag': 'forced2.z_psfflux_flag',
                'y_psf_flag': 'forced2.y_psfflux_flag'
            }
            if flux:
                psf_dict = {
                    'g_psf_flux': 'forced2.g_psfflux_flux',
                    'r_psf_flux': 'forced2.r_psfflux_flux',
                    'i_psf_flux': 'forced2.i_psfflux_flux',
                    'z_psf_flux': 'forced2.z_psfflux_flux',
                    'y_psf_flux': 'forced2.y_psfflux_flux',
                    'g_psf_flux_err': 'forced2.g_psfflux_fluxsigma',
                    'r_psf_flux_err': 'forced2.r_psfflux_fluxsigma',
                    'i_psf_flux_err': 'forced2.i_psfflux_fluxsigma',
                    'z_psf_flux_err': 'forced2.z_psfflux_fluxsigma',
                    'y_psf_flux_err': 'forced2.y_psfflux_fluxsigma'
                }
            else:
                psf_dict = {
                    'g_psf_mag': 'forced2.g_psfflux_mag',
                    'r_psf_mag': 'forced2.r_psfflux_mag',
                    'i_psf_mag': 'forced2.i_psfflux_mag',
                    'z_psf_mag': 'forced2.z_psfflux_mag',
                    'y_psf_mag': 'forced2.y_psfflux_mag',
                    'g_psf_mag_err': 'forced2.g_psfflux_magsigma',
                    'r_psf_mag_err': 'forced2.r_psfflux_magsigma',
                    'i_psf_mag_err': 'forced2.i_psfflux_magsigma',
                    'z_psf_mag_err': 'forced2.z_psfflux_magsigma',
                    'y_psf_mag_err': 'forced2.y_psfflux_magsigma'
                }
            # Put the PSF flag
            psf_dict.update(psf_flag)
        else:
            psf_dict = {}

        # Aperture photometry with matched PSF
        if aper:
            # Flag for aperture photometry
            aper_flag = {
                'g_aper_flag': 'forced4.g_convolvedflux_{}_flag'.format(aper_type),
                'r_aper_flag': 'forced4.r_convolvedflux_{}_flag'.format(aper_type),
                'i_aper_flag': 'forced4.i_convolvedflux_{}_flag'.format(aper_type),
                'z_aper_flag': 'forced4.z_convolvedflux_{}_flag'.format(aper_type),
                'y_aper_flag': 'forced4.y_convolvedflux_{}_flag'.format(aper_type),
            }
            if flux:
                aper_dict = {
                    'g_aper_flux': 'forced4.g_convolvedflux_{}_flux'.format(aper_type),
                    'r_aper_flux': 'forced4.r_convolvedflux_{}_flux'.format(aper_type),
                    'i_aper_flux': 'forced4.i_convolvedflux_{}_flux'.format(aper_type),
                    'z_aper_flux': 'forced4.z_convolvedflux_{}_flux'.format(aper_type),
                    'y_aper_flux': 'forced4.y_convolvedflux_{}_flux'.format(aper_type),
                    'g_aper_flux_err': 'forced4.g_convolvedflux_{}_fluxsigma'.format(aper_type),
                    'r_aper_flux_err': 'forced4.r_convolvedflux_{}_fluxsigma'.format(aper_type),
                    'i_aper_flux_err': 'forced4.i_convolvedflux_{}_fluxsigma'.format(aper_type),
                    'z_aper_flux_err': 'forced4.z_convolvedflux_{}_fluxsigma'.format(aper_type),
                    'y_aper_flux_err': 'forced4.y_convolvedflux_{}_fluxsigma'.format(aper_type),
                }
            else:
                aper_dict = {
                    'g_aper_mag': 'forced4.g_convolvedmag_{}_mag'.format(aper_type),
                    'r_aper_mag': 'forced4.r_convolvedmag_{}_mag'.format(aper_type),
                    'i_aper_mag': 'forced4.i_convolvedmag_{}_mag'.format(aper_type),
                    'z_aper_mag': 'forced4.z_convolvedmag_{}_mag'.format(aper_type),
                    'y_aper_mag': 'forced4.y_convolvedmag_{}_mag'.format(aper_type),
                    'g_aper_mag_err': 'forced4.g_convolvedmag_{}_magsigma'.format(aper_type),
                    'r_aper_mag_err': 'forced4.r_convolvedmag_{}_magsigma'.format(aper_type),
                    'i_aper_mag_err': 'forced4.i_convolvedmag_{}_magsigma'.format(aper_type),
                    'z_aper_mag_err': 'forced4.z_convolvedmag_{}_magsigma'.format(aper_type),
                    'y_aper_mag_err': 'forced4.y_convolvedmag_{}_magsigma'.format(aper_type),
                }
            aper_dict.update(aper_flag)
        else:
            aper_dict = {}

        # Shape of the object
        if shape:
            shape_dict = {
                'g_sdssshape_11': 'forced2.g_sdssshape_shape11',
                'g_sdssshape_22': 'forced2.g_sdssshape_shape22',
                'g_sdssshape_12': 'forced2.g_sdssshape_shape12',
                'r_sdssshape_11': 'forced2.r_sdssshape_shape11',
                'r_sdssshape_22': 'forced2.r_sdssshape_shape22',
                'r_sdssshape_12': 'forced2.r_sdssshape_shape12',
                'i_sdssshape_11': 'forced2.i_sdssshape_shape11',
                'i_sdssshape_22': 'forced2.i_sdssshape_shape22',
                'i_sdssshape_12': 'forced2.i_sdssshape_shape12',
                'z_sdssshape_11': 'forced2.z_sdssshape_shape11',
                'z_sdssshape_22': 'forced2.z_sdssshape_shape22',
                'z_sdssshape_12': 'forced2.z_sdssshape_shape12',
                'y_sdssshape_11': 'forced2.y_sdssshape_shape11',
                'y_sdssshape_22': 'forced2.y_sdssshape_shape22',
                'y_sdssshape_12': 'forced2.y_sdssshape_shape12'
            }
        else:
            shape_dict = {}
    else:
        raise NameError("Wrong rerun name")

    # Combine all the dicts together
    basic_dict.update(cmodel_dict)
    basic_dict.update(psf_dict)
    basic_dict.update(aper_dict)
    basic_dict.update(shape_dict)
    basic_dict.update(meta_dict)

    return basic_dict

def column_dict_to_str(columns, select=True):
    """
    Convert the dictionary of columns into a SQL search SQL.
    """
    col_str = ', '.join(["{0} AS {1}".format(v, k) for k, v in columns.items()])
    if select:
        return 'SELECT ' + col_str
    return col_str

def box_search_template(primary=True, clean=True, dr='pdr2', rerun='pdr2_wide', 
                        archive=None):
    """
    Get the SQL template for box search.
    """
    # Login to HSC archive
    if archive is None:
        archive = Hsc(dr=dr, rerun=rerun)
    else:
        dr = archive.dr
        rerun = archive.rerun

    # The selection part of the SQL search
    select_str = column_dict_to_str(basic_forced_photometry(rerun))

    pass

def cone_search_template(primary=True, clean=True, dr='pdr2', rerun='pdr2_wide', archive=None):
    """
    Get the SQL template for box search.
    """
    # Login to HSC archive
    if archive is None:
        archive = Hsc(dr=dr, rerun=rerun)
    else:
        dr = archive.dr
        rerun = archive.rerun
    pass