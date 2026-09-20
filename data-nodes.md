# __Data Sources__

All the tables and data processing tech notes

# Currently used data tables

__CBD Practice Model:__
`tables-formatted/transport-mode-MB` gives the count of each preferred mode of transport for each mesh block in the adelaide city zone. The mesh blocks are by usual residence.

`tables-formatted/POW-occupation-DZN` gives the count of each occupation type for each destination zone. The destination zone of each data point is that person's place of work.

# Future sources

__Census / Gov Data__

- Population (mesh block populations)
- Density? (mesh block population / mesh block area)
- Explore table builder for stuff
- Explore data.sa.gov.au

__Strava__

Just try stuff hopefully something will work
Last resort: could manually create a *smaller calibration table* using segment data.


__Super Tuesday!__

- KML to csv and parse the total attribute for each coordinate
- Using https://mygeodata.cloud to convert to csv
- Do for as many years as possible for regression training data

__Google__

- Look into later