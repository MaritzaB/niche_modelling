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
        'year': '2014',
        'month': '02',
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
