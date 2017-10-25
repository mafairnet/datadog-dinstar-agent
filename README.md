Dinstar Integration for Datadog
===================

DataDog Agent plugin for the Dinstar Hardware.

Prerequisites
-----------
- Datadog

Installation
-----------

Get the module files for the datadog agent.

```
cd /usr/src/
yum install git -y
git clone  https://github.com/mafairnet/datadog-dinstar-agent.git
cd datadog-dinstar-agent/
```

Copy the module files to the datadog directories.

```
cp -R checks.d/dinstar_dwg2000f.py /opt/datadog-agent/agent/checks.d/
cp -R conf.d/dinstar_dwg2000f.yaml /etc/dd-agent/conf.d/
```

Edit the configuration file for the module for the specific Dinstar model.

Dinstar DWG2000F
```
nano /etc/dd-agent/conf.d/dinstar_dwg2000f.yaml
```

Insert the IP, Name, User and Password for the Vega.

```
init_config:
	instances:
		- host: 0.0.0.0         #dinstar adress
          name: dinstar_name       #dinstar name
          user: user            #dinstar user
          secret: pass          #dinstar user pass
```

Restart  the datadog service.

```
/etc/init.d/datadog-agent restart
```

Check the datadog service status.

```
/etc/init.d/datadog-agent info
```

The output should be like the next text.

```
     dinstar_*
    ----------------
      - instance #0 [OK]
      - Collected 4 metrics, 0 events & 1 service check

```