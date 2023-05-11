import ast
import json
import threading
import unittest
from configparser import ConfigParser
from typing import List

# from assets.pot_asset import PotAsset
# from sensors import mcp3008


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
            # thread_pot = threading.Thread(target=pot.read_sensor_data)
            # thread_pot.start()


if __name__ == '__main__':
    unittest.main()
