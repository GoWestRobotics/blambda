"""
create a new lambda function
"""
import json

import os

runtimes = {
    'python27': ('python2.7', 'py'),
    'python36': ('python3.6', 'py'),
    'coffee': ('nodejs4.3', 'coffee')
}


def setup_parser(parser):
    parser.add_argument('function_name', type=str, help='the base name of the function')
    parser.add_argument('--nodir', help='do not create a directory', action='store_true')
    parser.add_argument('--runtime', default='python36', choices=runtimes.keys(), help='which lambda runtime '
                                                                                       '(default: %(default)s')


def run(args):
    fname = args.function_name

    runtime, ext = runtimes[args.runtime]
    filename = f"{fname}.{ext}"
    manifest = {
        "blambda": "manifest",
        "dependencies": {},
        "options": {
            "Description": fname,
            "Timeout": 300,
            "Runtime": runtime
        },
        "permissions": [],
        "source files": [filename]
    }

    if args.nodir:
        handler_path = filename
        manifest_path = "{}.json".format(fname)
    else:
        if not os.path.exists(fname):
            os.makedirs(fname)
        handler_path = os.path.join(fname, filename)
        manifest_path = os.path.join(fname, "{}.json".format(fname))

    with open(handler_path, 'w') as f:
        if 'python' in args.runtime:
            f.write('def lambda_handler(event, context):\n    return event')
        else:
            f.write('exports.handler = (event, context) ->\n    event')

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=4, sort_keys=True)
