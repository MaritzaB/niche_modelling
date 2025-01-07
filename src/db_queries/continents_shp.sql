select id, ST_AsText(
ST_WrapX(geom, 0, 360)
) as geom, 
ST_AsEWKT(geom) as ewkt, continent
from "continents";