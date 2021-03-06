#!/usr/bin/python
import requests
dinstar_ip = "0.0.0.0"

# Fill in your details here to be posted to the login form.
payload = {
    'username': 'user',
    'password': 'pass'
}

username = 'user'
password = 'pass'

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    #Send Auth Request
    s.auth = (username, password)
    p = s.post('http://' + dinstar_ip + '/', data=payload)

    # An authorised request.
    r = s.get('http://'+dinstar_ip+'/enMobileInfo.htm')
    dinstar_data = r.text
    p.close()
    r.close()
    s.close()


dinstar_results = dinstar_data.split('<tr>')

dinstar_total_channels =0
dinstar_inuse_channels = 0
dinstar_available_channels = 0
dinstar_blocked_channels = 0
dinstar_disconnected_channels = 0
index = 0
channels_signal = []

for chan in dinstar_results:
    if "GSM" in chan:
        chan_data = chan.split('</td><td>')
        if len(chan_data) > 2:
            if "Mobile Registered" in chan_data[4] and "Idle" in chan_data[12] :
                dinstar_available_channels += 1
            if "Alerting" in chan_data[12] :
                dinstar_blocked_channels += 1
            if "Mobile Registered" in chan_data[4] and "Active" in chan_data[12] :
                dinstar_inuse_channels += 1
            if "No SIM Card" in chan_data[4] :
                dinstar_disconnected_channels += 1
            if "signal" in chan_data[7] :
                if "0.gif" in chan_data[7] :
                    channels_signal.insert(index,0)
                if "1.gif" in chan_data[7] :
                    channels_signal.insert(index,1)
                if "2.gif" in chan_data[7] :
                    channels_signal.insert(index, 2)
                if "3.gif" in chan_data[7] :
                    channels_signal.insert(index, 3)
                if "4.gif" in chan_data[7] :
                    channels_signal.insert(index, 4)
                if "5.gif" in chan_data[7] :
                    channels_signal.insert(index, 5)
                if "6.gif" in chan_data[7] :
                    channels_signal.insert(index, 6)
        dinstar_total_channels += 1
    index += 1

print('Total GSM Channels')
print(dinstar_total_channels)

print('GSM InUse Channels')
print(dinstar_inuse_channels)

print('GSM Available Channels')
print(dinstar_available_channels)
print('GSM Disconnected Channels')
print(dinstar_disconnected_channels)

print('Channels Signal Data')
print(channels_signal)