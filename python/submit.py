import sys
import glob
import json
import datetime
import requests
from colorama import Fore, Style

cookie_file_path = "../" + glob.glob("cookies.json", root_dir="..")[0]
with open(cookie_file_path, "r") as f:
    cookies = json.load(f)

today_day = datetime.datetime.now().day
today_year = datetime.datetime.now().year

def get_url(day, year):
    assert 2000 <= year <= today_year and 1 <= day <= 25
    return "https://adventofcode.com/{year}/day/{day}/answer".format(year=year, day=day)

def submit(part, answer, day=today_day, year=today_year):
    url = get_url(day, year)
    data = {"answer": answer, "level": part}
    inp = input(f"{Fore.YELLOW}Confirm submitting {answer} to Day {day} part {part} (Y / n): {Style.RESET_ALL}")
    if inp.strip() == "" or inp.lower().startswith("y"):
        resp = requests.post(url, data=data, cookies=cookies)
        text = resp.text.split("<article><p>")[1].split("<a href")[0]
        print(f"Response: {text}")
        return resp
    else:
        print("Aborting.")
        return None

def error(msg=None):
    if msg is not None:
        raise RuntimeError(msg)
    raise RuntimeError(
        f"Invalid inputs. Format should be `{sys.argv[0]} <part> <answer> [day] [year]`"
    )

if __name__ == "__main__":
    args = sys.argv
    if len(args) <= 2:
        error()
    elif args[1] not in "12":
        error(f"Invalid part argument {args[1]}")
    elif len(args) <= 5:
        data = [None, None, today_day, today_year]
        for i, arg in enumerate(args[1:]):
            data[i] = int(arg)
        part, answer, day, year = data
        resp = submit(part, answer, day, year)
        if resp is None:
            print("Cancelled")
        elif resp.status_code != 200:
            print(f"Error: status code is {resp.status_code}")
        else:
            text = resp.text.replace("\n", "").split("<article><p>")[1].split("<a href=\"/")[0]
            print(f"Text: {Fore.YELLOW}{text}{Style.RESET_ALL}")
    else:
        error()

