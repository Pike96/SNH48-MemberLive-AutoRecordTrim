from urllib import request
import json
import time
import re
import ffmpeg

api48 = 'https://plive.48.cn/livesystem/api/live/v1/memberLivePage'
headers = {
    'os': 'android',
    'User-Agent': 'Mobile_Pocket',
    'IMEI': '864394020228161',
    'token': '0',
    'version': '5.0.1',
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


def record(name):
    last_stamp = int(time.time() * 1000)
    form = '{"lastTime":%s,"limit":20,"groupId":0,"memberId":0,"type":0,"giftUpdTime":1490857731000}' % \
           str(last_stamp)
    try:
        response_json = postform(api48, form, headers)
        response_dict = json.loads(response_json)
        print('Received ' + time.strftime("%b%d-%H-%M-%S", time.localtime(last_stamp / 1000)))
    except:
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
