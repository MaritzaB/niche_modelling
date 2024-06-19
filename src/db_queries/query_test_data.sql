select
    'Phoebastria immutabilis' as scientific_name,
    longitude, latitude,
    cast(substring("date", 1,4) as integer) as year,
	cast(substring("date",6,2) as integer) as month,
	geom,
	case when
		cast(substring("date", 1,4) as integer) < 2018 then 'train'
		else 'test'
		end "data"
from albatros_seasons as2
where 
    cast(substring("date",6,2) as integer) = 2
	