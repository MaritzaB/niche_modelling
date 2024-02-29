select *, 
	cast(substring("date", 1,4) as integer) as year,
	cast(substring("date",6,2) as integer) as month
from gps_albatros_isla_guadalupe gaig2 
