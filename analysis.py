# -*- coding: utf-8 -*-

import re
import MySQLdb
from config import *
import json


import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


def connect_sql():
    # 创建连接
    try:
        conn = MySQLdb.connect(db_config['host'], db_config['user'], db_config['passwd'],
                               db_config['db'], charset='utf8')
        print("MySQL数据库连接成功！")
    except:
        print("数据库连接失败！")
        exit(1)
    return conn


def analysis():
    # 分析log日志文件,将json数据匹配出来
    result = []
    # 查找到文件handle
    log_path = os.path.join(log_root_path, log_names)
    if not os.path.exists(log_path):
        print u'对不起,' + log_names + u'文件不存在'
        os._exit(0)
    else:
        with open(log_path.decode('utf-8'), 'r') as txt:
            # txt.read().encode('utf-8')
            for line in txt:
                pattern = re.compile(r'yuanli dumping status:(.+)')
                goal = pattern.search(line)
                if goal is not None:
                    result.append(goal.groups()[0])

        return result


def storage():
    # 将匹配出来的数据存储进数据库
    if db_type == 'mysql':
        conn = connect_sql()
        cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        # 获取当前年月日,数据库中查找,如果没有,则添加
        yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
        # nowTime = '2018-08-09'
        cur.execute(
            "SELECT `event`,`user`,`date_time` FROM log WHERE `date_time` = '%s'"%(yesterday))

        if len(cur.fetchall()) == 0:
            data = analysis()
            print data
            # os._exit(0)
            new_data = []
            for x in data:
                # 截取 yuanli dumping status: 字符
                # x = x[22:]
                x = x.decode('gbk')
                x = json.loads(x)
                # print x
                new_data.append((str(x['user']), str(x['event']), str(x['ts']),
                                 str(x['app'] if x['app'] else None),
                                 str(x['city'] if 'city'in x.keys() else None),
                                 str(x['modType'] if 'modType'in x.keys() else None),
                                 str(x['ip'] if 'ip'in x.keys() else None),
                                 str(x['module'] if 'module'in x.keys() else None),
                                 str(x['userName'] if 'userName'in x.keys() else None),
                                 str(x['url'] if 'url'in x.keys() else None),
                                 str(x['modId'] if 'modId'in x.keys() else None),
                                 str(x['conditions'] if 'conditions'in x.keys() else None)
                                 ))

            print new_data

            try:
                sql = 'insert into log(user,event,date_time,app,city,modType,ip,module,userName,url,modId,conditions) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                print new_data
                cur.executemany(sql, new_data)
                conn.commit()
                print ('插入数据')
                conn.close()
                cur.close()
            except MySQLdb.Error as e:
                conn.rollback()
                print("执行MySQL: %s 时出错：%s" % (sql, e))
        else:
            print u'当前日期的数据已经新增过数据库'


def statistics():
    # 统计当前日期,用户操作时间的次数
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
    # nowTime = '2018-08-09'
    # 执行数据库操作
    conn = connect_sql()
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cur.execute("SELECT COUNT(`event`) as num,`event`,`user` FROM log WHERE `date_time` = '%s' GROUP BY `event`,`user`"%(yesterday))

    if len(cur.fetchall()) == 0:
        print str(yesterday) + u'当前日期没有数据'
    else:
        for row in cur:
            print(str(row['user']) + "用户处理事件" + str(row['event']) + "共计" + str(
                row['num']) + "次")

    conn.close()
    cur.close()


def main():
    storage()
    statistics()


if __name__ == '__main__':
    main()
