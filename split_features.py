#!/usr/bin/env python

"""

This script takes a file containing one or more feature definitions, that is
pointed to by the -f flag. It then writes each feature defition out to it's own
independent file in an autogenerated directory tree.  If a base directory
is supplied with the -o flag, the features will be written out to this
directory.  Otherwise, the component property of each feature will be used
to determine the base directory.

Authors: Douglas Jacobsen, Xylar Asay-Davis
Last Modified: 10/16/2016

"""

import os
import json
import argparse
from utils.feature_write_utils import write_all_features

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-f", "--features_file", dest="features_file",
                    help="File containing features to split up",
                    metavar="FILE", required=True)

parser.add_argument("-o", "--output_dir", dest="output_dir_name",
                    help="Output directory, default is determined by the "
                         "component property",
                    metavar="PATH")

args = parser.parse_args()

if args.features_file:
    if not os.path.exists(args.features_file):
        parser.error('The file {} does not exist.'.format(args.features_file))

with open(args.features_file) as f:
    features_file = json.load(f)


for feature in features_file['features']:
    feature_name = feature['properties']['name']
    component = feature['properties']['component']
    object_type = feature['properties']['object']

    base_dir = component
    if args.output_dir_name is not None:
        base_dir = args.output_dir_name

    dir_name = feature_name.strip().replace(' ', '_').strip('\'').strip('.')

    if not os.path.exists('{}/{}/{}'.format(base_dir, object_type, dir_name)):
        os.makedirs('{}/{}/{}'.format(base_dir, object_type, dir_name))

    out_file_name = '{}/{}/{}/{}.geojson'.format(base_dir, object_type,
                                                 dir_name, object_type)

    write_all_features({'features': [feature]}, out_file_name, indent=4,
                       defaultGroupName=None, strip_history=True)

# vim: foldmethod=marker ai ts=4 sts=4 et sw=4 ft=python
