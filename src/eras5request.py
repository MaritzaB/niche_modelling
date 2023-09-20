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
        'year': '2014',
        'month': [
            '01', '02', '03',
            '04', '05', '06',
        ],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
    },
    'download.zip')
