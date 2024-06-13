select cast(substring("date", 1,4) as integer) as year,
	cast(substring("date",6,2) as integer) as month,
	ST_AsText(st_Collect(geom)) as geom,
	count(geom) as number_of_points
from albatros_seasons as2 
group by year, month
order by year, month
