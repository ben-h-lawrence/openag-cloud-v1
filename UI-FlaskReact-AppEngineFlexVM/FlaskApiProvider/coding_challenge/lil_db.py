import json
import datetime
from os import path

dir_path = path.dirname(path.realpath(__file__))
dbfile = path.join(dir_path, 'fake_db.json')

def write(key, entity):
    def datetime_handler(obj):
        if isinstance(obj, datetime.datetime):
            return obj.__str__()
        else:
            raise TypeError
    if not path.exists(dbfile):
        file = open(dbfile, 'w')
    with open(dbfile, 'r+') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = {}
        data[key] = data.get(key) or []
        data[key].append(entity)
        f.seek(0)
        json.dump(data, f, default=datetime_handler)
        f.truncate()

def query(key, values):
    result = {}
    if not len(values):
        return result;
    with open(dbfile, 'r') as infile:
        data = json.load(infile)
        for row in data.get(key):
            if is_subdict(values, row):
                result = row
                break
    return result

def update(key, values, pks):
    item = query(key, pks)
    if len(item):
        item.update(values)
        delete(key, pks)
        write(key, item)
        return 1
    return 0

def delete(key, pks):
    if not len(pks):
        return 0;
    def datetime_handler(obj):
        if isinstance(obj, datetime.datetime):
            return obj.__str__()
        else:
            raise TypeError
    if not path.exists(dbfile):
        file = open(dbfile, 'w')
    with open(dbfile, 'r+') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = {}
        data[key] = data.get(key) or []
        new_data = [entity for entity in data.get(key) if not is_subdict(pks, entity)]
        data[key] = new_data
        f.seek(0)
        json.dump(data, f, default=datetime_handler)
        f.truncate()

def is_subdict(small, big):
    return dict(big, **small) == big
