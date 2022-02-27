#!/usr/bin/env python3

import kodi
import settings

s = settings.Settings()
ss = s.GetSettings()
c = s.LoadSettings(ss.parser)
k = kodi.Kodi(**c)
k.Connect()

print()
print('### MOVIES ###')
print()
k.InvokeMethod('VideoLibrary.GetMovies')

print()
print('### MOVIE DETAILS ###')
print()
k.InvokeMethod('VideoLibrary.GetMovieDetails', {'movieid': 1, 'properties': ['title', 'year', 'tagline']})

print()
print('### ADDONS ###')
print()
k.InvokeMethod('Addons.GetAddons')

print()
print('### ADDON DETAILS ###')
print()
k.InvokeMethod('Addons.GetAddonDetails', {'addonid': 'plugin.video.youtube', 'properties': ['extrainfo']})

#k.InvokeMethod('Playlist.Add', {'playlistid': 0, 'item': {'file': ...}})
#k.InvokeMethod('Player.Open', {'item': {'file': 'plugin://plugin.video.youtube/?action=play_video&videoid=PSZuPt74e_c'}})

print()
print('### TYPES ###')
print()
i = k.InvokeMethod('JSONRPC.Introspect')
t = i['types']
for typ in t:
    print(typ, t[typ])

print()
print('### METHODS ###')
print()
m = i['methods']
for method in m:
    params = m[method]['params']
    returns = m[method]['returns']
    #print(method, params, '=>', returns)
    #required_params = list(filter(lambda x: 'required' in x, params))
    #print(method, required_params, '=>', returns)
    paramsdocs = []
    for param in params:
        if '$ref' in param:
            paramsdoc = '%s:%s' % (param['name'], param['$ref'])
        elif 'type' in param:
            paramsdoc = '%s:%s' % (param['name'], param['type'])
        if 'required' in param:
            paramsdoc += '*'
        paramsdocs.append(paramsdoc)
    print(method, '('  + ', '.join(paramsdocs) + ')', '=>', returns)

