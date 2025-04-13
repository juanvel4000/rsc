import requests

class RSCClient:
    def __init__(self, server):
        self.server = server
        self.uniqid = None

    def login(self, uniqid):
        self.uniqid = uniqid

    def create(self, username):
        res = requests.post(self.server + '/user/create', data={"username": username})
        data = res.json()
        if data['code'] == 200:
            self.uniqid = data['uniqid']
            return data['uniqid']
        else:
            return data.get('code', 500), data.get('message', 'Unknown error')

    def send(self, message):
        if not self.uniqid:
            return {"error": "Not logged in"}
        res = requests.post(self.server + "/message/send", data={
            "uniqid": self.uniqid,
            "contents": message
        })
        data = res.json()
        if data['code'] == 200:
            return True
        else:
            return data.get('code', 500), data.get('message', 'Failed to send message')

    def get(self):
        res = requests.get(self.server + "/message/get")
        return res.json()

    def info(self):
        res = requests.get(self.server + "/node/info")
        return res.json()
    def userinfo(self, username):
        res = requests.get(self.server + "/user/info", params={"username": username})
        if not res.json():
            return {"code": 404, "message": "could not find the user"}
        return res.json()
