# src/core/msg_library.py

import random
import json
import os
import time

class MsgLibrary:
    def __init__(self, local_file_path="gitcom_msgs.json"):
        self.local_file_path = local_file_path
        self.msg_data = self.load_msgs()
        self.used_msgs = {action: [] for action in self.msg_data.keys()}
    
    def load_msgs(self):
        if os.path.exists(self.local_file_path):
            with open(self.local_file_path, 'r') as file:
                return json.load(file)
        return {}
    
    def random_msg(self, action_type, commit_index):
        random.seed(commit_index + time.time())  # 使用时间戳和 commit_index 生成随机种子

        available_msgs = list(set(self.msg_data[action_type]) - set(self.used_msgs[action_type]))

        if not available_msgs:
            self.used_msgs[action_type] = []
            available_msgs = self.msg_data[action_type]

        commit_msg = random.choice(available_msgs)
        self.used_msgs[action_type].append(commit_msg)

        return commit_msg
