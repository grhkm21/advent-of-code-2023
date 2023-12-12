import sys
import glob
import json
import datetime
import requests

with open("cookies.json", "r") as f:
    cookies = json.load(f)

today_day = datetime.datetime.now().day
today_year = datetime.datetime.now().year

def get_url(day, year=today_year):
    assert 2000 <= year <= today_year and 1 <= day <= 25
    return "https://adventofcode.com/{year}/day/{day}/input".format(year=year, day=day)

args = sys.argv
if len(args) == 1:
    day, year = today_day, today_year
elif len(args) == 2:
    day, year = int(sys.argv[1]), today_year
elif len(args) == 3:
    day, year = int(sys.argv[1]), int(sys.argv[2])
else:
    raise RuntimeError(f"Invalid inputs. Format should be `{sys.argv[0]} [day] [year]`")

fname = f"in_{year}_{day:02}"
if len(glob.glob(f"input/{fname}*")):
    print("[!] File exists!")
    # exit(0)

url = get_url(day, year)
with open(f"input/{fname}", "w") as fout:
    rq = requests.get(url, cookies=cookies)
    if rq.status_code == 404:
        print(f"[404] Haven't unlocked? Error: {rq.text}")
        exit(1)
    fout.write(rq.text)
    print(f"Wrote output to input/{fname}")
