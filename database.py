#
# -*- coding: utf-8 -*-
#
import sys
import json


class Database:
    CONFIG = 'config'
    PACKAGES = 'packages'

    def truncate(self) -> dict:
        self.tables = dict()
        self.tables[self.CONFIG] = dict()
        self.tables[self.PACKAGES] = dict()
        return self.tables

    def __init__(self):
        self.tables = self.truncate()

    def dump(self, json_path: str) -> bool:
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.tables, f, ensure_ascii=True, indent=1, sort_keys=True)
                return True
        except:
            return False

    def load(self, json_path: str) -> bool:
        try:
            with open(json_path) as f:
                self.tables = json.load(f)
                return True
        except:
            return False

    def table_packages(self) -> dict:
        return self.tables[self.PACKAGES]

    def package_add(self, name: str, package_dict: dict) -> bool:
        table = self.table_packages()
        d = table.get(name)
        if d is not None:
            return d
        table[name] = package_dict
        d = table[name]
        return d

    @staticmethod
    def self_test() -> bool:
        json_path = 'database_selftest.json'
        database = Database()
        database.package_add(name='numpy', package_dict={})
        database.package_add(name='numpy', package_dict={})
        database.package_add(name='pandas', package_dict={'key': 'value'})
        database.dump(json_path)
        database.truncate()
        database.load(json_path)
        return True


def main():
    if not Database.self_test():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
