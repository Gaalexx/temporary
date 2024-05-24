from GIGAchat.GigaChat import *

giga = GigaChatSDK(max_tokens=500)

event = "встреча с друзьями"

ans = giga.requestGC(event)

print(ans)
