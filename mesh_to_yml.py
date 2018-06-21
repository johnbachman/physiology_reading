import logging
from os.path import join
from copy import deepcopy
from collections import defaultdict
import yaml

logger = logging.getLogger('mesh_to_yml')


mesh_path = 'mesh_data/ascii'


def parse_descriptors_ascii(filename):
    with open(filename, 'rt') as f:
        lines = [line.strip() for line in f.readlines()]

    def pipe_split(s):
        return s.split('|')[0]
    def new_record():
        return {'examples': [], 'descriptions':[], 'locations': []}
    records = {}
    ui = None
    cur_record = new_record()
    for line in lines:
        if not line:
            continue
        if line == '*NEWRECORD':
            if ui is not None:
                records[ui] = cur_record
                cur_record = new_record()
            continue
        # Split the line into key and data
        if line.startswith('PRINT ENTRY'):
            key = 'PRINT ENTRY'
            data = pipe_split(line.split(' ', maxsplit=3)[3])
        else:
            fields = line.split(' ', maxsplit=2)
            if len(fields) != 3:
                continue
            key, data = (fields[0], pipe_split(fields[2]))
        # Set the unique identifier
        if key == 'UI':
            ui = data
        # The MH (Mesh Heading) line contains the entry name
        elif key == 'MH':
            cur_record['name'] = data
            cur_record['examples'].append(data)
        # ENTRY and PRINT ENTRY contain synonyms/alternative names
        elif key == 'ENTRY' or key == 'PRINT ENTRY':
            cur_record['examples'].append(data)
        elif key == 'MS':
            cur_record['descriptions'].append(data)
        elif key == 'MN':
            cur_record['locations'].append(data)
        else:
            pass
            #cur_record[key] = data
    return records


def recursive_dict():
    return defaultdict(recursive_dict)


def insert_node(d, key_list, data):
    # Base case
    if len(key_list) == 0:
        if 'records' in d:
            d['records'].append(data)
        else:
            d['records'] = [data]
    else:
        child_dict = d[key_list[0]]
        insert_node(child_dict, key_list[1:], data)


def build_hierarchy(desc):
    hierarchy = recursive_dict()
    for ui, record in desc.items():
        tree_numbers = record.get('locations')
        record.pop('locations')
        if not tree_numbers:
            continue
        # Check if this is a root node
        for tn in tree_numbers:
            tn_keys = tn.split('.')
            key_list = ['.'.join(tn_keys[0:depth])
                        for depth in range(1, len(tn_keys)+1)]
            insert_node(hierarchy, key_list, record)
    return hierarchy


def build_yaml(key, values):
    subdict = {}
    if key == 'records':
        node = [{'OntologyNode': v} for v in values]
    else:
        entries = []
        for k, v in values.items():
            entries.extend(build_yaml(k, v))
        node = [{key: entries}]
    return node

if __name__ == '__main__':
    desc = parse_descriptors_ascii(join(mesh_path, 'd2018.bin'))
    hierarchy = build_hierarchy(desc)
    root_hierarchy = {'MESH': hierarchy}

    mesh = build_yaml('MESH', hierarchy)
    yaml.Dumper.ignore_aliases = lambda *args : True
    with open('mesh.yml', 'wt') as f:
        yaml.dump(mesh, f, default_flow_style=False)

