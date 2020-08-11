import time
import pymysql


def get_time():
    """向服务器同步时间，转换时间格式"""
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")

def get_conn():
    """从数据库获取数据，连接，游标"""
    # 创建连接
    conn = pymysql.connect(host="localhost",
                           user="root",
                           password="123456",
                           db="cov",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor

def close_conn(conn, cursor):
    """关闭数据库游标和连接"""
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def query(sql,*args):
    """
    封装通用查询
    :param sql:
    :param args:
    :return: 返回查询到的结果，((), ())的形式
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res

def test():
    sql = "select * from details"
    res = query(sql)
    return res[0]

def get_c1_data():
    """
    返回大屏div id=c1的数据
    因为会更新多次数据，取时间戳最新的那组数据
    """
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal)," \
          "sum(dead) " \
          "from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    res = query(sql)
    return res[0]

def get_c2_data():
    """返回各省数据"""
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1)" \
          "group by province"
    res = query(sql)
    return res

def get_l1_data():
    """返回累计趋势数据"""
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res
	
def get_l2_data():
	""""""
	sql = "select ds,confirm_add,suspect_add from history"
	res = query(sql)
	return res

def get_r1_data():
    sql = 'select city,confirm from ' \
          '(select city,confirm from details ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province not in ("湖北","北京","上海","天津","重庆") ' \
          'union all ' \
          'select province as city,sum(confirm) as confirm from details ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province in ("北京","上海","天津","重庆") group by province) as a ' \
          'order by confirm desc limit 5'
    res = query(sql)
    return res

def get_r2_data():
    sql = "select content from hotsearch order by id desc limit 20"
    res = query(sql)
    return res


if __name__ == "__main__":
    print(get_r2_data())