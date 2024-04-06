## Command-line

Command-line usage is available by running ``meshcot -h``.

```
usage: meshcot [-h] [-c CONFIG_FILE] [-p PREF_PACKAGE]

options:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --CONFIG_FILE CONFIG_FILE
                        Optional configuration file. Default: config.ini
  -p PREF_PACKAGE, --PREF_PACKAGE PREF_PACKAGE
                        Optional connection preferences package zip file (aka data package).
```

## Run as a service / Run forever

1. Add the text contents below a file named `/etc/systemd/system/meshcot.service`  
  You can use `nano` or `vi` editors: `sudo nano /etc/systemd/system/meshcot.service`
2. Reload systemctl: `sudo systemctl daemon-reload`
3. Enable MeshCOT: `sudo systemctl enable meshcot`
4. Start MeshCOT: `sudo systemctl start meshcot`

### `meshcot.service` Content
```ini
[Unit]
Description=MeshCOT - Display Drones in TAK
Documentation=https://meshcot.rtfd.io
Wants=network.target
After=network.target
StartLimitIntervalSec=0
# Uncomment this line if you're running dump1090 & meshcot on the same computer:
# After=dump1090-fa.service

[Service]
RuntimeDirectoryMode=0755
ExecStart=/usr/local/bin/meshcot -c /etc/meshcot.ini
SyslogIdentifier=meshcot
Type=simple
Restart=always
RestartSec=30
RestartPreventExitStatus=64
Nice=-5

[Install]
WantedBy=default.target
```

> Pay special attention to the `ExecStart` line above. You'll need to provide the full local filesystem path to both your meshcot executable & meshcot configuration files.