select id,
 ST_AsText(
ST_ShiftLongitude(geom)
) as geom
from "fullConvexHullAlbatross"
