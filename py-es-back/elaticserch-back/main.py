import datetime
import time

from utils.RequestUtils import Request



# 因为es 快照备份需要时间去创建，本分昨天的索引删除7天前的索引数据

base_url = "http://192.168.2.100:30188/"

# set 20  days ago
del_date = datetime.datetime.now() - datetime.timedelta(days=15)
del_date = del_date.strftime('%Y.%m.%d')
del_index = 'k8s-' + del_date

# back date
back_date = datetime.datetime.now() - datetime.timedelta(days=1)
back_date = back_date.strftime('%Y.%m.%d')
back_index = 'k8s-' + back_date

request = Request()

class EsBack:
    def checkSnapshop(self,uri):
        """
        检查快照仓库是否存在
        :param url:
        :return:
        """
        url = base_url + uri
        print(url)
        res = request.get(url)
        if res['code'] == 200:
            print("快照仓库已经存在")
        else:
            print("快照仓库不存在，请先检查快照仓库")
        return res

    def creatIndexBack(self,index):
        url = base_url + '_snapshot/'+ 'es_hw_obs/' + index
        body = {
            "indices": index
        }

        """
        创建es 的索引快照
        :param url: 
        :return: 
        """
        res = request.post(url,json=body)
        if res['code'] == 200:
            print("%s索引快照创建成功"%index)
        else:
            print("%s索引快照创建失败"%index)
        return res

    def deleteIndex(self,index):
        url = base_url + index
        res = request.delete(url)
        if res['code'] == 200:
            print("%s索引删除成功..."%index)
        else:
            print("%s索引删除失败..."%index)
        return res



def run_main():
    es = EsBack()

    s3_store = '_snapshot/es_hw_obs'


    # steps1 check store s3 is esxit
    s3_res = es.checkSnapshop(s3_store)
    print(s3_res)
    # steps2 create index snapshot
    snapshot = es.creatIndexBack(back_index)
    print(snapshot)
    time.sleep(10)
    # step3 delete snapshot index
    delete = es.deleteIndex(del_index)
    print(delete)

if __name__ == '__main__':

    run_main()
