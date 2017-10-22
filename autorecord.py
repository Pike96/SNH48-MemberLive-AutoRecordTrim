from urllib import request
import json
import time
import re
import ffmpeg
# import subprocess
# from win10toast import ToastNotifier

api48 = 'https://plive.48.cn/livesystem/api/live/v1/memberLivePage'
headers = {
    'os': 'android',
    'User-Agent': 'Mobile_Pocket',
    'IMEI': '864394020228161',
    'token': '0',
    'version': '4.0.4',
    'Content-Type': 'application/json;charset=utf-8',
    'Host': 'plive.48.cn',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}


def postform(url, form, headers):
    data = bytes(form, encoding='utf8')
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    return response.read().decode('utf-8')


def record(name, interval):
    last_stamp = int(time.time() * 1000)
    form = '{"lastTime":%s,"limit":20,"groupId":0,"memberId":0,"type":0,"giftUpdTime":1490857731000}' % \
           str(last_stamp)
    try:
        response_json = postform(api48, form, headers)
    except:
        print('Error in getting response ' + time.strftime("%b%d-%H-%M-%S", time.localtime(last_stamp / 1000)))
        return 0
    response_dict = json.loads(response_json)
    if response_dict['status'] == 200:
        # print('json OK')
        print('Received ' + time.strftime("%b%d-%H-%M-%S", time.localtime(last_stamp / 1000)))
    else:
        print('Error in getting response ' + time.strftime("%b%d-%H-%M-%S", time.localtime(last_stamp / 1000)))
        return 0
    try:
        live_list = response_dict['content']['liveList']
    except:
        return 0
    for live_item in live_list:
        title = live_item['title']
        check = re.match("(.)*{}(.)*".format(name), title)
        if check is not None:
            '''
            toaster = ToastNotifier()
            toaster.show_toast("你老婆 " + name + " 直播啦!!!",
                               "直播已经自动开始录制")
                               '''

            print(live_item['title'] + time.strftime("%b%d-%H-%M-%S", time.localtime(last_stamp / 1000)))
            fname = '{}{}.mp4'.format(live_item['title'],
                                      time.strftime("%b%d-%H-%M-%S", time.localtime(last_stamp / 1000)))
            stream = ffmpeg.input(live_item["streamPath"])
            stream = ffmpeg.output(stream, fname)
            try:
                ffmpeg.run(stream)
                # remove()
            except:
                print('Error in recording')
            '''
            subprocess.run('./ffmpeg -i {} {}{}.mp4'
                           .format(live_item["streamPath"],
                                   live_item['title'],
                                   time.strftime("%b%d-%H-%M", time.localtime(last_stamp / 1000))))
                                   '''

def main():
    # name = input("小偶像的姓名：")
    name = "刘崇恬"
    while 1:
        record(name, 10)
        time.sleep(10)
    input('Enter to finish: ')
    return 0


if __name__ == '__main__':
    main()
