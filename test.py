from service.supabase import supabase
from realtime.connection import Socket

def callback(data):
    print(data)

URL = supabase.realtime_url + f'/websocket?apikey={supabase.supabase_key}&vsn=1.0.0'
print(URL)
s = Socket(URL)
s.connect()

channel = s.set_channel('realtime:*')
channel.join().on("INSERT", callback)
s.listen()