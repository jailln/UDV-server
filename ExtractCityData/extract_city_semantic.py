import sys
import argparse
import yaml
import math
import py3dtiles
import numpy as np
from psycopg2 import connect, sql
from psycopg2.extras import NamedTupleCursor
from py3dtiles import TriangleSoup, GlTF, B3dm, BatchTable
import json
import itertools

if __name__ == '__main__':

    # arg parse
    descr = '''TODO.'''
    parser = argparse.ArgumentParser(description=descr)

    cfg_help = 'Path to the database configuration file'
    parser.add_argument('db_config_path', type=str, help=cfg_help)

    args = parser.parse_args()

    db_config = None

    with open(args.db_config_path, 'r') as db_config_file:
        try:
            db_config = yaml.load(db_config_file)
            db_config_file.close()
        except:
            print('ERROR: ', sys.exec_info()[0])
            db_config_file.close()
            sys.exit()

    # Check that db configuration is well defined
    if (("PG_HOST" not in db_config) or ("PG_NAME" not in db_config)
        or ("PG_PORT" not in db_config) or ("PG_USER" not in db_config)
        or ("PG_PASSWORD" not in db_config) or ("MATERIALIZED_VIEW_NAME" not in db_config)):
        print(("ERROR: Database is not properly defined in '{0}', please refer to README.md"
              .format(args.db_config_path)))
        sys.exit()

    # Connect to database
    db = connect(
        "postgresql://{0}:{1}@{2}:{3}/{4}"
        .format(db_config['PG_USER'], db_config['PG_PASSWORD'], db_config['PG_HOST'],
        db_config['PG_PORT'], db_config['PG_NAME']),
        cursor_factory=NamedTupleCursor, # fetch method will return named tuples instead of regular tuples
    )

    db.autocommit = True
    # Open a cursor to perform database operations
    cursor = db.cursor()

    # test
    #test = utils.CitiesConfig.allRepresentations(args.city, "buildings")
    t_destination = "lod2"
    t_temp = "temp_table"
    epsg = 3946
    imageRootDir = "/media/data/Backup villes/DataLyon_Archives/LYON_1ER_2012"
    imageOutputDir = "appearance"

    hierarchy = {}
    reverseHierarchy = {}
    objects = []
    classes = set()

    def addToHierarchy(object_id, parent_id):
        if parent_id is not None:
            if parent_id not in hierarchy:
                hierarchy[parent_id] = []
            hierarchy[parent_id].append(object_id)
            reverseHierarchy[object_id] = parent_id

    # Get building objects' id, class and hierarchy
    buildingIds = (1,31,216,316,545,654,679,853,948)
    cursor.execute("SELECT building.id, building_parent_id, cityobject.gmlid, cityobject.objectclass_id FROM building JOIN cityobject ON building.id=cityobject.id WHERE building_root_id IN %s", (buildingIds,))
    for t in cursor.fetchall():
        objects.append({'internalId': t[0], 'gmlid': t[2], 'class': t[3]})
        addToHierarchy(t[0], t[1])
        classes.add(t[3])

    # Building + descendants ids
    subBuildingIds = tuple([i['internalId'] for i in objects])

    # Get surface geometries' id and class
    # TODO: offset
    cursor.execute("SELECT cityobject.id, cityobject.gmlid, thematic_surface.building_id, thematic_surface.objectclass_id, ST_AsBinary(ST_Multi(ST_Collect(ST_Translate(surface_geometry.geometry, -1845500, -5176100, 0)))) FROM surface_geometry JOIN thematic_surface ON surface_geometry.root_id=thematic_surface.lod2_multi_surface_id JOIN cityobject ON thematic_surface.id=cityobject.id WHERE thematic_surface.building_id IN %s GROUP BY surface_geometry.root_id, cityobject.id, cityobject.gmlid, thematic_surface.building_id, thematic_surface.objectclass_id", (subBuildingIds,))
    for t in cursor.fetchall():
        objects.append({'internalId': t[0], 'gmlid': t[1], 'class': t[3], 'geometry': t[4]})
        addToHierarchy(t[0], t[2])
        classes.add(t[3])

    # Get class names
    classDict = {}
    cursor.execute("SELECT id, classname FROM objectclass")
    for t in cursor.fetchall():
        # TODO: allow custom fields to be added (here + in queries)
        classDict[t[0]] = (t[1], ['gmlid'])

    # Create classes
    bt = BatchTable()
    for c in classes:
        bt.add_class(classDict[c][0], classDict[c][1])

    geometricInstances = [(o['internalId'], o) for o in objects if 'geometry' in o]
    nonGeometricInstances = [(o['internalId'], o) for o in objects if 'geometry' not in o]

    objectPosition = {}
    for i, (object_id, _) in enumerate(itertools.chain(geometricInstances, nonGeometricInstances)):
        objectPosition[object_id] = i

    def getParent(object_id):
        if object_id in reverseHierarchy:
            return [objectPosition[reverseHierarchy[object_id]]]
        return []

    # First insert objects with geometries
    arrays = []
    for object_id, obj in geometricInstances:
        bt.add_class_instance(classDict[obj['class']][0], obj, getParent(object_id))


        geom = TriangleSoup.from_wkb_multipolygon(obj['geometry'])
        arrays.append({
            'position': geom.getPositionArray(),
            'normal': geom.getNormalArray(),
            'bbox': [[float(i) for i in j] for j in geom.getBbox()]
        })

    # Then insert objects with no geometry
    for object_id, obj in nonGeometricInstances:
        bt.add_class_instance(classDict[obj['class']][0], obj, getParent(object_id))

    gltf = GlTF.from_binary_arrays(arrays, np.identity(4).flatten('F'))
    b3dm = B3dm.from_glTF(gltf, bt)
    f = open("test.b3dm", 'wb')
    f.write(b3dm.to_array())
