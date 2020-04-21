from flask import Flask, request
import requests
import json
import schedule
import time

app = Flask(__name__)

client_id = '8558c925300669618b3ba7d9555f799e'
access_token = ''

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/kakao')
def kakao():
    base_url = 'https://kauth.kakao.com/oauth/authorize'
    redirect_uri = 'http://127.0.0.1:5000/oauth'
    scope = 'talk_message'
    payload = base_url + '?client_id=' + client_id + '&redirect_uri=' + redirect_uri + '&response_type=code&scope=' + scope 
    return '<a href='+payload+'>KAKAO LOGIN</a>'

@app.route('/oauth')
def oauth():
    code = request.args.get('code')
    base_url = 'https://kauth.kakao.com/oauth/token'
    data =  {'grant_type' : 'authorization_code',
            'client_id' : client_id,
            'redirect_uri' : 'http://127.0.0.1:5000/oauth',
            'code': code}
    res = requests.request('POST', base_url, data=data)
    global access_token
    access_token = res.json()['access_token']

    while True: 
        schedule.run_pending()
        time.sleep(1)

    return 'Success!'

def job():
    base_url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
    data = {
        'object_type': 'list', 
        'header_title': 'WEEKLY MAGAZINE', 
        'header_link': {
                'web_url' : 'http://www.naver.com',
                'mobile_web_url' : 'http://m.naver.com',
        },
        'contents': [{
            'title': '자전거 라이더를 위한 공간',
            'description': '매거진',
            'image_url': 'https://avatars0.githubusercontent.com/u/19206046?s=460&u=24fce93ccb2fafb950ecb5ec5ba1e384dfe049e0&v=4',
            'link': {
                'web_url' : 'http://www.naver.com',
                'mobile_web_url' : 'http://m.naver.com',
            },
        }, {
            'title': '자전거 라이더를 위한 공간',
            'description': '매거진',
            'image_url': 'https://avatars0.githubusercontent.com/u/19206046?s=460&u=24fce93ccb2fafb950ecb5ec5ba1e384dfe049e0&v=4',
            'link': {
                'web_url' : 'http://www.naver.com',
                'mobile_web_url' : 'http://m.naver.com',
            },
        },]
    }
    
    headers = {'Authorization' : 'Bearer ' + access_token}

    res = requests.request('POST', base_url, data={'template_object':json.dumps(data)}, headers=headers)

if __name__ == '__main__':
    schedule.every().hour.do(job)
    app.run()