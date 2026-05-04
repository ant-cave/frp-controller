import subprocess
import json
import lib
import time


# 获取所有配置
configs = lib.get_config()
allscreens=lib.get_all_screens()
for pid in configs:
    name=configs[pid]
    for current in allscreens:
        if current==name:
            print(name)
    