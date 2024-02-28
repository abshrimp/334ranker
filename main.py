import chromedriver_binary
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from decimal import Decimal, ROUND_HALF_UP
import math
import threading
import time
import datetime
import calendar
import json
import copy
import requests
import os
import sys
import traceback

post_url = ""
post_body = {}
post_body_2 = {}
today_result = {}
world_rank = {}
load_res_yet = True
timeline_body = {}
getuser_url = ""
getuser_body = {}
not_url = ""
not_body = {}
search_body = {}
search2_body = {}
idlist = []
driver3 = ""
driver4 = ""
limit = 0
pre_result = {}

start_now = datetime.datetime.now()
start_time = ""
end_time = ""


def get_allresult():
    global today_result, world_rank, load_res_yet
    load_res_yet = False
    for _ in range(5):
        try:
            r = requests.get(os.environ['GAS_URL'])
            r_json = r.json()
            time.sleep(0.5)
            today_result = r_json["result"]
            world_rank = r_json["rank"]
        except Exception as e:
            traceback.print_exc()
            time.sleep(2)
        else:
            break
    if today_result == {} or world_rank == {}:
        load_res_yet = True
    else:
        print("loaded json")

def get_preresult():
    global pre_result
    for _ in range(5):
        try:
            r = requests.get(os.environ['GAS_URL'] + "?p=pre", timeout=120)
            r_json = r.json()
            time.sleep(0.5)
            pre_result = r_json
        except Exception as e:
            traceback.print_exc()
            time.sleep(2)
        else:
            print("loaded pre_result")
            break

def tweet(driver, account, password, tel):
    global post_body, post_url
    for _ in range(5):
        try:
            driver.get('https://twitter.com/Rank334_2/status/1705386885135343879')
            try:
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role=textbox]")))
            except:
                try:
                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[href='/login']")))
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "[href='/login']").click()
                    time.sleep(20)
                    driver.get('https://twitter.com/Rank334_2/status/1705386885135343879')
                    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role=textbox]")))
                except:
                    sys.exit(1)
                    #login_twitter(account, password, tel, driver)
                    break
            time.sleep(1)

            element_box = driver.find_element(By.CSS_SELECTOR, "[role=textbox]")
            element_box.send_keys("ツイート時刻：10:01:32.629")
            time.sleep(2) 
            
            driver.find_element(By.CSS_SELECTOR, "[data-testid=tweetButtonInline]").click()
            time.sleep(20)


            for _ in range(5):
                for request in driver.requests:
                    if request.response:
                        if "CreateTweet" in request.url:
                            post_url = request.url
                            post_body2 = json.loads(request.body)
                            time.sleep(0.5)
                            if "variables" in post_body2:
                                post_body = post_body2
                                print("set post_body")

                                try:
                                    restid = json.loads(decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity')))["data"]["create_tweet"]["tweet_results"]["result"]["rest_id"]
                                    driver.execute_script("""
var restid = arguments[0];
var data = {"variables": {"tweet_id": restid, "dark_request": false}};

var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
})

function get_queryid(name, defaultId) {
    try {
        let queryids = webpackChunk_twitter_responsive_web;
        for (let i = 0; i < queryids.length; i++) {
            for (let key in queryids[i][1]) {
                try {
                    if (queryids[i][1][key].length === 1) {
                        let tmp = {};
                        queryids[i][1][key](tmp);
                        if (tmp.exports.operationName === name) return tmp.exports.queryId;
                    }
                } catch { }
            }
        }
        return defaultId;
    } catch {
        return defaultId;
    }
}

var xhr = new XMLHttpRequest();
xhr.open('POST', 'https://twitter.com/i/api/graphql/' + get_queryid('DeleteTweet', 'VaenaVgh5q5ih7kvyVjgtg') + '/DeleteTweet');
xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
xhr.setRequestHeader('x-csrf-token', token);
xhr.setRequestHeader('x-twitter-active-user', 'yes');
xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
xhr.setRequestHeader('x-twitter-client-language', 'ja');
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.withCredentials = true;
xhr.send(JSON.stringify(data));

""", restid)
                                except Exception as e:
                                    traceback.print_exc()
                                    time.sleep(2)
                                break
                if post_body != {}:
                    break
                time.sleep(0.5)
                    

            time.sleep(3)

        except Exception as e:
            traceback.print_exc()
            time.sleep(2)
        else:
            break
	
    

def login_twitter(account, password, tel, driver):
    global timeline_body, getuser_body, getuser_url, not_url, not_body, search_body
    for _ in range(5):
        try:
            driver.get('https://twitter.com/i/flow/login')
            driver.maximize_window()
            element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "text")))
            time.sleep(1)
            
            act = ActionChains(driver)
            
            element_account = driver.find_element(By.TAG_NAME, "input")
            element_account.send_keys("")
            for i in range(len(account)):
                time.sleep(1)
                act.send_keys(account[i])
                act.perform()
            time.sleep(2)
            element_account.send_keys(Keys.ENTER)
            time.sleep(20)

            element_pass = driver.find_elements(By.TAG_NAME, "input")[1]
            for i in range(len(password)):
                time.sleep(1)
                act.send_keys(password[i])
                act.perform()
            time.sleep(2)
            element_pass.send_keys(Keys.ENTER)
            time.sleep(20)

            element_tel = driver.find_elements(By.NAME, "text")
            if len(element_tel) > 0:
                element_tel[0].send_keys(tel)
                time.sleep(2) 
                element_tel[0].send_keys(Keys.ENTER)
                time.sleep(20)

            driver.get('https://twitter.com/home')
            time.sleep(20)
            
            for _ in range(5):
                for request in driver.requests:
                    if request.response:
                        if "Timeline" in request.url and "graphql" in request.url:
                            if request.body != b'':
                                timeline_body2 = json.loads(request.body)
                                time.sleep(0.5)
                                if "variables" in timeline_body2:
                                    timeline_body = timeline_body2
                                    print("set timeline_body")
                                    break
                            else:
                                timeline_body2 = request.params
                                time.sleep(0.5)
                                if "variables" in timeline_body2:
                                    timeline_body = timeline_body2
                                    for key in timeline_body:
                                    	timeline_body[key] = json.loads(timeline_body[key])
                                    print("set timeline_body")
                                    break
                if timeline_body != {}:
                    break
                time.sleep(0.5)
		
            driver.get('https://twitter.com/intent/user?user_id=1')
            time.sleep(20)
            
            for _ in range(5):
                for request in driver.requests:
                    if request.response:
                        if "UserByRestId" in request.url and "graphql" in request.url:
                            getuser_url = request.url
                            if request.body != b'':
                                getuser_body2 = json.loads(request.body)
                                time.sleep(0.5)
                                if "variables" in getuser_body2:
                                    getuser_body = getuser_body2
                                    print("set getuser_body")
                                    break
                            else:
                                getuser_body2 = request.params
                                time.sleep(0.5)
                                if "variables" in getuser_body2:
                                    getuser_body = getuser_body2
                                    for key in getuser_body:
                                    	getuser_body[key] = json.loads(getuser_body[key])
                                    print("set getuser_body")
                                    break
                if getuser_body != {}:
                    break
                time.sleep(0.5)

            driver.get('https://twitter.com/notifications/mentions')
            time.sleep(20)
            
            for _ in range(5):
                for request in driver.requests:
                    if request.response:
                        if "mentions.json" in request.url:
                            not_url = request.url
                            if request.body != b'':
                                not_body = json.loads(request.body)
                            else:
                                not_body = request.params
                            print("set not_body")
                            break
                if not_body != {}:
                    break
                time.sleep(0.5)
            
            driver.get('https://twitter.com/search?q=334&src=typed_query&f=live')
            time.sleep(20)
            
            for _ in range(5):
                for request in driver.requests:
                    if request.response:
                        if "SearchTimeline" in request.url and "graphql" in request.url:
                            if request.body != b'':
                                search_body2 = json.loads(request.body)
                                time.sleep(0.5)
                                if "variables" in search_body2:
                                    search_body = search_body2
                                    print("set search_body")
                                    break
                            else:
                                search_body2 = request.params
                                time.sleep(0.5)
                                if "variables" in search_body2:
                                    search_body = search_body2
                                    for key in search_body:
                                    	search_body[key] = json.loads(search_body[key])
                                    print("set search_body")
                                    break
                if search_body != {}:
                    break
                time.sleep(0.5)

            
            tweet(driver, account, password, tel)
        
        except Exception as e:
            traceback.print_exc()
            time.sleep(2)
        else:
            break



