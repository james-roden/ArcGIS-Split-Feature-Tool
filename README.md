# ArcGIS-Split-Feature-Tool
*Written by James M Roden*

Split feature class into separate feature classes based on specified field attribute

[DOWNLOAD](https://github.com/GISJMR/ArcGIS-Split-Feature-Tool/raw/master/SplitFeatureTool.zip)

![exmaple](https://github.com/GISJMR/ArcGIS-Split-Feature-Tool/raw/master/example.png)
*Example of input and output*

## Algorithm
* Create feature layer from input feature class
* Loop through each record and for each unique attribute create a 'new selection'
* Export selected features to new feature class
