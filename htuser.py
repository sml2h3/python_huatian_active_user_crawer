#coding=utf-8
import sys
import json
import requests
import threading
from logger import Logger

logger = Logger('collect.py')


class GetHTuser(threading.Thread):
    def __init__(self, lock, threadName):
        super(GetHTuser, self).__init__(name=threadName)
        self.lock = lock

    def run(self):
        global X
        global Y
        global access_token
        global signatureNear
        global deviceNo
        global imei
        global NearUrl
        global InfoUrl
        is_false = True
        is_over = True
        is_page_over = True
        p = 1
        while is_false == True:
            is_over = True
            p = 1
            self.lock.acquire()
            tem_x = X
            tem_y = Y
            X = X + 2
            self.lock.release()
            while is_over:
                is_page_over = True
                p = 1
                if tem_y > 360:
                    is_over = False
                    continue
                while is_page_over == True:
                    try:
                        logger.info('正在检索X:'+str(tem_x)+',Y:'+str(tem_y)+"的第"+str(p)+"页")
                        GetNear = NearUrl + access_token
                        headers = {
                            "protocol": "http",
                            "signature": signatureNear,
                            "User-agent":"Huatian App Android 5.1.1 Xiaomi v3.13.0 build 3940",
                            "device_info": '{"imei": "'+ imei +'"}',
                            "deviceNo": deviceNo,
                            "device_model": "Redmi Note 3",
                            "channel": "xiaomi_huatian",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "charset" : "UTF-8",
                            "Host": "love.163.com",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip",
                            "Content-Length": "1082"
                        }
                        data = {
                            "access_token": access_token,
                            "longitude": str(tem_x),
                            "pageSize": "20",
                            "latitude": str(tem_y),
                            "pageNo": str(p),
                            "deviceInfo": "%7B%22datatype%22%3A%22aimt_datas%22%2C%22id_ver%22%3A%22Android_1.0.1%22%2C%22rdata%22%3A%22e8Ycs%2FFNIWxj9ZpfLcrsJlUFMWAeHBCk899tNkPth0gEAchZ0cqav06hq4R8Hjv60ZLD0XR%2FljFtB8V9WAO4yP4YOd7Oe9keTX1bLtG23X2gxZS1wEKHhM2DhCfRECXHTCsB%2BWP%2BRvIfN5V7F9hQfzdEZWw5%2FkN3bBNC4KN6VbYh9SLb2EkE7rTaTZhX0DoZMe0WJfK6K9gWCQd8CoNT3oFiXCZHBz7Nr52EX7mgy6QpzAjLkgJ%2Fyd%2F7EPh6WRt%2BU8%2BQIAxOnKy9xAOrLe3R0vAtN1p4LwQM2yqSQl4bBUQoFFkijW5OyOwtedsQJBJkiem6QMzBKjbalSQstYjWw3XFD8CvH62C%2BJ%2BIKICgZvBWFpH%2BPCAfB4uQJLbdRFb7M8Dceys%2Fb%2BxIJzmAIgDeL5ezhIkTqmKOaqC5RPdLz4O%2BsAK8AohmAKwcCm4sclKv08uWbPXZMGJ3s3d58PrcaaYR%2Brizfyf0aDZAi9VClseLt9K6RCIMYekqKzN2mOtogqHM8gD0i2B0B2C6rb0x%2Bm0PQZg4O0tFxuHtPH6C%2BIqnUzR8bjK97rzMjGqwX%2BpfVhaR%2FjwgHweLkCS23URW%2B5l9SNDQPme6UxP1Jm2nVIs%3D%22%2C%22rk%22%3A%22pgjII9NOrp5dEWT90JD4UwH9VXQpgCi1g1Fb1R3qQrwpGR0O1bW0qIuY0Aq1S4WtspMT5Nms%2FaEA7QxqIDQMDL9Exwnk%2BSXx9n3vuyZv0ffyGZnQxueoSBMEaTeJd4ueCcUlMC5XigCwS3RtdriFH5bdjd8knSYeCbciRHkFDHA%3D%22%7D%0A&"
                        }
                        json_data = requests.post(GetNear, headers=headers, data=data).text
                        is_page_over = userdeal(json_data)
                        logger.info('第'+str(p)+'页的返回值为：'+str(is_page_over))
                        p = p + 2
                    except requests.RequestException as e:
                        logger.error(e)
                tem_y = tem_y + 1


def userdeal(json_data):
    n = 0
    json_data = json.loads(json_data)
    userList = json_data['dataList']
    for i in userList:
        n = n + 1
        user = i['user']
        id = user['id']
        name = user['name']
        avatar = user['avatar']
        age = user['age']
        height = user['height']
        sex = user['sex']
        if sex == '1':
            sexs = '男'
        else:
            sexs = '女'
        dirname = 'Id-'+id+'-sex-'+sexs+'-name-'+name
        diricon = 'Id-'+id+'-sex-'+sexs+'-name-'+name +'/avatar'
        try:
            m = mkdir(diricon)
        except Exception as e:
            logger.error(e)
        if m:
            logger.info('生成id为'+id+'的信息文件夹成功')
            f2 = open(dirname+'/user.data', 'w')
            info = '{"id":"'+id+'","name":"'+name+'","age":"'+age+'","height":"'+height+'","sex":"'+sexs+'"}'
            f2.write(info)
            ir = requests.get(avatar)
            if ir.status_code == 200:
                open(diricon+'/logo.jpg', 'wb').write(ir.content)
                open('allavatar/'+id+'.jpg', 'wb').write(ir.content)
        else:
            logger.error('生成id为'+id+'的信息文件夹失败')
    if n > 0:
        return True
    else:
        return False



def main():
    global lock
    for i in range(4):
        GetHTuser(lock, "thread-" + str(i)).start()


def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    path = sys.path[0]+"/"+path
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False


if __name__ == '__main__':
    lock = threading.Lock()
    X = 0
    Y = 0
    access_token = 'a00d3844af44fac8c792b04e5a70fc72'
    signatureNear = 'f+4YfITkA01aRjR6Di4Bd/OXTR4='
    signatureInfo = 'eWwuhn+WjcT/OsxWrSP9Ajruy+k='
    deviceNo = 'ac6b6dfb08d43b18c829ce55d3ca5a06'
    imei = '861735037772596'
    NearUrl = "http://love.163.com/api/home/allNearby?access_token="
    InfoUrl = "http://love.163.com/api/user/userPageInfo?access_token="
    mkdir('allavatar')
    main()
