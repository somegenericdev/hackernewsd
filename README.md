# hackernewsd

![image info](logo.png)

Daemon that exposes an RSS feed containing any Hackernews or Lobsters stories that match your list of queries.

# Install - Windows

1. Create in your home folder (C:\Users\YOUR_USERNAME) a file called ".hackernewsdrc". <br> 
Replace the queries in the example below with whatever keywords you want the daemon to look for. <br>
Should you want to expose the daemon's web API to the internet you can set the `host` parameter to `0.0.0.0`.

```
{
	"queries": [ ".NET", "C#", "Microsoft", "CLR", "F#", "Mono" ],
	"host": "127.0.0.1",
	"port": 5555
}
```

2. Download the [latest release](https://github.com/somegenericdev/hackernewsd) and extract the executable
3. Move the executable to the startup application folder (C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup)

# Install - Linux

1. Create in your home folder (/home/YOUR_USERNAME) a file called ".hackernewsdrc". <br> 
Replace the queries in the example below with whatever keywords you want the daemon to look for. <br>
Should you want to expose the daemon's web API to the internet you can set the `host` parameter to `0.0.0.0`.


```
{
	"queries": [ ".NET", "C#", "Microsoft", "CLR", "F#", "Mono" ],
	"host": "127.0.0.1",
	"port": 5555
}
```

2. Download the binary
```
cd ~
curl -JOL "https://github.com/somegenericdev/hackernewsd/releases/download/v3.0.0/hackernewsd-v3.0.0-linux64.zip" && unzip hackernewsd-v*-linux64.zip && sudo mv hackernewsd /bin/hackernewsd
chmod +x /bin/hackernewsd
chown $USER:$USER /bin/hackernewsd
```
3. Create a systemd service

```
cd /etc/systemd/system
sudo touch hackernewsd.service
sudo tee -a hackernewsd.service > /dev/null <<EOT
[Service]
Type=simple
ExecStart=/bin/hackernewsd
WorkingDirectory=$HOME
Restart=always
RestartSec=5
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=%n
User=$USER
Group=$USER
EOT

sudo systemctl start hackernewsd
sudo ln -s /etc/systemd/system/hackernewsd.service /etc/systemd/system/multi-user.target.wants/hackernewsd.service
sudo systemctl daemon-reload
```

# Usage

The daemon exposes 4 RSS feeds (2 for Hackernews and 2 for Lobsters), which you can add to your RSS reader of choice:

```
http://127.0.0.1:5555/feed_hn_blog.xml
http://127.0.0.1:5555/feed_hn.xml
http://127.0.0.1:5555/feed_lobsters_blog.xml
http://127.0.0.1:5555/feed_lobsters.xml
```

The `_blog` feeds point to the URL of the stories (usually an external blog), while the other ones point to the Hackernews/Lobsters URL itself.

# Build from source

1. Install the dependency list
```
 pip install -r requirements.txt 
```
2. Install pyinstaller
```
pip install -U pyinstaller
```
3. Build the project with pyinstaller
```
pyinstaller --noconsole --onefile src/app.py
```






