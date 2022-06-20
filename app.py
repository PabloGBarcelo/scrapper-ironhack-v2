from ssl import HAS_TLSv1_1
import requests
import time
import json
import pickle
import os
import re
import urllib.request
from urllib.parse import urlparse
from pyquery import PyQuery as pq

extensions = {".jpg", ".png", ".gif"}

# Obtain temario.json calling API
# For example for IRONHACK WDFT alumni course v1:
# https://lms-api.ironhack.tech/v1/courses/course-v1:IRONHACK+WDFT+alumni_course

authorizationToken = "INSERT_BEARER_TOKEN"

headers = {
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(authorizationToken),
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
}

payload = {}

urlLogin = "https://my.ironhack.com"
urlToken = "https://learn.ironhack.com/"
lessonsAllCourses = []

style = """
		<style type='text/css'>
		.container {
		    margin: 0 auto;
		    text-align: center;
		    width: 30%;
		}
		.lesson {
		    padding: 7px;
		    background: #88ceff;
		    border: 2px solid white;
		    border-radius: 10px;
		}
		a.shortcut {
		    color: white;
		    text-transform: uppercase;
		    font-weight: bold;
		    font-family: sans-serif;
		    text-decoration: none;
		}
		h2.header {
		    text-transform: uppercase;
		    width: 75%;
		    margin: 0 auto;
		    color: white;
		}
		</style>
		"""

#################### CREATE FOLDER FILES ##############

def writeFile(url, path, title):
    print(url)
    request = requests.request(
        "GET", url, headers=headers, data=payload).json()
    with open(path, "w", encoding="utf-8") as file:
        while request['result']['level'] != 'content':
            request['result'] = request['result']['children'][0]

        file.write('''<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Ironhack Student Portal</title>
    <link rel="preconnect" href="./libs/cdn.ironhack.com/" />
    <link
      rel="icon"
      href="./libs/cdn.ironhack.com//student-portal/favicon.ico"
    />
    <link
      rel="apple-touch-icon"
      href="./libs/cdn.ironhack.com//student-portal/apple-touch-icon.png"
    />
    <meta name="importmap-type" content="systemjs-importmap" />
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
      crossorigin="anonymous"
    />
    <link
      rel="preload"
      href="https://cdn.jsdelivr.net/npm/single-spa@5.9.3/lib/system/single-spa.min.js"
      as="script"
    />
    <script src="https://cdn.jsdelivr.net/npm/import-map-overrides@1.16.0/dist/import-map-overrides.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/systemjs@6.4.0/dist/system.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/systemjs@6.4.0/dist/extras/amd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/systemjs@6.4.0/dist/extras/named-exports.min.js"></script>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/styles/default.min.css"
    />
    <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/highlight.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/highlightjs-line-numbers.js@2.8.0/dist/highlightjs-line-numbers.min.js"></script>

    <style data-styled="active" data-styled-version="5.2.0"></style>
    <style data-emotion="css" data-s=""></style>
    <style data-emotion="css-global" data-s="">
      .emoji {
        width: 2.4rem;
        height: 2.4rem;
        display: inline-block;
        margin-bottom: -0.25rem;
        background-size: contain;
      }
      body {
        padding: 30px;
      }
    </style>

    <style type="text/css">
      .hljs-ln {
        border-collapse: collapse;
      }
      .hljs-ln td {
        padding: 0;
      }
      .hljs-ln-n:before {
        content: attr(data-line-number);
      }
    </style>
    <style type="text/css">
      .hljs-ln {
        border-collapse: collapse;
      }
      .hljs-ln td {
        padding: 0;
      }
      .hljs-ln-n:before {
        content: attr(data-line-number);
      }
    </style>
  </head>''')
        file.write("<h1>" + title + "</h1>")
        file.write(request['result']['data'].replace(
            '"//codepen.io', '"https://codepen.io'))
        file.write("</html>")
    return


def main():
    urlTemplate = "https://lms-api.ironhack.tech/v1/courses/{0}/units/{1}"

    with open("temario.json", "r") as f:
        allCourse = json.load(f)

    # get course name
    course = allCourse['result']['id']
    # lesson name = allCourse['result']['children'][0]
    # Create new dict better to use
    for moduleWeek in allCourse['result']['children']:
        if moduleWeek['display_name'] != 'Tips & tricks for success':
            print(moduleWeek['display_name'])
            for idm, module in enumerate(moduleWeek['children']):
                for idu, unit in enumerate(module['children']):
                    # for unit in submodule['children']:
                    lesson = unit['id']
                    title = unit['display_name']
                    writeFile(urlTemplate.format(
                        course, lesson), str(idm+1)+"."+str(idu+1) +
                        " "+lesson+".html", title)
                    print(lesson, str(idm+1)+"."+str(idu+1) +
                          " "+lesson+".html", "complete")
                    time.sleep(5)

    # request = requests.request("POST", url, headers=headers, data=payload)


if __name__ == '__main__':
    print("Extractor ")
    main()
