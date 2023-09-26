#!/usr/bin/env python

import cdsapi

c = cdsapi.Client()

c.retrieve(
    'satellite-sea-surface-temperature',
    {
        'version': '2_1',
        'variable': 'all',
        'format': 'zip',
        'processinglevel': 'level_4',
        'sensor_on_satellite': 'combined_product',
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
