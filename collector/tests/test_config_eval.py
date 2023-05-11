import json
import unittest
from configparser import ConfigParser
from typing import List, Dict


class MyTestCase(unittest.TestCase):
    def test_eval_pot(self):
        conf = ConfigParser()
        # get conf from test file
        conf.read("config_test.ini")
        pots: List = json.loads(conf["ASSETS"]["pots"])
        print(conf["ASSETS"])
        print(pots)
        for pot_dict in pots:
            print(pot_dict)

        print("--------------- Shelf from config ----------------")
        shelf_dict: Dict = json.loads(conf["ASSETS"]["shelf"])
        print(shelf_dict)

if __name__ == '__main__':
    unittest.main()
