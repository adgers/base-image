import datetime
import time
from dateutil.relativedelta import relativedelta

from elasticsearch import Elasticsearch
import re

# es = Elasticsearch("http://192.168.2.100:31516")
#
#
# index = es.indices.get_alias().keys()
#
# print(index)


class EsSnapshot():
    def __init__(self, Es):
        self.Es = Es

    def date_range(self,date_s):
        """
        返回删除的日期
        :param date_s:
        :return:
        """
        del_date = str((datetime.datetime.fromtimestamp(time.time()) - relativedelta(days=date_s)).strftime("%Y.%m.%d"))
        return del_date

    #
    def indics(self,date_s,index_pre):
        """
        返回匹配的所有索引
        :param date_s:
        :param index_pre:
        :return:
        """
        indics = es.indices.get_alias().keys()
        delete_date = self.date_range(date_s)
        indics_list = []
        delete_list = []
        for index in indics:
            if re.search('^{}'.format(index_pre), index) :
                indics_list.append(index)
        for index_delet in indics_list:
            if delete_date in index_delet:
                # print(index_delet)
                delete_list.append(index_delet)
        return  delete_list

    # 创建快照
    def create_snapshot(self, *args):
        """
        对前一天的数据进行快照 传值 是两个。date_s index_pre
        :param args:
        :return:
        """
        create_sna_index = self.indics(args[0], args[1])[0]
        # print("创建快照：snapshot_%s" % (create_sna_index))
        flag = self.Es.snapshot.create(repository="es_hw_obsback",
                                snapshot="snapshot_{}".format(create_sna_index))
        return flag

    def delete_index(self, *args):
        """
        对7天前的索引进行删除
        :param args:
        :return:
        """
        delte_sna_index = self.indics(args[0],args[1])
        print("删除索引：删除7天前的索引 {}".format(delte_sna_index))
        flag = self.Es.indices.delete(index=delte_sna_index)
        return flag


if __name__ == '__main__':
    es = Elasticsearch("http://192.168.2.100:32298")
    excute = EsSnapshot(es)
    create_sna_index = excute.indics(1,"k8s")[0]
    print(create_sna_index)
    # delete_sna = excute.indics(7,'k8s')[0]
    # print(create_sna_index)
    try:
        # 一天前的索引进行创建索引快照
        create_snap_index = excute.indics(1,'k8s')[0]
        print("创建名称为：%s" % create_snap_index)
        snap_flag = excute.create_snapshot(1,'k8s')

       # 七天前的索引数据进行删除
        delete_index = excute.indics(7, 'k8s')[0]
        print("删除的索引名称为：%s"%delete_index)
        delete_flag = excute.delete_index(7,'k8s')

    except Exception as  e:
        print("备份索引失败。。。。%f"%e)

