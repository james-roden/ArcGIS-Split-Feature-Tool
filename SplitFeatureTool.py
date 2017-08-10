# -----------------------------------------------
# Name: Split Feature Tool
# Purpose: Splits input feature into multiple features based on specified attribute
# Author: James M Roden
# Created: Aug 2016
# ArcGIS Version: 10.3
# Python Version 2.6
# PEP8
# -----------------------------------------------

try:
    import arcpy
    import os
    import re
    import sys
    import traceback

    # Function constructs a SQL where clause
    def build_where_clause(table, field, value):
        """
        Constructs a syntactically correct SQL statement with the correct field delimiters
        Idea provided by blah238 on Stack Exchange

        table   -- Input feature class
        field   -- Input field
        value   -- The field value
        """

        # Data source specific delimiters
        field_delimiters = arcpy.AddFieldDelimiters(table, field)  # Returns a delimited field name
        field_type = arcpy.ListFields(table, field)[0].type
        # If field type is string, add quotes
        if str(field_type) == "String":
            value = "'{}'".format(value)
        where_clause = "{} = {}".format(field_delimiters, value)
        return where_clause

    # arcpy environment settings
    arcpy.env.workspace = r"in_memory"
    arcpy.env.scratchWorkspace = r"in_memory"
    arcpy.env.overwriteOutput = True

    # ArcGIS tool parameters
    features = arcpy.GetParameterAsText(0)
    field_name = arcpy.GetParameterAsText(1)
    workspace = arcpy.GetParameterAsText(2)

    # Create layer and loop through unique field values and split into new feature classes
    features_layer = arcpy.MakeFeatureLayer_management(features, None)
    with arcpy.da.SearchCursor(features, field_name) as cursor:
        field_set = set()
        for row in cursor:
            field_value = str(row[0])
            if field_value in field_set:
                continue
            else:
                field_set.add(field_value)
            sql_exp = build_where_clause(features, field_name, field_value)
            arcpy.SelectLayerByAttribute_management(features_layer, "NEW_SELECTION", sql_exp)

            # Construct eligible filename
            field_value = re.sub("[^\w]+", "", field_value)
            output_file = os.path.join(workspace, field_value[:15])

            # Save output
            arcpy.CopyFeatures_management(features_layer, output_file)
            arcpy.AddMessage("Created file: " + output_file)

except:
    tb = sys.exc_info()[2]  # Traceback object
    tbinfo = traceback.format_tb(tb)[0]  # Traceback string
    # Concatenate error information and return to GP window
    pymsg = ('PYTHON ERRORS:\nTraceback info:\n' + tbinfo + '\nError Info: \n'
             + str(sys.exc_info()[1]))
    msgs = 'ArcPy ERRORS:\n' + arcpy.GetMessage(2) + '\n'
    arcpy.AddError(msgs)
    print pymsg

finally:
    # Delete in_memory
    arcpy.Delete_management('in_memory')

# End of script
