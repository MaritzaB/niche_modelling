select id, ST_AsText(
ST_WrapX(geom, 0, 360)
) as geom
from "guadalupe_island";