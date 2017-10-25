#
# Sangoma Vega 50 Agent for DataDog
# By mafairnet [Miguel Angel Torres Govea]
#

import requests
from checks import AgentCheck

class SvegaCheck(AgentCheck):

    def check(self, instance):

        if 'host' not in instance:
            self.log.error('host not defined, skipping')
        if 'name' not in instance:
            self.log.error('name not defined, skipping')
        if 'user' not in instance:
            self.log.error('user not defined, skipping')
            return
        if 'secret' not in instance:
            self.log.error('secret not defined, skipping')
            return

        # Fill in your details here to be posted to the login form.
        payload = {
            'username': instance['user'],
            'password': instance['secret']
        }

        username = instance['user']
        password = instance['secret']



        ## CONNECT
        ## Use 'with' to ensure the session context is closed after use.
        with requests.Session() as s:
            #Send Auth Request
            s.auth = (username, password)
            p = s.post('http://'+instance['host']+'/', data=payload)

            ## DINSTAR DATA  
            # An authorised request.
            r = s.get('http://'+instance['host']+'/enMobileInfo.htm')
            dinstar_data = r.text
            ## Close session
            p.close()
            r.close()
            s.close()

        dinstar_results = dinstar_data.split('<tr>')

        dinstar_total_channels =0
        dinstar_inuse_channels = 0
        dinstar_available_channels = 0
        dinstar_blocked_channels = 0
        dinstar_disconnected_channels = 0

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
                dinstar_total_channels += 1
            
        self.gauge('dinstar.'+instance['name']+'.dinstar.total.channels',dinstar_total_channels)
        self.gauge('dinstar.'+instance['name']+'.dinstar.inuse.channels',dinstar_inuse_channels)
        self.gauge('dinstar.'+instance['name']+'.dinstar.available.channels',dinstar_available_channels)
        self.gauge('dinstar.'+instance['name']+'.dinstar.disconnected.channels',dinstar_disconnected_channels)