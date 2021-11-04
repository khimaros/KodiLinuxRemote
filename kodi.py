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
        response = self.InvokeMethod('Player.GetItem', {'playerid': self.player_id})
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
        self.InvokeMethod('Player.PlayPause', {'playerid': self.player_id})

    def Stop(self):
        self.InvokeMethod('Player.Stop', {'playerid': self.player_id})

    def Previous(self):
        self.InvokeMethod('Player.GoTo', {'playerid': self.player_id, 'to': 'previous'})

    def Next(self):
        self.InvokeMethod('Player.GoTo', {'playerid': self.player_id, 'to': 'next'})

    def MuteToggle(self):
        self.InvokeMethod('Application.SetMute', {'mute': 'toggle'})

    def VolumeIncrease(self):
        self.InvokeMethod('Application.SetVolume', {'volume': 'increment'})

    def VolumeDecrease(self):
        self.InvokeMethod('Application.SetVolume', {'volume': 'decrement'})

    def InvokeMethod(self, method, params=None):
        print('=>', self.base_url, method, params)
        jreq = jsonrpcclient.request(method, params)
        auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        print('**', jreq)
        response = requests.post(self.base_url, json=jreq, auth=auth)
        try:
            jresp = jsonrpcclient.parse(response.json())
            result = jresp.result
        except Exception as e:
            print('!!', e, jresp)
        print('<=', result)
        return result
