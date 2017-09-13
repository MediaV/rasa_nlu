from os import walk, mkdir
from shutil import rmtree
from os.path import join

class IdVersionManager():

    def __init__(self, folder):
        self.directory = folder
        # id_version_dict[id][version] = is_active
        self.id_version_dict = {}
        self.load()

    def parse(self, model_name):
        if model_name.startswith('model_'):
            try:
                return map(int, model_name[6:].split('-'))
            except ValueError as e:
                raise ValueError('wrong format, model name: {}, error msg: {}'.format(model_name, e))
        else:
            raise ValueError('wrong format of model name !')

    def next_model_version(self, model_id):
        if model_id in self.id_version_dict:
            return max(self.id_version_dict[model_id].keys()) + 1
        else:
            return 1

    def next_model_id(self):
        ids = self.id_version_dict.keys()
        if len(ids) == 0:
            return 1
        else:
            return max(ids) + 1

    def lookup_model(self, lookup_is_active, lookup_page, lookup_limit):
        lookup_result = []
        index = 0
        for model_id, model_version_dict in self.id_version_dict.iteritems():
            for model_version, model_is_active in model_version_dict.iteritems():
                if model_version > 0 and (lookup_is_active == False or model_is_active == True):
                    index += 1
                    if lookup_page * lookup_limit < index <= (lookup_page + 1) * lookup_limit:
                        d = {}
                        d['id'] = model_id
                        d['version'] = model_version
                        d['is_active'] = model_is_active
                        lookup_result.append(d)
        return lookup_result

    def get_model_version(self, model_id):
        model_data = {'id': model_id, 'versions': []}
        is_active = False
        for key, value in self.id_version_dict[model_id].iteritems():
            if key > 0:
                model_data['versions'].append({'version': key, 'is_active': value})
                if value == True:
                    is_active = True
        model_data['is_active'] = is_active
        return {'model': model_data}

    def delete_model(self, model_id):
        for (dirpath, dirnames, _) in walk(self.directory):
            for model_name in dirnames:
                id_and_version = self.parse(model_name)
                if len(id_and_version) == 2 and id_and_version[0] == model_id:
                    dir_to_delete = join(dirpath, model_name)
                    rmtree(dir_to_delete)
            break

    def disable_model(self, model_id):
        version_dict = self.id_version_dict[model_id]
        for key in version_dict:
            version_dict[key] = False

    def enable_model(self, model_id, model_version):
        version_dict = self.id_version_dict[model_id]
        for key, value in version_dict.iteritems():
            if value == True and key != model_version:
                raise ValueError('model {} with version {} is already enabled, try use switch command'.format(model_id, model_version))
        self.id_version_dict[model_id][model_version] = True

    def switch_model(self, model_id, model_version):
        version_dict = self.id_version_dict[model_id]
        for key, value in version_dict.iteritems():
            if value == True and key != model_version:
                version_dict[key] = False
                break
        self.id_version_dict[model_id][model_version] = True

    def load(self):
        f = []
        for (_, dirnames, _) in walk(self.directory):
            f.extend(dirnames)
            break
        for model_name in f:
            if model_name.startswith('model_'):
                parse_result = self.parse(model_name)
                if len(parse_result) == 2:
                    model_id, model_version = parse_result
                else:
                    continue
                if not model_id in self.id_version_dict:
                    self.id_version_dict[model_id] = {}
                self.id_version_dict[model_id][model_version] = False
