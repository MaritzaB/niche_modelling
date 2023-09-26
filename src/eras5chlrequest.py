#!/usr/bin/env python

import cdsapi

c = cdsapi.Client()

c.retrieve(
    'satellite-ocean-colour',
    {
        'version': '6_0',
        'format': 'zip',
        'variable': 'mass_concentration_of_chlorophyll_a',
        'projection': 'regular_latitude_longitude_grid',
        'year': [
            '2014', '2015', '2016',
            '2017', '2018',
        ],
        'month': [
            '01', '02', '03',
            '04',
        ],
        'day': '01',
    },
    'download.zip')
