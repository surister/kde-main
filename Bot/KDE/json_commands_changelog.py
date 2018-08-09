import json
import os

file_dir = os.path.dirname(__file__)
real_path = file_dir + '/changelog/changelog_list.json'


def get_changelog():

    with open(real_path, 'r') as file:
        return json.load(file)


def read_changelog_version(version):

    with open(real_path, 'r') as file:
        change_log = json.load(file)
        return change_log[version]


def write_changelog(version, features):
    x = get_changelog()
    if version not in x.keys():
        x[version] = features
        with open(real_path, "w") as db:
            json.dump(x, db, indent=3)
