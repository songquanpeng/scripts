#!/usr/bin/python3
import requests
import os
import sys

filename = "./.star_count"
push_url = ""


def star_counter(username: str, token: "") -> int:
    all_repos_url = "https://api.github.com/users/{}/repos?per_page=100".format(username)
    header = {} if token == "" else {"Authorization": "bearer {}".format(token)}
    res = requests.get(all_repos_url, header)
    repos = res.json()
    count = 0
    for repo in repos:
        count += repo["stargazers_count"]
    return count


def load_count() -> int:
    try:
        with open(filename, 'r') as f:
            count = int(f.read())
    except IOError:
        count = 0
    return count


def save_count(count: int):
    with open(filename, 'w') as f:
        f.write(str(count))


def send_message(msg: str):
    requests.get("{}{}".format(push_url, msg))


def main():
    if len(sys.argv) != 4:
        print("Error! This script requires three arguments: GITHUB_USERNAME GITHUB_TOKEN PUSH_URL")
        return
    username = sys.argv[1]
    token = sys.argv[2]
    global push_url
    push_url = sys.argv[3]
    last_count = load_count()
    current_count = star_counter(username, token)
    if current_count != last_count:
        if current_count > last_count:
            send_message("Star 数量增加了，哈哈！{} --> {}！".format(last_count, current_count))
        else:
            send_message("Star 数量减少了，淦！{} --> {}！".format(last_count, current_count))
        save_count(current_count)


if __name__ == '__main__':
    main()
