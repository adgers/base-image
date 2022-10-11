import requests



# 重构
# 1、创建类
class Request:
    def __init__(self):
       pass

    # 2、定义公共的方法
    def requests_api(self, url, data=None, json=None, headers=None, cookies=None, method="get"):
        if method == 'get':
            # 发起get 请求
            print("发起get 请求...")
            r = requests.get(url, data=data, json=json, headers=headers, cookies=cookies)
        elif method == 'post':
            print("发送post请求")
            r = requests.post(url, data=data, json=json, headers=headers, cookies=cookies)
        # 获取我们的请求返回内容
        elif method == 'put':
            print("发送put请求")
            r = requests.put(url, data=data, json=json, headers=headers, cookies=cookies)
        elif method == 'delete':
            print("发送delete请求")
            r = requests.delete(url, data=data, json=json, headers=headers, cookies=cookies)
        code = r.status_code
        try:
            body = r.json()
        except Exception as e:
            body = r.text
            print("返回的类型不是json：", e)

        # 内容保存到字典
        res = dict()
        res["code"] = code
        res["body"] = body
        # 字典进行返回
        return res

    # 3、重构get和post
    def get(self, url, **kwargs):
        return self.requests_api(url, method="get", **kwargs)

    def post(self, url, **kwargs):
        return self.requests_api(url, method="post", **kwargs)
    def put(self,url, **kwargs):
        return self.requests_api(url,method="put",**kwargs)
    def delete(self,url,**kwargs):
        return self.requests_api(url,method="delete", **kwargs)