# -*- coding: utf-8 -*-

import os
from os.path import expanduser
from datetime import datetime, date, timedelta

# DATA_DIR
data_dir = os.path.join(expanduser('~'), 'data')
# 配置log文件路径
log_root_path = os.path.join(data_dir, 'logs')
# 配置log文件的名字
log_names = 'nps_'+str((date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")) + '.log'
# 配置数据库信息
db_config = {
    'user': 'root',
    'passwd': '',
    'host': '127.0.0.1',
    'port': 3306,
    'db': 'log_analysis',
    'charset': 'utf8'
}
# 数据库类型配置
db_type = 'mysql'
