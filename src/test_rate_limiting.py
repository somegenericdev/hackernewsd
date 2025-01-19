import requests
i = 0
out = ""

while i < 500:
    resp = requests.get(f"https://news.ycombinator.com/news?p=1")
    statusCode = resp.status_code
    html = resp.content.decode('utf-8')
    out = f"{out}\n{statusCode} {html}"
    i = i + 1
    print(i)

with open("out", "w") as file:
    file.write(out)