def login_twitter2(account, password, tel, driver):
    for _ in range(5):
        try:
            driver3.get('https://twitter.com/i/flow/login')
            driver3.maximize_window()
            element = WebDriverWait(driver3, 60).until(EC.presence_of_element_located((By.NAME, "text")))
            time.sleep(1)
            
            act = ActionChains(driver3)
            
            element_account = driver3.find_element(By.TAG_NAME, "input")
            element_account.send_keys("")
            for i in range(len(account)):
                time.sleep(1)
                act.send_keys(account[i])
                act.perform()
            time.sleep(2)
            element_account.send_keys(Keys.ENTER)
            time.sleep(20)

            element_pass = driver3.find_elements(By.TAG_NAME, "input")[1]
            for i in range(len(password)):
                time.sleep(1)
                act.send_keys(password[i])
                act.perform()
            time.sleep(2)
            element_pass.send_keys(Keys.ENTER)
            time.sleep(20)

            element_tel = driver3.find_elements(By.NAME, "text")
            if len(element_tel) > 0:
                element_tel[0].send_keys(tel)
                time.sleep(2) 
                element_tel[0].send_keys(Keys.ENTER)
                time.sleep(20)
        
        except Exception as e:
            traceback.print_exc()
            time.sleep(2)
        else:
            break


    global post_body_2, search2_body
    for _ in range(5):
        try:
            driver3.get('https://twitter.com/search?q=@rank334&src=typed_query&f=live')
            time.sleep(20)
            
            for _ in range(5):
                for request in driver3.requests:
                    if request.response:
                        if "SearchTimeline" in request.url and "graphql" in request.url:
                            if request.body != b'':
                                search2_body2 = json.loads(request.body)
                                time.sleep(0.5)
                                if "variables" in search2_body2:
                                    search2_body = search2_body2
                                    print("set search2_body")
                                    break
                            else:
                                search2_body2 = request.params
                                time.sleep(0.5)
                                if "variables" in search2_body2:
                                    search2_body = search2_body2
                                    for key in search2_body:
                                    	search2_body[key] = json.loads(search2_body[key])
                                    print("set search2_body")
                                    break
                if search2_body != {}:
                    break
                time.sleep(0.5)

            time.sleep(3)
            
            
            driver3.get('https://twitter.com/Rank334_2/status/1705386885135343879')
            try:
                element = WebDriverWait(driver3, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role=textbox]")))
            except:
                try:
                    element = WebDriverWait(driver3, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[href='/login']")))
                    time.sleep(1)
                    driver3.find_element(By.CSS_SELECTOR, "[href='/login']").click()
                    time.sleep(2)
                    driver3.get('https://twitter.com/Rank334_2/status/1705386885135343879')
                    element = WebDriverWait(driver3, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role=textbox]")))
                except:
                    #sys.exit(1)
                    pass
                    break
            time.sleep(1)

            element_box = driver3.find_element(By.CSS_SELECTOR, "[role=textbox]")
            element_box.send_keys("ツイート時刻：10:01:32.629")
            time.sleep(2) 
            
            driver3.find_element(By.CSS_SELECTOR, "[data-testid=tweetButtonInline]").click()
            time.sleep(2)


            for _ in range(5):
                for request in driver3.requests:
                    if request.response:
                        if "CreateTweet" in request.url:
                            post_body2 = json.loads(request.body)
                            time.sleep(0.5)
                            if "variables" in post_body2:
                                post_body_2 = post_body2
                                print("set post_body_2")
                                
                                try:
                                    restid = json.loads(decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity')))["data"]["create_tweet"]["tweet_results"]["result"]["rest_id"]
                                    driver3.execute_script("""
var restid = arguments[0];
var data = {"variables": {"tweet_id": restid, "dark_request": false}};

var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
})

function get_queryid(name, defaultId) {
    try {
        let queryids = webpackChunk_twitter_responsive_web;
        for (let i = 0; i < queryids.length; i++) {
            for (let key in queryids[i][1]) {
                try {
                    if (queryids[i][1][key].length === 1) {
                        let tmp = {};
                        queryids[i][1][key](tmp);
                        if (tmp.exports.operationName === name) return tmp.exports.queryId;
                    }
                } catch { }
            }
        }
        return defaultId;
    } catch {
        return defaultId;
    }
}

var xhr = new XMLHttpRequest();
xhr.open('POST', 'https://twitter.com/i/api/graphql/' + get_queryid('DeleteTweet', 'VaenaVgh5q5ih7kvyVjgtg') + '/DeleteTweet');
xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
xhr.setRequestHeader('x-csrf-token', token);
xhr.setRequestHeader('x-twitter-active-user', 'yes');
xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
xhr.setRequestHeader('x-twitter-client-language', 'ja');
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.withCredentials = true;
xhr.send(JSON.stringify(data));

""", restid)
                                except Exception as e:
                                    traceback.print_exc()
                                    time.sleep(2)
                                break
                if post_body_2 != {}:
                    break
                time.sleep(0.5)
                    
            time.sleep(3)
		
        except Exception as e:
            traceback.print_exc()
            time.sleep(2)
        else:
            break

    
    threading.Thread(target=check_unsend, args=(end_time, driver,)).start()



def reply(req, driver):
    print("reply start", datetime.datetime.now())
    driver.execute_script("""
var url = arguments[0];
var data = JSON.stringify(arguments[1]);
    
var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
})

var xhr = new XMLHttpRequest();
xhr.open('POST', url);
xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
xhr.setRequestHeader('x-csrf-token', token);
xhr.setRequestHeader('x-twitter-active-user', 'yes');
xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
xhr.setRequestHeader('x-twitter-client-language', 'ja');
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.withCredentials = true;

xhr.onload = function () {
    let res = JSON.parse(xhr.responseText);
    if ("errors" in res) window.unsend.push(data);
}

xhr.send(data);

""", post_url, req)
    


def reply2(reqs):

    for req in reqs:
        print("reply2 start", datetime.datetime.now())
        req = json.loads(req)
        req["features"] = post_body_2["features"]
        driver3.execute_script("""
var url = arguments[0];
    
var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
})

var xhr = new XMLHttpRequest();
xhr.open('POST', url);
xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
xhr.setRequestHeader('x-csrf-token', token);
xhr.setRequestHeader('x-twitter-active-user', 'yes');
xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
xhr.setRequestHeader('x-twitter-client-language', 'ja');
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.withCredentials = true;

var data = JSON.stringify(arguments[1]);
xhr.send(data);

""", post_url, req)



def get_kyui(pt):
    if pt < 500:
        rank = "E"
    elif pt < 1000:
        rank = "E+"
    elif pt < 1500:
        rank = "D"
    elif pt < 2000:
        rank = "D+"
    elif pt < 2500:
        rank = "C"
    elif pt < 3000:
        rank = "C+"
    elif pt < 3500:
        rank = "B"
    elif pt < 4000:
        rank = "B+"
    elif pt < 4500:
        rank = "A"
    elif pt < 5000:
        rank = "A+"
    elif pt < 5500:
        rank = "S1"
    elif pt < 6000:
        rank = "S2"
    elif pt < 6500:
        rank = "S3"
    elif pt < 7000:
        rank = "S4"
    elif pt < 7500:
        rank = "S5"
    elif pt < 8000:
        rank = "S6"
    elif pt < 8500:
        rank = "S7"
    elif pt < 9000:
        rank = "S8"
    elif pt < 9500:
        rank = "S9"
    else:
        rank = "RoR"
	
    return rank



def get_rank(key, name):
    if today_result == {}:
        return True
    if key in world_rank:
        if world_rank[key][4] != world_rank[key][6]:
            rep_text2 = "\n参考記録: " + world_rank[key][6]
        else:
            rep_text2 = ""

        pt = float(world_rank[key][2])
        rank = get_kyui(pt)
        pt2 = float(world_rank[key][4])
        rank2 = get_kyui(pt2)
                                                    
        return name + "\n\n級位: " + rank + "\n⠀最高pt: " + world_rank[key][2] + "\n⠀歴代: " + str(world_rank[key][3]) + " / " + world_rank["累計"][0] + "\n⠀現在pt: " + world_rank[key][4] + " (" + rank2 + "帯)\n⠀世界ランク: " + str(world_rank[key][5]) + " / " + world_rank["現在"][0] + rep_text2 +\
                        "\n1s以内出場数: " + str(world_rank[key][7]) + "\n自己ベスト: " + world_rank[key][0] + " (" + str(world_rank[key][1]) + "回)\n戦績: 🥇×" + str(world_rank[key][8]) + " 🥈×" + str(world_rank[key][9]) + " 🥉×" + str(world_rank[key][10]) + " 📋×" + str(world_rank[key][11])
    else:
        return name + "\n\n最高pt: -\n歴代: - / " + world_rank["累計"][0] + "\n現在pt: -\n世界ランク: - / " + world_rank["現在"][0] + "\n1s以内出場数: 0\n自己ベスト: -\n戦績: 🥇×0 🥈×0 🥉×0 📋×0"


def has_rank(key, name, item):
    text = item["status"]["data"]["full_text"].lower()
    mentions = item["status"]["data"]["entities"]["user_mentions"]
    for user in mentions:
        text = text.replace("@" + user["screen_name"].lower(), "")
    if "ランク" in text or "ﾗﾝｸ" in text or "らんく" in text or "rank" in text or "ランキング" in text or "ﾗﾝｷﾝｸﾞ" in text:
        return get_rank(key, name)
    else:
        return False



def get_result(key, name):
    previous = datetime.datetime.now() - datetime.timedelta(hours=3, minutes=33)
    if today_result == {}:
        return "ランキングは準備中です\nしばらくお待ちください"
    if key in today_result:
        return name + "\n\n" + previous.date().strftime('%Y/%m/%d') + "の334結果\nresult: +" + today_result[key][2] + " [sec]\nrank: " + today_result[key][0] + " / " + today_result["参加者数"][0]
    else:
        return name + "\n\n" + previous.date().strftime('%Y/%m/%d') + "の334結果\nresult: DQ\nrank: DQ / " + today_result["参加者数"][0]



def TweetIdTime(id):
    epoch = ((id >> 22) + 1288834974657) / 1000.0
    d = datetime.datetime.fromtimestamp(epoch)
    return d


def TimeToStr(d):
    stringTime = ""
    stringTime += '{0:02d}'.format(d.hour)
    stringTime += ':'
    stringTime += '{0:02d}'.format(d.minute)
    stringTime += ':'
    stringTime += '{0:02d}'.format(d.second)
    stringTime += '.'
    stringTime += '{0:03d}'.format(int(d.microsecond / 1000))
    return stringTime


def get_followed(id, driver):
    driver.execute_script("""
if (window.followed === undefined) window.followed = {};
var id = arguments[2];
window.followed[id] = "";
var data = arguments[0];
var url = arguments[1].split("?")[0];
var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
})
data.variables.userId = id;
let param = "?" + Object.entries(data).map((e) => { return `${e[0].replaceAll("%22", "")}=${encodeURIComponent(JSON.stringify(e[1]))}` }).join("&");
var xhr = new XMLHttpRequest();
xhr.open('GET', url + param);
xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
xhr.setRequestHeader('x-csrf-token', token);
xhr.setRequestHeader('x-twitter-active-user', 'yes');
xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
xhr.setRequestHeader('x-twitter-client-language', 'ja');
xhr.withCredentials = true;
xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
        if (xhr.status == 200) {
            try {
                out = JSON.parse(xhr.responseText);
                if ("followed_by" in out.data.user.result.legacy) {
                    if (out.data.user.result.legacy.followed_by) window.followed[id] = 1;
                    else window.followed[id] = 2;
                } else window.followed[id] = 2;
            } catch (e) {
                console.error(e);
                window.followed[id] = 3;
            }
        } else window.followed[id] = 3;
    }
}
xhr.send();
    """, getuser_body, getuser_url, id)
    while True:
        time.sleep(0.01)
        res = driver.execute_script("return window.followed['" + id + "']")
        if res != "":
            driver.execute_script("window.followed['" + id + "'] = ''")
            return res


def following(id, driver):
    driver.execute_script("""
if (window.following === undefined) window.following = {};
var id = arguments[0];
window.following[id] = "";
var url = "https://api.twitter.com/1.1/friendships/create_all.json?user_id=" + id;
    
var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
})

var xhr = new XMLHttpRequest();
xhr.open('POST', url);
xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
xhr.setRequestHeader('x-csrf-token', token);
xhr.setRequestHeader('x-twitter-active-user', 'yes');
xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
xhr.setRequestHeader('x-twitter-client-language', 'ja');
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.withCredentials = true;
xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
        if (xhr.status == 200) window.following[id] = true;
        else window.followed[id] = false;
    }
}
xhr.send();
""", id)
    while True:
        time.sleep(0.01)
        res = driver.execute_script("return window.following['" + id + "']")
        if res != "":
            driver.execute_script("window.following['" + id + "'] = ''")
            return res


def receive(dict, driver):
    global idlist, limit
    ranker_id = "1558892196069134337"
    ranker_id_2 = "1556292536477843456"

    for item in dict:
        
        if item["status"]["data"]["user"]["id_str"] != ranker_id and item["status"]["data"]["user"]["id_str"] != ranker_id_2:
            rep_text = False
            follow_flag = False
            if "in_reply_to_status_id_str" not in item["status"]["data"] or item["status"]["data"]["in_reply_to_status_id_str"] == None:
                user_id = item["status"]["data"]["user"]["id_str"]
                text = item["status"]["data"]["full_text"].lower()
                mentions = item["status"]["data"]["entities"]["user_mentions"]
                for user in mentions:
                    text = text.replace("@" + user["screen_name"].lower(), "")
                user_name = item["status"]["data"]["user"]["name"]
                if user_name == "":
                    user_name = "@" + item["status"]["data"]["user"]["screen_name"]
                if "ふぉろー" in text or "フォロー" in text or "follow" in text or "ふぉろば" in text or "フォロバ" in text:
                    if item["status"]["data"]["id_str"] not in idlist:
                        idlist.append(item["status"]["data"]["id_str"])
                        follow_flag = True
                        if item["status"]["data"]["user"]["following"] == True:
                            rep_text = "既にフォローしています"
                        else:
                            print("フォロー : " + user_name + "  @" + item["status"]["data"]["user"]["screen_name"])
                            followed = get_followed(user_id, driver)
                            if followed == 1:
                                follow = following(user_id, driver)
                                if follow == True:
                                    rep_text = "フォローしました"
                                else:
                                   rep_text = "エラーが発生しました🙇\n時間をおいてもう一度お試しください"
                            elif followed == 2:
                                rep_text = "334Rankerをフォローしてからお試しください"
                            else:
                                rep_text = "エラーが発生しました🙇\n時間をおいてもう一度お試しください"
                else:
                    rep_text = has_rank(user_id, user_name, item)
                    if rep_text == False or rep_text == True:
                        rep_text = get_result(user_id, user_name)
            else:
                if item["status"]["data"]["in_reply_to_user_id_str"] == ranker_id or item["status"]["data"]["in_reply_to_user_id_str"] == ranker_id_2:
                    user_id = item["status"]["data"]["user"]["id_str"]
                    user_name = item["status"]["data"]["user"]["name"]
                    if user_name == "":
                        user_name = "@" + item["status"]["data"]["user"]["screen_name"]
                    text = item["status"]["data"]["full_text"].lower()
                    if "ふぉろー" in text or "フォロー" in text or "follow" in text or "ふぉろば" in text or "フォロバ" in text:
                        if item["status"]["data"]["id_str"] not in idlist:
                            idlist.append(item["status"]["data"]["id_str"])
                            follow_flag = True
                            if item["status"]["data"]["user"]["following"] == True:
                                rep_text = "既にフォローしています"
                            else:
                                print("フォロー : " + user_name + "  @" + item["status"]["data"]["user"]["screen_name"])
                                followed = get_followed(user_id, driver)
                                if followed == 1:
                                    follow = following(user_id, driver)
                                    if follow == True:
                                        rep_text = "フォローしました"
                                    else:
                                        rep_text = "エラーが発生しました🙇\n時間をおいてもう一度お試しください"
                                elif followed == 2:
                                    rep_text = "334Rankerをフォローしてからお試しください"
                                else:
                                    rep_text = "エラーが発生しました🙇\n時間をおいてもう一度お試しください"
                    else:
                        rep_text = has_rank(user_id, user_name, item)
                        if rep_text == True:
                            rep_text = "ランキングは準備中です\nしばらくお待ちください"
                else:
                    user_id = item["status"]["data"]["in_reply_to_user_id_str"]
                    user_name = ""
                    text_range = item["status"]["data"]["display_text_range"]
                    mentions = item["status"]["data"]["entities"]["user_mentions"]
                    flag = False 
                    for user in mentions:
                        if (user["id_str"] == ranker_id or user["id_str"] == ranker_id_2) and text_range[0] <= user["indices"][0] and user["indices"][1] <= text_range[1]:
                            flag = True
                        if user["id_str"] == user_id:
                            user_name = user["name"]
                    if flag:
                        if user_name == "":
                            if user_id == item["status"]["data"]["user"]["id_str"]:
                                user_name = item["status"]["data"]["user"]["name"]
                            if user_name == "":
                                user_name = "@" + item["status"]["data"]["in_reply_to_screen_name"]
                        rep_text = has_rank(user_id, user_name, item)
                        if rep_text == True:
                            rep_text = "ランキングは準備中です\nしばらくお待ちください"
                        elif rep_text == False:
                            orig_time = TweetIdTime(int(item["status"]["data"]["in_reply_to_status_id_str"]))
                            rep_text = "ツイート時刻：" + TimeToStr(orig_time)

            if rep_text != False:
                if item["status"]["data"]["id_str"] not in idlist or follow_flag == True:
                    if follow_flag == False:
                        idlist.append(item["status"]["data"]["id_str"])
                    print(item["status"]["data"]["user"]["name"])
                    req = copy.deepcopy(post_body)
                    req["variables"]["reply"]["in_reply_to_tweet_id"] = item["status"]["data"]["id_str"]
                    req["variables"]["tweet_text"] = rep_text
                    limit += 1
                    if limit >= 290 and datetime.datetime.now() < datetime.datetime(start_now.year, start_now.month, start_now.day, 3, 45, 0):
                        threading.Thread(target=reply2, args=([json.dumps(req)],)).start()
                    else:
                        threading.Thread(target=reply, args=(req, driver,)).start()



def interval(since, until, end, index, driver):
    while True:
        if until < datetime.datetime.now():
            if (end - until).total_seconds() <= 6:
                add = (end - until).total_seconds()
            elif datetime.datetime(until.year, until.month, until.day, 3, 28, 0) < datetime.datetime.now() < datetime.datetime(until.year, until.month, until.day, 3, 34, 2):
                add = 6
            elif index % 12 == 0:
                add = 6
            else:
                add = 5
            if until < end:
                threading.Thread(target=interval, args=(until, until + datetime.timedelta(seconds = add), end, index + 1, driver,)).start()
            since2 = since - datetime.timedelta(seconds = 1)
            res = driver.execute_async_script("""
var url = 'https://api.twitter.com/1.1/search/tweets.json?q=@rank334 since:""" + since2.strftime('%Y-%m-%d_%H:%M:%S_JST') + """ until:""" + until.strftime('%Y-%m-%d_%H:%M:%S_JST') + """ -filter:retweets -filter:quote -from:rank334 -from:rank334_2&count=100&result_type=recent&tweet_mode=extended';

var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
})

var callback = arguments[arguments.length - 1];
/*
var xhr = new XMLHttpRequest();
xhr.open('GET', url);
xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
xhr.setRequestHeader('x-csrf-token', token);
xhr.setRequestHeader('x-twitter-active-user', 'yes');
xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
xhr.setRequestHeader('x-twitter-client-language', 'ja');
xhr.withCredentials = true;

xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
        if (xhr.status == 200) {
            try {
                out = JSON.parse(xhr.responseText);
                out2 = [];
                for(var i = 0; i < out.statuses.length; i++) {
                    out2.push({"status": {"data": out.statuses[i]}})
                }
                callback(out2);
            } catch {
                callback([]);
            }
        }
        else callback([]);
    }
}

xhr.send();*/

callback([]);
            """)
            if res != []:
                receive(res, driver)
            if datetime.datetime(start_now.year, start_now.month, start_now.day, 3, 38, 0) < until and load_res_yet:
                get_allresult()
            break
        time.sleep(0.01)


def print_log(driver):
    logs = driver.get_log('browser')
    for log in logs:
        if "message" in log and "timestamp" in log:
            if "Please make sure it has an appropriate" not in log["message"] and "keyregistry" not in log["message"] and "live_pipeline" not in log["message"]:
                print(datetime.datetime.fromtimestamp(log['timestamp'] / 1000))
                print(log)
                print()


def interval2(since, end, driver):
    while True:
        if since < datetime.datetime.now():
            driver.execute_script("""
var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
});
function setheader(xhr) {
    xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
    xhr.setRequestHeader('x-csrf-token', token);
    xhr.setRequestHeader('x-twitter-active-user', 'yes');
    xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
    xhr.setRequestHeader('x-twitter-client-language', 'ja');
    xhr.withCredentials = true;
}
window.adaptive = [];
let from = new Date(arguments[0] * 1000);
let until = new Date(arguments[1] * 1000);
let refresh = "";
let param = "?" + Object.entries(arguments[3]).map((e) => { return `${e[0]}=${encodeURIComponent(JSON.stringify(e[1]))}` }).join("&").replaceAll("%22", "");

let not = setInterval(function (arguments) {
    if (until < new Date()) clearInterval(not);
    get_notifications("&cursor=" + refresh, arguments);
}, 8000, arguments);

function get_notifications(cursor, arguments) {
    try {
        let xhr = new XMLHttpRequest();
        let url = arguments[2].split("?")[0] + param + cursor;
        xhr.open('GET', url);
        get_tweets(cursor, xhr);
    } catch { }
}

function get_tweets(cursor, xhr) {
    setheader(xhr);
    xhr.send();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let res = JSON.parse(xhr.responseText);
            let tweets = res.globalObjects.tweets;
            let users = res.globalObjects.users;
            let timelines = res.timeline.instructions;
            let timeline = [];
            for (let j = 0; j < timelines.length; j++) {
                if ("addEntries" in timelines[j]) timeline = timeline.concat(timelines[j].addEntries.entries);
                else if ("replaceEntry" in timelines[j]) timeline.push(timelines[j].replaceEntry.entry);
            }
            for (let i = 0; i < timeline.length; i++) {
                try {
                    if (!timeline[i].entryId.includes("cursor")) {
                        let id = timeline[i].content.item.content.tweet.id;
                        let tweet = tweets[id];
                        if (!tweet.full_text.toLowerCase().includes("@rank334") && !tweet.full_text.toLowerCase().includes("@rank334_2")) continue;
                        if (new Date(tweet.created_at) < from) continue;
                        if (until <= new Date(tweet.created_at)) {
                            clearInterval(not);
                            continue;
                        }
                        tweet["user"] = users[tweet.user_id_str];
                        let status = {
                            "status": {
                                "data": tweet
                            }
                        }
                        window.adaptive.push(status);
                    }
                    else if (timeline[i].entryId.includes("top")) refresh = timeline[i].content.operation.cursor.value;
                } catch { }
            }
        }
    }
}
""", int(since.timestamp()), int(end.timestamp()), not_url, not_body)
            while True:
                time.sleep(0.01)
                out = driver.execute_script("""
let adaptive = JSON.parse(JSON.stringify(window.adaptive));
window.adaptive = [];
return adaptive;
""")
                if out != []:
                    threading.Thread(target=receive, args=(out, driver,)).start()
                else:
                    if end + datetime.timedelta(seconds=20) < datetime.datetime.now():
                        print_log(driver)
                        break
            break
        time.sleep(0.01)



def interval3(until, index, driver):
    if index == 0:
        driver3.execute_script("window.search = {};")
    while True:
        if until < datetime.datetime.now():
            if until <= datetime.datetime(start_now.year, start_now.month, start_now.day, 3, 34, 48):
                threading.Thread(target=interval3, args=(until + datetime.timedelta(seconds = 1), index + 1, driver,)).start()
            since = until - datetime.timedelta(seconds = 2)
            driver3.execute_script("""
window.search[""" + str(index) + """] = "";

var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
})

function callback(out) {
    window.search[""" + str(index) + """] = out;
}

function get_queryid(name, defaultId) {
    try {
        let queryids = webpackChunk_twitter_responsive_web;
        for (let i = 0; i < queryids.length; i++) {
            for (let key in queryids[i][1]) {
                try {
                    if (queryids[i][1][key].length === 1) {
                        let tmp = {};
                        queryids[i][1][key](tmp);
                        if (tmp.exports.operationName === name) return tmp.exports.queryId;
                    }
                } catch { }
            }
        }
        return defaultId;
    } catch {
        return defaultId;
    }
}

var data2 = arguments[0];
data2.variables["cursor"] = "";
data2.variables["rawQuery"] = "@rank334 -filter:retweets -from:rank334 -from:rank334_2 since:""" + since.strftime('%Y-%m-%d_%H:%M:%S_JST') + """ until:""" + until.strftime('%Y-%m-%d_%H:%M:%S_JST') + """"
let queryid2 = get_queryid("SearchTimeline", "KUnA_SzQ4DMxcwWuYZh9qg");

function setheader(xhr) {
    xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
    xhr.setRequestHeader('x-csrf-token', token);
    xhr.setRequestHeader('x-twitter-active-user', 'yes');
    xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
    xhr.setRequestHeader('x-twitter-client-language', 'ja');
    xhr.withCredentials = true;
}

let out4 = [];
     
        let param = "?" + Object.entries(data2).map((e) => {
            return `${e[0].replaceAll("%22", "")}=${encodeURIComponent(JSON.stringify(e[1]))}`
        }).join("&")
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'https://api.twitter.com/graphql/' + queryid2 + '/SearchTimeline' + param);
        setheader(xhr);
        xhr.setRequestHeader('content-type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    try {
                        let instructions = JSON.parse(xhr.responseText).data.search_by_raw_query.search_timeline.timeline.instructions;
                        for (let j = 0; j < instructions.length; j++) {
                            if ("entries" in instructions[j]) var entries = instructions[j].entries;
                            else if ("entry" in instructions[j]) var entries = [instructions[j].entry];
                            else continue;
                            for (let i = 0; i < entries.length; i++) {
                                if (!entries[i].entryId.includes("promoted") && !entries[i].entryId.includes("cursor")) {
                                    try {
                                        var res = entries[i].content.itemContent.tweet_results.result;
                                        if ("tweet" in res) res = res.tweet;
                                        let legacy = res.legacy;
                                        legacy["text"] = legacy.full_text;
                                        if (!legacy.text.toLowerCase().includes("@rank334") && !legacy.text.toLowerCase().includes("@rank334_2")) continue;
                                        legacy["source"] = res.source;
                                        legacy["user"] = res.core.user_results.result.legacy;
                                        legacy.user["id_str"] = legacy.user_id_str;
                                        out4.push({
                                            "status": {
                                                "data": legacy
                                            }
                                        });
                                        continue;
                                    } catch (e) {
                                        console.error(e);
                                    }
                                }
                            }
                        }
                        callback(out4);
                    } catch (e) {
                        console.error(e);
                        callback(out4);
                    }
                } else callback(out4);
            }
        }
        xhr.send();
            """, search2_body)
            while True:
                time.sleep(0.01)
                out = driver3.execute_script("return window.search[" + str(index) + "];")
                if out != "":
                    if out != []:
                        receive(out, driver)
                    break
            break
        time.sleep(0.01)



def check_unsend(end, driver):

    driver.execute_script("window.unsend = []")
    while True:
        time.sleep(0.01)
        out = driver.execute_script("""
let unsend = JSON.parse(JSON.stringify(window.unsend));
window.unsend = [];
return unsend;
""")
        if out != []:
            threading.Thread(target=reply2, args=(out,)).start()
        else:
            if end + datetime.timedelta(seconds=20) < datetime.datetime.now():
                break




def retweet(id, driver):
    
    try:
        data = {
            "variables": {
                "tweet_id": id,
                "dark_request": False
            },
            "queryId": ""
        }
    
        driver.execute_script("""
function get_queryid(name, defaultId) {
    try {
        let queryids = webpackChunk_twitter_responsive_web;
        for (let i = 0; i < queryids.length; i++) {
            for (let key in queryids[i][1]) {
                try {
                    if (queryids[i][1][key].length === 1) {
                        let tmp = {};
                        queryids[i][1][key](tmp);
                        if (tmp.exports.operationName === name) return tmp.exports.queryId;
                    }
                } catch {}
            }
        }
        return defaultId;
    } catch {
        return defaultId;
    }
}

var queryid = get_queryid('CreateRetweet', 'ojPdsZsimiJrUGLR1sjUtA');
var url = 'https://api.twitter.com/graphql/' + queryid + '/CreateRetweet';

var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
})

var data = arguments[0];
data.queryId = queryid;

var xhr = new XMLHttpRequest();
xhr.open('POST', url);
xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
xhr.setRequestHeader('x-csrf-token', token);
xhr.setRequestHeader('x-twitter-active-user', 'yes');
xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
xhr.setRequestHeader('x-twitter-client-language', 'ja');
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.withCredentials = true;
xhr.send(JSON.stringify(data));

""", data)
    except Exception as e:
        print("error retweet")



def postrank(bin, driver, text):

    driver.execute_script("""
window.data2 = "";
var bin = atob(arguments[0]);
var buffer = new Uint8Array(bin.length);
for (let i = 0; i < bin.length; i++) {
    buffer[i] = bin.charCodeAt(i);
}
var blob = new Blob([buffer.buffer], { type: "image/png" });
var data = new FormData();
data.append("media", blob, "blob");

var url = 'https://upload.twitter.com/i/media/upload.json?command=INIT&total_bytes=' + blob.size + '&media_type=image%2Fjpeg&media_category=tweet_image';

var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
})

var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function () {
    if (this.readyState == 4) {
        append(JSON.parse(this.responseText)["media_id_string"]);
    }
}
xhr.open('POST', url);
xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
xhr.setRequestHeader('x-csrf-token', token);
xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
xhr.withCredentials = true;
xhr.send();

function append(id) {
    let url = 'https://upload.twitter.com/i/media/upload.json?command=APPEND&media_id=' + id + '&segment_index=0';

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState == 4) {
            final(id);
        }
    }
    xhr.open('POST', url);
    xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
    xhr.setRequestHeader('x-csrf-token', token);
    xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
    xhr.withCredentials = true;
    xhr.send(data);
}

function final(id) {
    let url = 'https://upload.twitter.com/i/media/upload.json?command=FINALIZE&media_id=' + id;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState == 4) {
            window.data2 = id;
        }
    }
    xhr.open('POST', url);
    xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
    xhr.setRequestHeader('x-csrf-token', token);
    xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
    xhr.withCredentials = true;
    xhr.send();
}
    """, bin)
    while True:
        time.sleep(0.01)
        res = driver.execute_script("return window.data2")
        if res != "":
            req = copy.deepcopy(post_body)
            req["variables"]["media"]["media_entities"] = [{"media_id": res, "tagged_users": []}]
            req["variables"]["tweet_text"] = text
            del req["variables"]['reply']
            print("post rank :")
            threading.Thread(target=reply, args=(req, driver,)).start()
            break



def browser2(driver, driver2):
    for _ in range(5):
        try:
            driver.get(os.environ['HTML_URL2'])
            wait = WebDriverWait(driver, 60).until(EC.alert_is_present())
            Alert(driver).accept()
            data = driver.execute_script('return window.data')
            driver2.execute_script("""
window.data = "";
var data = arguments[0];
var data2 = arguments[1];
var url = arguments[2].split("?")[0];
var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
})
var queue = [];
for (let i = 0; i < data2.length; i++) {
    queue.push(getdata(i));
}
function getdata(i) {
    const p = new Promise((resolve, reject) => {
        data.variables.userId = data2[i][1];
        let param = "?" + Object.entries(data).map((e) => { return `${e[0].replaceAll("%22", "")}=${encodeURIComponent(JSON.stringify(e[1]))}` }).join("&");
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url + param);
        xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
        xhr.setRequestHeader('x-csrf-token', token);
        xhr.setRequestHeader('x-twitter-active-user', 'yes');
        xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
        xhr.setRequestHeader('x-twitter-client-language', 'ja');
        xhr.withCredentials = true;
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                let res = JSON.parse(xhr.responseText);
                try {
                    data2[i].push(res.data.user.result.legacy.name);
                    data2[i].push(res.data.user.result.legacy.screen_name);
                    data2[i].push(res.data.user.result.legacy.profile_image_url_https);
                } catch {
                    data2[i].push("unknown");
                    data2[i].push("unknown");
                    data2[i].push("");
                }
                resolve();
            }
        }
        xhr.send();
    });
    return p;
}
const promise = Promise.all(queue);
promise.then((e) => window.data = data2);
            """, getuser_body, data, getuser_url)
            while True:
                time.sleep(0.01)
                res = driver2.execute_script("return window.data")
                if res != "":
                    break
            driver.execute_script('document.getElementById("input").value = arguments[0]; start();', str(res))
            wait2 = WebDriverWait(driver, 180).until(EC.alert_is_present())
        except Exception as e:
            traceback.print_exc()
            time.sleep(2)
        else:
            Alert(driver).accept()
            bin = driver.execute_script('return window.res')
            postrank(bin, driver2, "This month's top 30")
            break


def browser(tweets, driver2):
    global driver4
    for _ in range(10):
        try:
            if driver4 == "":
                options=Options()
                #options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-gpu")
                options.add_argument('--disable-dev-shm-usage')
                driver4 = webdriver.Chrome(options = options)
                driver4.set_window_size(589, 1)
                driver4.get(os.environ['HTML_URL'])
                wait = WebDriverWait(driver4, 10).until(EC.alert_is_present())
                Alert(driver4).accept()
            
        except Exception as e:
            traceback.print_exc()
            time.sleep(2)
        else:
            break
    
    for _ in range(5):
        try:
            driver4.execute_script('document.getElementById("input").value = arguments[0]; start();', tweets)
            wait2 = WebDriverWait(driver4, 180).until(EC.alert_is_present())
        except Exception as e:
            traceback.print_exc()
            time.sleep(1)
        else:
            Alert(driver4).accept()
            bin = driver4.execute_script('return window.res')
            postrank(bin, driver2, "Today's top 30")
            wait3 = WebDriverWait(driver4, 300).until(EC.alert_is_present())
            Alert(driver4).accept()
            break
            
    dt = datetime.datetime.now()
    if dt.replace(day=calendar.monthrange(dt.year, dt.month)[1]).day == dt.day:
        browser2(driver4, driver2)
        
def round(flo, num):
    if num >= 4:
        return math.floor(flo * (10 ** num)) / (10 ** num)
    else:
        n_str = str(flo)
        return Decimal(n_str).quantize(Decimal(str(10 ** (-1 * num))), rounding=ROUND_HALF_UP)

def make_ranking2(dict):
    global world_rank, today_result
    preres = {}
    clients = ["Twitter for iPhone",  "Twitter for Android",  "Twitter Web Client",  "TweetDeck",  "TweetDeck Web App",  "Twitter for iPad",  "Twitter for Mac",  "Twitter Web App",  "Twitter Lite",  "Mobile Web (M2)",  "Twitter for Windows",  "Janetter",  "Janetter for Android",  "Janetter Pro for iPhone",  "Janetter for Mac",  "Janetter Pro for Android",  "Tweetbot for iΟS",  "Tweetbot for iOS",  "Tweetbot for Mac",  "twitcle plus",  "ツイタマ",  "ツイタマ for Android",  "ツイタマ+ for Android",  "Sobacha",  "SobaCha",  "Metacha",  "MetaCha",  "MateCha",  "ツイッターするやつ",  "ツイッターするやつγ",  "ツイッターするやつγ pro",  "jigtwi",  "feather for iOS",  "hamoooooon",  "Hel2um on iOS",  "Hel1um Pro on iOS",  "Hel1um on iOS",  "undefined"]
    ii = 1
    todayplayer = []
    for key in pre_result:
        world_rank[key][2] = pre_result[key][4]
    for i in range(len(dict)):
        todayplayer.append(dict[i][6])
        if i > 1:
            if float(dict[i][2]) > float(dict[i - 1][2]):
                ii = i + 1
        preres[dict[i][6]] = [str(ii), dict[i][1], dict[i][2]]
        todayp = 10000 * 2 ** (-10 * float(dict[i][2]))
        if dict[i][6] in world_rank:
            if float(world_rank[dict[i][6]][0]) == float(dict[i][2]):
                world_rank[dict[i][6]][1] += 1
            if float(world_rank[dict[i][6]][0]) > float(dict[i][2]):
                world_rank[dict[i][6]][0] = dict[i][2]
            if float(pre_result[dict[i][6]][2]) < todayp:
                world_rank[dict[i][6]][6] = '{:.2f}'.format(round((float(pre_result[dict[i][6]][3]) + todayp) / 10, 2))
            else:
                world_rank[dict[i][6]][6] = '{:.2f}'.format(round((float(pre_result[dict[i][6]][2]) + float(pre_result[dict[i][6]][3])) / 10, 2))
            world_rank[dict[i][6]][4] = str(round((float(pre_result[dict[i][6]][0]) + float(pre_result[dict[i][6]][1])) / 10, 4))
            for client in clients:
                if client in dict[i][3]:
                    if float(pre_result[dict[i][6]][0]) < todayp:
                        world_rank[dict[i][6]][4] = str(round((float(pre_result[dict[i][6]][1]) + todayp) / 10, 4))
                        if float(world_rank[dict[i][6]][4]) > float(world_rank[dict[i][6]][2]):
                            world_rank[dict[i][6]][2] = world_rank[dict[i][6]][4]
                    break
            world_rank[dict[i][6]][7] += 1
        else:
            world_rank[dict[i][6]] = [dict[i][2], 1, "0.00", 0, "0.00", 0, '{:.2f}'.format(round(todayp / 10, 2)), 1, 0, 0, 0, 0]
            for client in clients:
                if client in dict[i][3]:
                    world_rank[dict[i][6]][2] = str(round(todayp / 10, 4))
                    world_rank[dict[i][6]][4] = str(round(todayp / 10, 4))
                    break
        
        if ii == 1:
            world_rank[dict[i][6]][8] += 1
        if ii == 2:
            world_rank[dict[i][6]][9] += 1
        if ii == 3:
            world_rank[dict[i][6]][10] += 1
        if ii <= 30:
            world_rank[dict[i][6]][11] += 1

    del world_rank["累計"]
    del world_rank["現在"]
    for key in world_rank.keys():
        if key not in todayplayer:
            world_rank[key][4] = str(round((float(pre_result[key][0]) + float(pre_result[key][1])) / 10, 4));
            world_rank[key][6] = '{:.2f}'.format(round((float(pre_result[key][2]) + float(pre_result[key][3])) / 10, 2));
    world_sort1 = sorted(world_rank.items(), key=lambda x:float(x[1][2]), reverse=True)
    ii = 0
    count1 = 0
    before = 10001.00
    for i in world_sort1:
        if float(i[1][2]) < before:
            ii = count1 + 1
            before = float(i[1][2])
        world_rank[i[0]][2] = '{:.2f}'.format(round(float(world_rank[i[0]][2]), 2))
        if float(i[1][2]) == 0.0:
            world_rank[i[0]][3] = '-'
        else:
            count1 += 1
            world_rank[i[0]][3] = ii

    world_sort2 = sorted(world_rank.items(), key=lambda x:float(x[1][4]), reverse=True)
    ii = 0
    count2 = 0
    before = 10001.00
    for i in world_sort2:
        if float(i[1][4]) < before:
            ii = count2 + 1
            before = float(i[1][4])
        world_rank[i[0]][4] = '{:.2f}'.format(round(float(world_rank[i[0]][4]), 2))
        if float(i[1][4]) == 0.0:
            world_rank[i[0]][5] = '-'
        else:
            count2 += 1
            world_rank[i[0]][5] = ii

    world_rank["累計"] = [str(count1)]
    world_rank["現在"] = [str(count2)]
    today_result = preres
    today_result["参加者数"] = [str(len(dict))]
    print("set pre-result", datetime.datetime.now())
                

def make_ranking(dict, driver):
    time1 = datetime.datetime(start_now.year, start_now.month, start_now.day, 3, 34, 0)
    winner = ""
    users = []
    dict2 = []
    for item in dict:
        if item["text"] == "334" and item["user"]["id_str"] not in users:
            users.append(item["user"]["id_str"])
            time2 = TweetIdTime(int(item["id_str"]))
            res = (time2 - time1).total_seconds()
            if 0 <= res and res < 1:
                result = '{:.3f}'.format(res)
                if winner == "" or result == winner:
                    winner = result
                    threading.Thread(target=retweet, args=(item["id_str"], driver,)).start()

                img_src = "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png"
                if item["user"]["profile_image_url_https"] != "":
                    img_src = item["user"]["profile_image_url_https"]
                
                dict2.append([
                    img_src,
                    item["user"]["name"],
                    str(result),
                    item["source"],
                    item["id_str"],
                    "@" + item["user"]["screen_name"],
                    item["user"]["id_str"]
                ])

    print(str(dict2))
    threading.Thread(target=browser, args=(str(dict2), driver,)).start()
    threading.Thread(target=make_ranking2, args=(dict2,)).start()

    

def get_334(driver):
    time1 = datetime.datetime(start_now.year, start_now.month, start_now.day, 3, 33, 59)
    time2 = datetime.datetime(start_now.year, start_now.month, start_now.day, 3, 34, 1)
    get_time = datetime.datetime(start_now.year, start_now.month, start_now.day, 3, 34, 2)
    while True:
        if get_time < datetime.datetime.now():
            print("get334 start: ")
            print(datetime.datetime.now())
            driver.execute_script("""
window.data = "";
var url1 = 'https://api.twitter.com/1.1/search/';
var url2 = '.json?count=100&result_type=recent&q=334 since:""" + time1.strftime('%Y-%m-%d_%H:%M:%S_JST') + """ until:""" + time2.strftime('%Y-%m-%d_%H:%M:%S_JST') + """ -filter:retweets -filter:quote -from:rank334 -from:rank334_2';
var out = [];
var out2 = [];
var out3 = [];
var out4 = [];
var out7 = [];
var cookie = document.cookie.replaceAll(" ", "").split(";");
var token = "";
cookie.forEach(function (value) {
    let content = value.split('=');
    if (content[0] == "ct0") token = content[1];
})
let time1 = new Date()
time1.setHours(3);
time1.setMinutes(34);
time1.setSeconds(0);
time1.setMilliseconds(0);

function get_queryid(name, defaultId) {
    try {
        let queryids = webpackChunk_twitter_responsive_web;
        for (let i = 0; i < queryids.length; i++) {
            for (let key in queryids[i][1]) {
                try {
                    if (queryids[i][1][key].length === 1) {
                        let tmp = {};
                        queryids[i][1][key](tmp);
                        if (tmp.exports.operationName === name) return tmp.exports.queryId;
                    }
                } catch { }
            }
        }
        return defaultId;
    } catch {
        return defaultId;
    }
}

var data = arguments[0];
data.variables["cursor"] = "";
data.variables.seenTweetIds = [];
let queryid = get_queryid("HomeLatestTimeline", "02vsYHq98uLTwnNu2VF0Lg");
data.queryId = queryid;
var data2 = arguments[1];
data2.variables["cursor"] = "";
data2.variables["rawQuery"] = "334 -filter:retweets -filter:quote -from:rank334 -from:rank334_2 since:""" + time1.strftime('%Y-%m-%d_%H:%M:%S_JST') + """ until:""" + time2.strftime('%Y-%m-%d_%H:%M:%S_JST') + """"
let queryid2 = get_queryid("SearchTimeline", "KUnA_SzQ4DMxcwWuYZh9qg");
var count = 0;
//get_tweets();
//get_tweets2();
get_tweets3(data);
get_tweets4(data2);
setTimeout(function() { get_tweets5(data2) }, 2000);


function setheader(xhr) {
    xhr.setRequestHeader('Authorization', 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA');
    xhr.setRequestHeader('x-csrf-token', token);
    xhr.setRequestHeader('x-twitter-active-user', 'yes');
    xhr.setRequestHeader('x-twitter-auth-type', 'OAuth2Session');
    xhr.setRequestHeader('x-twitter-client-language', 'ja');
    xhr.withCredentials = true;
}

function get_tweets(max_id) {
    let xhr = new XMLHttpRequest();
    let url = max_id !== undefined ? url1 + "universal" + url2 + " max_id:" + max_id : url1 + "universal" + url2;
    xhr.open('GET', url);
    setheader(xhr);
    xhr.send();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.error("get1");
            if (xhr.status === 200) {
                try {
                    res = JSON.parse(xhr.responseText).modules;
                    if (res.length <= 0 || (max_id !== undefined && res.length <= 1)) final([]);
                    else {
                        if (max_id !== undefined) res.shift();
                        for (let i = 0; i < res.length; i++) {
                            let tweet = res[i].status.data;
                            tweet["index"] = parseInt(BigInt(tweet.id_str).toString(2).slice(0, -22), 2) + 1288834974657;
                            out.push(tweet);
                        }
                        get_tweets(out[out.length - 1].id_str);
                    }
                } catch (e) {
                    console.error(e);
                    final([]);
                }
            } else final([]);
        }
    }
}

function get_tweets2(max_id) {
    let xhr = new XMLHttpRequest();
    let url = max_id !== undefined ? url1 + "tweets" + url2 + " max_id:" + max_id : url1 + "tweets" + url2;
    xhr.open('GET', url);
    setheader(xhr);
    xhr.send();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.error("get2");
            if (xhr.status === 200) {
                try {
                    res = JSON.parse(xhr.responseText);
                    if ('statuses' in res) {
                        res = res.statuses;
                        if (res.length <= 0 || (max_id !== undefined && res.length <= 1)) final(out2);
                        else {
                            if (max_id !== undefined) res.shift();
                            for (let i = 0; i < res.length; i++) {
                                let tweet = res[i];
                                tweet["index"] = parseInt(BigInt(tweet.id_str).toString(2).slice(0, -22), 2) + 1288834974657;
                                out2.push(res[i]);
                            }
                            get_tweets2(out2[out2.length - 1].id_str);
                        }
                    } else final(out2);
                } catch (e) {
                    console.error(e);
                    final(out2);
                }
            } else final(out2);
        }
    }
}

function get_tweets3(d) {
    try {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'https://api.twitter.com/graphql/' + queryid + '/HomeLatestTimeline');
        setheader(xhr);
        xhr.setRequestHeader('content-type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                console.error("get3");
                if (xhr.status === 200) {
                    try {
                        var flag = true;
                        let entries = JSON.parse(xhr.responseText).data.home.home_timeline_urt.instructions[0].entries;
                        for (let i = 0; i < entries.length; i++) {
                            if (!entries[i].entryId.includes("promoted") && !entries[i].entryId.includes("cursor")) {
                                try {
                                    if (entries[i].entryId.includes("home")) var res = entries[i].content.items[0].item.itemContent.tweet_results.result;
                                    else var res = entries[i].content.itemContent.tweet_results.result;
                                    if ("tweet" in res) res = res.tweet;
                                    let legacy = res.legacy;
                                    if (new Date(legacy.created_at) < time1) {
                                        if (entries[i].entryId.includes("home")) continue;
                                        else {
                                            flag = false;
                                            final(out3);
                                            break;
                                        }
                                    }
                                    legacy["text"] = legacy.full_text;
                                    if (legacy.text != "334") continue;
                                    legacy["source"] = res.source;
                                    legacy["index"] = parseInt(BigInt(legacy.id_str).toString(2).slice(0, -22), 2) + 1288834974657;
                                    legacy["user"] = res.core.user_results.result.legacy;
                                    legacy.user["id_str"] = legacy.user_id_str;
                                    out3.push(legacy);
                                    continue;
                                } catch (e) {
                                    console.error(e);
                                }
                            }
                            if (entries[i].entryId.includes("bottom")) {
                                let data3 = Object.assign({}, data);
                                data3.variables.cursor = entries[i].content.value;
                                flag = false;
                                get_tweets3(data3);
                                break;
                            }
                        }
                        if (flag) final(out3);
                    } catch (e) {
                        console.error(e);
                        final(out3);
                    }
                } else final(out3);
            }
        }
        xhr.send(JSON.stringify(d));
    } catch (e) {
        console.error(e);
        final(out3);
    }
}

function get_tweets4(d) {
    try {
        let param = "?" + Object.entries(d).map((e) => {
            return `${e[0].replaceAll("%22", "")}=${encodeURIComponent(JSON.stringify(e[1]))}`
        }).join("&")
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'https://api.twitter.com/graphql/' + queryid2 + '/SearchTimeline' + param);
        setheader(xhr);
        xhr.setRequestHeader('content-type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                console.error("get4");
                if (xhr.status === 200) {
                    try {
                        var flag = true;
                        let instructions = JSON.parse(xhr.responseText).data.search_by_raw_query.search_timeline.timeline.instructions;
                        var flag2 = true;
                        loop: for (let j = 0; j < instructions.length; j++) {
                            if ("entries" in instructions[j]) var entries = instructions[j].entries;
                            else if ("entry" in instructions[j]) var entries = [instructions[j].entry];
                            else continue;
                            for (let i = 0; i < entries.length; i++) {
                                if (!entries[i].entryId.includes("promoted") && !entries[i].entryId.includes("cursor")) {
                                    try {
                                        flag2 = false;
                                        var res = entries[i].content.itemContent.tweet_results.result;
                                        if ("tweet" in res) res = res.tweet;
                                        let legacy = res.legacy;
                                        if (new Date(legacy.created_at) < time1) {
                                            if (entries[i].entryId.includes("home")) continue;
                                            else {
                                                flag = false;
                                                final(out4);
                                                break loop;
                                            }
                                        }
                                        legacy["text"] = legacy.full_text;
                                        if (legacy.text != "334") continue;
                                        legacy["source"] = res.source;
                                        legacy["index"] = parseInt(BigInt(legacy.id_str).toString(2).slice(0, -22), 2) + 1288834974657;
                                        legacy["user"] = res.core.user_results.result.legacy;
                                        legacy.user["id_str"] = legacy.user_id_str;
                                        out4.push(legacy);
                                        continue;
                                    } catch (e) {
                                        console.error(e);
                                    }
                                }
                                if (entries[i].entryId.includes("bottom")) {
                                    let data3 = JSON.parse(JSON.stringify(data2));
                                    data3.variables.cursor = entries[i].content.value;
                                    flag = false;
                                    if (flag2) final(out4);
                                    else get_tweets4(data3);
                                    break loop;
                                }
                            }
                        }
                        if (flag) final(out4);
                    } catch (e) {
                        console.error(e);
                        final(out4);
                    }
                } else final(out4);
            }
        }
        xhr.send();
    } catch (e) {
        console.error(e);
        final(out4);
    }
}

function get_tweets5(d) {
    try {
        let param = "?" + Object.entries(d).map((e) => {
            return `${e[0].replaceAll("%22", "")}=${encodeURIComponent(JSON.stringify(e[1]))}`
        }).join("&")
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'https://api.twitter.com/graphql/' + queryid2 + '/SearchTimeline' + param);
        setheader(xhr);
        xhr.setRequestHeader('content-type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                console.error("get5");
                if (xhr.status === 200) {
                    try {
                        var flag = true;
                        let instructions = JSON.parse(xhr.responseText).data.search_by_raw_query.search_timeline.timeline.instructions;
                        var flag2 = true;
                        loop: for (let j = 0; j < instructions.length; j++) {
                            if ("entries" in instructions[j]) var entries = instructions[j].entries;
                            else if ("entry" in instructions[j]) var entries = [instructions[j].entry];
                            else continue;
                            for (let i = 0; i < entries.length; i++) {
                                if (!entries[i].entryId.includes("promoted") && !entries[i].entryId.includes("cursor")) {
                                    try {
                                        flag2 = false;
                                        var res = entries[i].content.itemContent.tweet_results.result;
                                        if ("tweet" in res) res = res.tweet;
                                        let legacy = res.legacy;
                                        if (new Date(legacy.created_at) < time1) {
                                            if (entries[i].entryId.includes("home")) continue;
                                            else {
                                                flag = false;
                                                final(out7);
                                                break loop;
                                            }
                                        }
                                        legacy["text"] = legacy.full_text;
                                        if (legacy.text != "334") continue;
                                        legacy["source"] = res.source;
                                        legacy["index"] = parseInt(BigInt(legacy.id_str).toString(2).slice(0, -22), 2) + 1288834974657;
                                        legacy["user"] = res.core.user_results.result.legacy;
                                        legacy.user["id_str"] = legacy.user_id_str;
                                        out7.push(legacy);
                                        continue;
                                    } catch (e) {
                                        console.error(e);
                                    }
                                }
                                if (entries[i].entryId.includes("bottom")) {
                                    let data3 = JSON.parse(JSON.stringify(data2));
                                    data3.variables.cursor = entries[i].content.value;
                                    flag = false;
                                    if (flag2) final(out7);
                                    else get_tweets5(data3);
                                    break loop;
                                }
                            }
                        }
                        if (flag) final(out7);
                    } catch (e) {
                        console.error(e);
                        final(out7);
                    }
                } else final(out7);
            }
        }
        xhr.send();
    } catch (e) {
        console.error(e);
        final(out7);
    }
}

function final(out6) {
    out = out.concat(out6);
    count++;
    if (count < 3) return;
    let out5 = []
    let ids = [];
    out.sort((a, b) => a.index - b.index);
    for (let i = 0; i < out.length; i++) {
        if (!ids.includes(out[i].id_str)) {
            out5.push(out[i]);
            ids.push(out[i].id_str);
        }
    }
    window.data = out5;
}
            """, timeline_body, search_body)
            while True:
                time.sleep(0.01)
                res = driver.execute_script("return window.data")
                if res != "":
                    print("get334 from Ranker", datetime.datetime.now())
                    add = []
                    for _ in range(5):
                        try:
                            r = requests.get(os.environ['GAS_URL2'], timeout=10)
                            r_json = r.json()
                            time.sleep(0.5)
                            print("get334 from Ranker2", datetime.datetime.now())
                            add = r_json["data"]
                            if add == []:
                                time.sleep(0.5)
                            else:
                                break
                        except Exception as e:
                            traceback.print_exc()
                            break

                    res = res + add
                    res.sort(key=lambda x: int(x["index"]))
                    ids = []
                    res2 = []
                    for r in res:
                        if r["id_str"] not in ids:
                            res2.append(r)
                            ids.append(r["id_str"])

                    print("get334 conplete: ")
                    print(datetime.datetime.now())
                    make_ranking(res2, driver)
                    break
            break
        time.sleep(0.01)



def notice(driver):
    global today_result, world_rank, load_res_yet, driver4
    notice_time = datetime.datetime(start_now.year, start_now.month, start_now.day, 3, 32, 0)
    while True:
        if notice_time < datetime.datetime.now():
            today_result = {}
            #world_rank = {}
            load_res_yet = True
            
            req = copy.deepcopy(post_body)
            req["variables"]["tweet_text"] = "334観測中 (" + datetime.datetime.now().date().strftime('%Y/%m/%d') + ")"
            del req["variables"]['reply']
            print("notice tweet :")
            threading.Thread(target=reply, args=(req, driver,)).start()
    
            break
        time.sleep(5)



def start():
    global start_now, start_time, end_time, driver3, driver4
    for _ in range(10):
        try:
            options=Options()
            #options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(options = options)
            driver.set_script_timeout(5)
            driver3 = webdriver.Chrome(options = options)
            driver4 = webdriver.Chrome(options = options)
            driver4.set_window_size(589, 1)
            driver4.get(os.environ['HTML_URL'])
            wait = WebDriverWait(driver4, 10).until(EC.alert_is_present())
            Alert(driver4).accept()
            
        except Exception as e:
            traceback.print_exc()
            time.sleep(2)
            if _ == 9:
                sys.exit(1)
                break
        else:
            break

            
    times = [
        [datetime.datetime(start_now.year, start_now.month, start_now.day, 0, 33, 0), datetime.datetime(start_now.year, start_now.month, start_now.day, 4, 33, 0)], #0:03
        [datetime.datetime(start_now.year, start_now.month, start_now.day, 4, 33, 0), datetime.datetime(start_now.year, start_now.month, start_now.day, 8, 33, 0)], #4:03
        [datetime.datetime(start_now.year, start_now.month, start_now.day, 8, 33, 0), datetime.datetime(start_now.year, start_now.month, start_now.day, 12, 33, 0)], #8:03
        [datetime.datetime(start_now.year, start_now.month, start_now.day, 12, 33, 0), datetime.datetime(start_now.year, start_now.month, start_now.day, 16, 33, 0)], #12:03
        [datetime.datetime(start_now.year, start_now.month, start_now.day, 16, 33, 0), datetime.datetime(start_now.year, start_now.month, start_now.day, 20, 33, 0)], #16:03
        [datetime.datetime(start_now.year, start_now.month, start_now.day, 20, 33, 0), datetime.datetime(start_now.year, start_now.month, start_now.day, 0, 33, 0) + datetime.timedelta(days=1)], #20:03
        [datetime.datetime(start_now.year, start_now.month, start_now.day, 0, 33, 0) + datetime.timedelta(days=1), datetime.datetime(start_now.year, start_now.month, start_now.day, 0, 33, 0) + datetime.timedelta(days=1)]
    ]
    for i in range(len(times)):
        if start_now < times[i][0]:
            start_time = times[i][0]
            end_time = times[i][1]
            
            get_allresult()
            if len(sys.argv) != 1:
                start_time = datetime.datetime.now().replace(microsecond = 0) + datetime.timedelta(seconds=240)
                end_time = times[i][0]
            login_twitter("rank334", os.environ['PASS'], os.environ['TEL'], driver)
            login_twitter2("rank334_2", os.environ['PASS'], os.environ['TEL'], driver)
            threading.Thread(target=interval, args=(start_time, start_time + datetime.timedelta(seconds=5), end_time, 0, driver,)).start()
            threading.Thread(target=interval2, args=(start_time, end_time, driver,)).start()
            
            if (len(sys.argv) == 1 and i == 0) or (len(sys.argv) != 1 and i == 1 and datetime.datetime.now() < datetime.datetime(start_now.year, start_now.month, start_now.day, 3, 34, 0)):
                threading.Thread(target=interval3, args=(datetime.datetime(start_now.year, start_now.month, start_now.day, 3, 34, 0), 0, driver,)).start()
                get_preresult()
                notice(driver)
                get_334(driver)
                
            break
         
start()
