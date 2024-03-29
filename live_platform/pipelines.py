# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from twisted.enterprise import adbapi
from datetime import datetime

class LivePlatformPipeline(object):
    '''保存到数据库中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行'''

    def __init__(self, dbpool):
        self.dbpool = dbpool


    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        #读取settings中配置的数据库参数
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            # cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....

        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    def open_spider(self, spider):
        spider.conn = MySQLdb.connect(user='root', passwd='root', db='platform', host='127.0.0.1', charset="utf8",
                                    use_unicode=False)
        spider.cursor = spider.conn.cursor()
        param = (spider.des,)
        spider.cursor.execute("delete from index_platform where platform_name = %s", param)
        spider.conn.commit()

    def spider_closed(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()


    # 写入数据库中
    # SQL语句在这里
    # def _conditional_update(self, tx, item):
    #     sql = "update index_platform set status = 0 where room_id = %s and status = 1"
    #     params = (item['room_id'],)
    #     tx.execute(sql, params)

    def _conditional_insert(self, tx, item):
        time = datetime.now()

        params = (item['room_id'], item['platform_name'],)

        tx.execute("select 1 from index_platform_bak where room_id = %s and platform_name = %s", params)
        ret = tx.fetchone()

        if not ret:
            sql = "insert into index_platform_bak(platform_name,platform_type,channel_name,channel_type,room_id,name,watch_num,follow_num,room_desc,room_thumb,url,room_status,time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            params = (item['platform_name'], item['platform_type'], item['channel_name'], item['channel_type'], item['room_id'], item['name'], item['watch_num'], item['follow_num'],item['room_desc'],item['room_thumb'],item['url'],item['room_status'],time)
            tx.execute(sql, params)

        sql_insert = "insert into index_platform(platform_name,platform_type,channel_name,channel_type,room_id,name,watch_num,follow_num,room_desc,room_thumb,url,room_status,time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (
        item['platform_name'], item['platform_type'], item['channel_name'], item['channel_type'], item['room_id'],
        item['name'], item['watch_num'], item['follow_num'], item['room_desc'], item['room_thumb'], item['url'],
        item['room_status'], time)
        tx.execute(sql_insert, params)

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue