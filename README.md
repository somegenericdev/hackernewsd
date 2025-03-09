# hackernewsd

Daemon that notifies you of any stories that match your list of queries.


# Install - Windows

`TODO!!!!!`

1. Create in your home folder (C:\Users\YOUR_USERNAME) a file called ".hackernewsdrc". <br> 
Replace the queries in the example below with whatever keywords you want the daemon to look for

```
{
	"queries": [ ".NET", "C#", "Microsoft", "CLR", "F#", "Mono" ]
}
```

2. Clone the project
3. Install the dependencies
```
 pip install -r requirements.txt
```
4. Move the script to the startup application folder 
```
mv hackernewsd.py C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\hackernewsd.pyw
```
 
# Install - Linux

1. Create in your home folder (/home/YOUR_USERNAME) a file called ".hackernewsdrc". <br> 
Replace the queries in the example below with whatever keywords you want the daemon to look for

```
{
	"queries": [ ".NET", "C#", "Microsoft", "CLR", "F#", "Mono" ]
}
```

2. Download the binary
```
cd ~
curl -JOL "https://github.com/somegenericdev/hackernewsd/releases/download/v1.0.2/hackernewsd-v1.0.2-linux64.zip" && unzip hackernewsd-v1.0.1-linux64.zip && sudo mv hackernewsd /bin/hackernewsd
chmod +x /bin/hackernewsd
chown $USER:$USER /bin/hackernewsd
```
3. Create a systemd service

```
cd /etc/systemd/system
sudo touch hackernewsd.service
sudo tee -a hackernewsd.service > /dev/null <<EOT
[Unit]
Description=hackernewsd

[Service]
WorkingDirectory=/bin
ExecStart=/bin/hackernewsd
Restart=always
# Restart service after 10 seconds if the service crashes:
RestartSec=10
KillSignal=SIGINT
SyslogIdentifier=log.hackernewsd
User=USER_HERE
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
EOT

sudo sed -i -e "s/USER_HERE/$USER/g" hackernewsd.service
sudo systemctl start hackernewsd
sudo systemctl enable hackernewsd
```

`TODO, this systemd thing doesnt work, it tries to run as root. try https://askubuntu.com/questions/1371102/running-systemd-service-as-user-rather-than-root`

# Build from source

1. Install the dependency list
```
 pip install -r requirements.txt #windows
 pip install $(cat requirements.txt | grep --invert-match "win11toast") #linux
```
2. Install pyinstaller
```
pip install -U pyinstaller
```
3. Build the project with pyinstaller
```
pyinstaller --noconsole --onefile src/app.py
```

# TODO

Trovare libreria con evento onclick cross platform per notifiche