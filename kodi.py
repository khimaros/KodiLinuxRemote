import requests
import jsonrpcclient
from requests.exceptions import ConnectionError
from settings import Settings

class Kodi():
    player_id = None
    username = None
    password = None

    def __init__(self, username, password, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.username = username
        self.password = password
        self.base_url = 'http://' + self.ip_address + ':' + self.port + '/jsonrpc'

    def Connect(self):
        try:
            # TODO Save settings based on response
            self.GetActivePlayers()
            settings = Settings()
            settings.Save({'ip_address' : self.ip_address, 'port' : self.port, 'username' : self.username, 'password' : self.password})
            return True
        except ConnectionError as conn_error:
            print(conn_error)
            return False

    def Handshake(self):
        try:
            self.player_id = self.GetActivePlayers()
            # print(self.player_id)
            if self.player_id is None:
                currentPlaying = 'Nothing is playing'
            else:
                currentPlaying = self.PlayerGetItem()
            return currentPlaying
        except ConnectionError as conn_error:
            # print(conn_error)
            return False

    def GetActivePlayers(self):
        response = self.InvokeMethod('Player.GetActivePlayers')
        if len(response) == 0:
            return None
        else:
            return response[0]['playerid']

    def PlayerGetItem(self):
        response = self.InvokeMethod('Player.GetItem', {'name': 'playerid', 'value': self.player_id})
        return response['item']['label']

    def InputBack(self):
        self.InvokeMethod('Input.Back')

    def InputLeft(self):
        self.InvokeMethod('Input.Left')

    def InputRight(self):
        self.InvokeMethod('Input.Right')

    def InputSelect(self):
        self.InvokeMethod('Input.Select')

    def InputUp(self):
        self.InvokeMethod('Input.Up')

    def InputDown(self):
        self.InvokeMethod('Input.Down')

    def PlayPause(self):
        self.InvokeMethod('Player.PlayPause', {'name': 'playerid', 'value': self.player_id})

    def Stop(self):
        self.InvokeMethod('Player.Stop', {'name': 'playerid', 'value': self.player_id})

    def Previous(self):
        pass

    def Next(self):
        #response = requests.post(self.url_helper.prepare_url_with_param('Player.GoTo', parent_params), auth=(self.username, self.password))
        pass

    def SetVolume(self, vol_type):
        self.InvokeMethod('Application.SetVolume', {'name': 'volume', 'value': vol_type})

    def InvokeMethod(self, method, params=None):
        print('=>', self.base_url, method, params)
        response = requests.post(self.base_url,
            json=jsonrpcclient.request(method, params),
            auth=requests.auth.HTTPBasicAuth(self.username, self.password),
        )
        result = jsonrpcclient.parse(response.json()).result
        print('<=', result)
        return result
