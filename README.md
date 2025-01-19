# hackernewsd

Daemon that notifies you of any stories that match your list of queries.

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

# Install - Windows

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

2. Clone the project
3. Install the dependencies
```
 pip install -r requirements.txt
```
4. Move the script to the bin folder 
```
mv hackernewsd.py /bin/
```
5. Create a systemd service

```TODO```

# TODO

Trovare libreria con evento onclick cross platform per notifiche