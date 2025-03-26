import chromedriver_binary
import calendar, copy, datetime, json, os, requests, sys, threading, time, traceback, re, gzip, io, hmac, hashlib, base64, urllib.parse, random
from collections import Counter, defaultdict
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver
from requests_oauthlib import OAuth1Session


TIME334 = [3, 34]
KEYWORD = "334"
PHP_URL = os.environ["PHP_URL"]
TOKENS = os.environ["TOKENS"]
API_KEYS = os.environ["KEYS"]
HTML_URL = "https://abshrimp.github.io/334ranker/"
HTML_URL2 = "https://abshrimp.github.io/334ranker/index2.html"
ANDROID_AUTH = os.environ["AUTH"]
clients = ['Twitter for iPhone',  'Twitter for Android',  'Twitter Web Client',  'TweetDeck',  'TweetDeck Web App',  'Twitter for iPad',  'Twitter for Mac',  'Twitter Web App',  'Twitter Lite',  'Mobile Web (M2)',  'Twitter for Windows',  'Janetter',  'Janetter for Android',  'Janetter Pro for iPhone',  'Janetter for Mac',  'Janetter Pro for Android',  'Tweetbot for iΟS',  'Tweetbot for iOS',  'Tweetbot for Mac',  'twitcle plus',  'ツイタマ',  'ツイタマ for Android',  'ツイタマ+ for Android',  'Sobacha',  'SobaCha',  'Metacha',  'MetaCha',  'MateCha',  'ツイッターするやつ',  'ツイッターするやつγ',  'ツイッターするやつγ pro',  'jigtwi',  'feather for iOS',  'hamoooooon',  'Hel2um on iOS',  'Hel1um Pro on iOS',  'Hel1um on iOS',  'undefined']

records_rank, today_result, request_body, request_header = {}, {}, {}, {}
past_records, rep_accounts, search_accounts = [], [], []
today_joined = 0
joined_num = {"max_pt_rank": 0, "now_pt_rank": 0}
prepare_flag = False

# main_account = [name, token, secret] nameは小文字で
# rep_accounts = [[name, token, secret], ...] nameは小文字で
# search_accounts = [[token, secret], ...]
# name$token$secret|name$token$secret|token$secret#token$secret#...

split_tokens = TOKENS.split("|")
main_account = split_tokens[0].split("$")
tokens = split_tokens[1].split("#")
for account in tokens:
    rep_accounts.append(account.split("$"))
tokens = split_tokens[2].split("#")
for account in tokens:
    search_accounts.append(account.split("$"))

CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = API_KEYS.split("|")[:4]
oauth1 = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
consumer_key, consumer_secret, kdt, x_twitter_client_adid, x_client_uuid, x_twitter_client_deviceid = ANDROID_AUTH.split("|")


def TweetIdTime(id):
    return datetime.datetime.fromtimestamp(((id >> 22) + 1288834974657) / 1000.0)


def If(bool, t, f):
    return t if bool else f


def sendAndroid(url, params, oauth_token, token_secret, http_method="GET"):
    try:
        host = "api.twitter.com"
        url = "https://" + host + url

        oauth_nonce = "".join([str(random.randint(0, 9)) for _ in range(32)])
        oauth_timestamp = str(int(time.time()))
        parameters = {
            "oauth_consumer_key": consumer_key,
            "oauth_token": oauth_token,
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": oauth_timestamp,
            "oauth_nonce": oauth_nonce,
            "oauth_version": "1.0",
        }
        sign_params = If (http_method == "POST" and "graphql" in url, parameters, {**parameters, **params})
        parameter_string = "&".join(f"{k}={v}" for k, v in sorted(sign_params.items()))
        signature_base_string = f"{http_method}&{urllib.parse.quote(url, '')}&{urllib.parse.quote(parameter_string, '')}"
        signing_key = f"{consumer_secret}&{token_secret}"
        digest = hmac.new(signing_key.encode(), signature_base_string.encode(), hashlib.sha1).digest()
        oauth_signature = base64.b64encode(digest).decode()
        parameters["oauth_signature"] = oauth_signature

        headers = {
            "Host": host,
            "Timezone": "Asia/Tokyo",
            "Os-Security-Patch-Level": "2021-08-05",
            "Optimize-Body": "true",
            "Accept": "application/json",
            "X-Twitter-Client": "TwitterAndroid",
            "X-Attest-Token": "no_token",
            "User-Agent": "TwitterAndroid/10.53.2-release.0 (310532000-r-0)",
            "X-Twitter-Client-Adid": x_twitter_client_adid,
            #'Accept-Encoding': 'gzip, deflate, br',
            "X-Twitter-Client-Language": "en-US",
            "X-Client-Uuid": x_client_uuid,
            "X-Twitter-Client-Deviceid": x_twitter_client_deviceid,
            "Authorization": f'OAuth realm="http://api.twitter.com/", ' + ", ".join(f'{urllib.parse.quote(k)}="{urllib.parse.quote(v)}"' for k, v in parameters.items()),
            "X-Twitter-Client-Version": "10.53.2-release.0",
            "Cache-Control": "no-store",
            "X-Twitter-Active-User": "yes",
            "X-Twitter-Api-Version": "5",
            "Kdt": kdt,
            "X-Twitter-Client-Limit-Ad-Tracking": "0",
            "Accept-Language": "en-US",
            "X-Twitter-Client-Flavor": "",
        }

        if http_method == "GET":
            url += "?"
            for param in params:
                url += param + "=" + params[param] + "&"
            url = url[:-1]
            response = requests.get(url, headers=headers)

        else:
            if "graphql" in url:
                json_bytes = json.dumps(params).encode("utf-8")
                gzip_buffer = io.BytesIO()
                with gzip.GzipFile(fileobj=gzip_buffer, mode="wb") as f:
                    f.write(json_bytes)
                gzip_data = gzip_buffer.getvalue()
                post_headers = {
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Encoding": "gzip",
                    "Content-Type": "application/json",
                }
                headers = {**headers, **post_headers}
                response = requests.post(url, headers=headers, data=gzip_data)
            else:
                url += "?"
                for param in params:
                    url += f'{param}={params[param]}&'
                url = url[:-1]
                post_headers = {"Content-Type": "application/x-www-form-urlencoded"}
                headers = {**headers, **post_headers}
                response = requests.post(url, headers=headers)

        return response.json()
    except:
        return {"errors": "err"}


def create_tweet(text, oauth_token, token_secret, rep_id=None):
    reply_str = If (rep_id is not None, f',"reply":{{"exclude_reply_user_ids":[],"in_reply_to_tweet_id":{rep_id}}}', "")
    json_data = {
        "features": '{"longform_notetweets_inline_media_enabled":true,"super_follow_badge_privacy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"super_follow_user_api_enabled":true,"super_follow_tweet_api_enabled":true,"articles_api_enabled":true,"android_graphql_skip_api_media_color_palette":true,"creator_subscriptions_tweet_preview_api_enabled":true,"freedom_of_speech_not_reach_fetch_enabled":true,"tweetypie_unmention_optimization_enabled":true,"longform_notetweets_consumption_enabled":true,"subscriptions_verification_info_enabled":true,"blue_business_profile_image_shape_enabled":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"immersive_video_status_linkable_timestamps":true,"super_follow_exclusive_tweet_notifications_enabled":true}',
        "variables": f'{{"nullcast":false,"includeTweetImpression":true,"includeHasBirdwatchNotes":false,"includeEditPerspective":false,"includeEditControl":true,"includeCommunityTweetRelationship":false{reply_str},"includeTweetVisibilityNudge":true,"tweet_text":"{text}"}}',
    }
    return sendAndroid("/graphql/B8zcLvy-DN84y11pB2NObA/CreateTweet", json_data, oauth_token, token_secret, "POST")


def create_follow(id, oauth_token, token_secret):
    payload = {
        "ext": "mediaRestrictions%2CaltText%2CmediaStats%2CmediaColor%2Cinfo360%2ChighlightedLabel%2CunmentionInfo%2CeditControl%2CpreviousCounts%2ClimitedActionResults%2CsuperFollowMetadata",
        "send_error_codes": "true",
        "user_id": id,
        "handles_challenges": "1",
    }
    return sendAndroid("//friendships/create.json", payload, oauth_token, token_secret, "POST")


def get_mentions(oauth_token, token_secret, cursor = None):
    params = {
        "earned": "true",
        "include_ext_is_blue_verified": "true",
        "include_ext_verified_type": "true",
        "include_ext_profile_image_shape": "true",
        "include_ext_is_tweet_translatable": "true",
        "include_entities": "true",
        "include_cards": "true",
        "cards_platform": "Android-12",
        "include_carousels": "true",
        "ext": "mediaRestrictions%2CaltText%2CmediaStats%2CmediaColor%2Cinfo360%2ChighlightedLabel%2CunmentionInfo%2CeditControl%2CpreviousCounts%2ClimitedActionResults%2CsuperFollowMetadata",
        "include_media_features": "true",
        "include_blocking": "true",
        "include_blocked_by": "true",
        "include_quote_count": "true",
        "include_ext_previous_counts": "true",
        "include_ext_limited_action_results": "true",
        "tweet_mode": "extended",
        "include_composer_source": "true",
        "include_ext_media_availability": "true",
        "include_ext_edit_control": "true",
        "include_reply_count": "true",
        "include_ext_sensitive_media_warning": "true",
        "include_ext_views": "true",
        "simple_quoted_tweet": "true",
        "include_ext_birdwatch_pivot": "true",
        "include_user_entities": "true",
        "include_profile_interstitial_type": "true",
        "include_ext_professional": "true",
        "include_viewer_quick_promote_eligibility": "true",
        "include_ext_has_nft_avatar": "true",
    }
    if cursor != None:
        params["cursor"] = cursor
    return sendAndroid(
        "/2/notifications/mentions.json", params, oauth_token, token_secret
    )


def search_timeline(text, oauth_token, token_secret, cursor=None):
    cursor_param = f"cursor%22%3A%22{cursor}%22%2C%22" if cursor is not None else ""
    params = {
        "variables": f'%7B%22{cursor_param}includeTweetImpression%22%3Atrue%2C%22query_source%22%3A%22typed_query%22%2C%22includeHasBirdwatchNotes%22%3Afalse%2C%22includeEditPerspective%22%3Afalse%2C%22includeEditControl%22%3Atrue%2C%22query%22%3A%22{urllib.parse.quote(text)}%22%2C%22timeline_type%22%3A%22Latest%22%7D',
        "features": "%7B%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22super_follow_badge_privacy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22super_follow_user_api_enabled%22%3Atrue%2C%22unified_cards_ad_metadata_container_dynamic_card_content_query_enabled%22%3Atrue%2C%22super_follow_tweet_api_enabled%22%3Atrue%2C%22articles_api_enabled%22%3Atrue%2C%22android_graphql_skip_api_media_color_palette%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22subscriptions_verification_info_enabled%22%3Atrue%2C%22blue_business_profile_image_shape_enabled%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22immersive_video_status_linkable_timestamps%22%3Atrue%2C%22super_follow_exclusive_tweet_notifications_enabled%22%3Atrue%7D",
    }
    return sendAndroid("/graphql/4NfkwyiViTLQw7ZcJmxtKg/SearchTimeline", params, oauth_token, token_secret)


def search_timeline_web(text, oauth_token, token_secret, cursor=None):
    cursor_param = f"cursor%22%3A%22{cursor}%22%2C%22" if cursor is not None else ""
    params = {
        "variables": f'%7B%22rawQuery%22%3A%22{urllib.parse.quote(text)}%22%2C%22count%22%3A20%2C%22{cursor_param}querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Latest%22%7D',
        "features": "%7B%22profile_label_improvements_pcf_label_in_post_enabled%22%3Afalse%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22premium_content_api_read_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22responsive_web_grok_analyze_button_fetch_trends_enabled%22%3Afalse%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D",
    }
    return sendAndroid("/graphql/oyfSj18lHmR7VGC8aM2wpA/SearchTimeline", params, oauth_token, token_secret)


def get_user(id, oauth_token, token_secret):
    params = {
        "variables": f"%7B%22include_smart_block%22%3Atrue%2C%22includeTweetImpression%22%3Atrue%2C%22include_profile_info%22%3Atrue%2C%22includeTranslatableProfile%22%3Atrue%2C%22includeHasBirdwatchNotes%22%3Afalse%2C%22include_tipjar%22%3Atrue%2C%22includeEditPerspective%22%3Afalse%2C%22include_reply_device_follow%22%3Atrue%2C%22includeEditControl%22%3Atrue%2C%22include_verified_phone_status%22%3Afalse%2C%22rest_id%22%3A%22{id}%22%7D",
        "features": "%7B%22verified_phone_label_enabled%22%3Afalse%2C%22super_follow_badge_privacy_enabled%22%3Atrue%2C%22subscriptions_verification_info_enabled%22%3Atrue%2C%22super_follow_user_api_enabled%22%3Atrue%2C%22blue_business_profile_image_shape_enabled%22%3Atrue%2C%22immersive_video_status_linkable_timestamps%22%3Atrue%2C%22super_follow_exclusive_tweet_notifications_enabled%22%3Atrue%7D",
    }
    return sendAndroid("/graphql/iOA9WG49OYDPdIvJi4K7Yw/UserResultByIdQuery", params, oauth_token, token_secret)


def latest_timeline(oauth_token, token_secret, cursor=None):
    cursor_param = If (cursor is not None, f"cursor%22%3A%22{cursor}%22%2C%22", "")
    params = {
        "variables": f"%7B%22{cursor_param}includeTweetImpression%22%3Atrue%2C%22request_context%22%3A%22ptr%22%2C%22includeHasBirdwatchNotes%22%3Afalse%2C%22includeEditPerspective%22%3Afalse%2C%22includeEditControl%22%3Atrue%2C%22count%22%3A100%2C%22includeTweetVisibilityNudge%22%3Atrue%2C%22autoplay_enabled%22%3Atrue%7D",
        "features": "%7B%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22super_follow_badge_privacy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22super_follow_user_api_enabled%22%3Atrue%2C%22unified_cards_ad_metadata_container_dynamic_card_content_query_enabled%22%3Atrue%2C%22super_follow_tweet_api_enabled%22%3Atrue%2C%22articles_api_enabled%22%3Atrue%2C%22android_graphql_skip_api_media_color_palette%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22subscriptions_verification_info_enabled%22%3Atrue%2C%22blue_business_profile_image_shape_enabled%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22immersive_video_status_linkable_timestamps%22%3Atrue%2C%22super_follow_exclusive_tweet_notifications_enabled%22%3Atrue%7D",
    }
    return sendAndroid("/graphql/fk-JW3tHUsfC6mBcx0ea3Q/HomeTimelineLatest", params, oauth_token, token_secret)


def latest_timeline_web(oauth_token, token_secret, cursor=None):
    cursor_param = If (cursor is not None, f"cursor%22%3A%22{cursor}%22%2C%22", "")
    params = {
        "variables": f"%7B%22count%22%3A20%2C%22{cursor_param}includePromotedContent%22%3Atrue%2C%22latestControlAvailable%22%3Atrue%2C%22seenTweetIds%22%3A%5B%5D%7D",
        "features": "%7B%22profile_label_improvements_pcf_label_in_post_enabled%22%3Afalse%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22premium_content_api_read_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22responsive_web_grok_analyze_button_fetch_trends_enabled%22%3Afalse%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D",
    }
    return sendAndroid("/graphql/4U9qlz3wQO8Pw1bRGbeR6A/HomeLatestTimeline", params, oauth_token, token_secret)


def request_php(url, data=None):
    for attempt in range(5):
        try:
            if data != None:
                response = requests.post(PHP_URL + url + ".php", headers={"Content-Type": "application/json"}, data=json.dumps(data))
                return response
            else:
                response = requests.get(PHP_URL + url + ".php")
                return response.json()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 5 - 1:
                print(f"Retrying in {60} seconds...")
                time.sleep(60)
            else:
                print("All attempts failed.")
                return None


def tweet_by_oauth(payload):
    print("tweet at ", datetime.datetime.now())
    tweet_response = oauth1.post("https://api.twitter.com/2/tweets", json=payload, headers={"Content-Type": "application/json"})


twcount = 0  # 返信用アカウント振り分け用カウンター

def reply(text, rep_id):
    global twcount
    twcount += 1
    index = twcount % (len(rep_accounts) + 1)
    if index == len(rep_accounts):
        print(f"reply {main_account[0]} at ", datetime.datetime.now())
        response = create_tweet(text, main_account[1], main_account[2], rep_id)
        if "errors" in response:
            print(response)
    else:
        print(f"reply {rep_accounts[index][0]} at ", datetime.datetime.now())
        response = create_tweet(text, rep_accounts[index][1], rep_accounts[index][2], rep_id)
        if "errors" in response:
            print(response)
            response = create_tweet(text, main_account[1], main_account[2], rep_id)
            if "errors" in response:
                print(response)


idlist = []  # 返信済みのツイートID

def receive(reps):

    def get_kyui(pt):
        if pt < 500: rank = 'E'
        elif pt < 1000: rank = 'E+'
        elif pt < 1500: rank = 'D'
        elif pt < 2000: rank = 'D+'
        elif pt < 2500: rank = 'C'
        elif pt < 3000: rank = 'C+'
        elif pt < 3500: rank = 'B'
        elif pt < 4000: rank = 'B+'
        elif pt < 4500: rank = 'A'
        elif pt < 5000: rank = 'A+'
        elif pt < 5500: rank = 'S1'
        elif pt < 6000: rank = 'S2'
        elif pt < 6500: rank = 'S3'
        elif pt < 7000: rank = 'S4'
        elif pt < 7500: rank = 'S5'
        elif pt < 8000: rank = 'S6'
        elif pt < 8500: rank = 'S7'
        elif pt < 9000: rank = 'S8'
        elif pt < 9500: rank = 'S9'
        else: rank = 'RoR'
        return rank

    def get_rank(key, name):
        def s(key):
            return f"{round(d[key], 2):.2f}"

        if prepare_flag:
            return "ランキングは準備中です\\nしばらくお待ちください"
        if key in records_rank:
            d = records_rank[key]
            rep_text2 = If (d["now_pt"] != d["refer_pt"], f'\\n参考記録: {s("refer_pt")}', "")
            rank, rank2 = get_kyui(d["max_pt"]), get_kyui(d["now_pt"])
            return f"{name}\\n\\n級位: {rank}\\n　最高pt: {s('max_pt')}\\n　歴代: {d['max_pt_rank']} / {str(joined_num['max_pt_rank'])}\\n　現在pt: {s('now_pt')} ({rank2}帯)\\n　世界ランク: {d['now_pt_rank']} / {str(joined_num['now_pt_rank'])}{rep_text2}\\n1s以内出場数: {str(d['count'])}\\n自己ベスト: {d['best']} ({str(d['best_count'])}回)\\n戦績: 🥇×{str(d['f'])} 🥈×{str(d['s'])} 🥉×{str(d['t'])} 📋×{str(d['rankin'])}"
        return f"{name}\\n\\n最高pt: -\\n歴代: - / {str(joined_num['max_pt_rank'])}\\n現在pt: -\\n世界ランク: - / {str(joined_num['now_pt_rank'])}\\n1s以内出場数: 0\\n自己ベスト: -\\n戦績: 🥇×0 🥈×0 🥉×0 📋×0"

    def has_rank(key, name, data):
        """ランクを要求しているか判定"""
        """return ランク返信文章 or False"""

        text = data["full_text"].lower()
        mentions = data["entities"]["user_mentions"]
        for user in mentions:
            text = text.replace("@" + user["screen_name"].lower(), "")
        if any(x in text for x in ["ランク", "ﾗﾝｸ", "らんく", "rank", "ランキング", "ﾗﾝｷﾝｸﾞ"]):
            return get_rank(key, name)
        if any(x in text for x in ["順位", "じゅんい", "ジュンイ", "ｼﾞｭﾝｲ"]):
            return get_result(key, name)
        return False

    def get_result(key, name):
        """当日の結果返信文章生成"""

        previous = datetime.datetime.now() - datetime.timedelta(hours=TIME334[0], minutes=TIME334[1] - 1)
        if prepare_flag:
            return "ランキングは準備中です\\nしばらくお待ちください"
        if key in today_result:
            return f"{name}\\n\\n{previous.date().strftime('%Y/%m/%d')}の334結果\\nresult: +{today_result[key][1]} [sec]\\nrank: {str(today_result[key][0])} / {str(today_joined)}"
        return f"{name}\\n\\n{previous.date().strftime('%Y/%m/%d')}の334結果\\nresult: DQ\\nrank: DQ / {str(today_joined)}"

    def follow_request(data, mentions=[]):
        """フォローリクエスト"""
        """return フォローした or ランク返信文章 or False"""

        user = data["user"]
        user_id = user["id_str"]
        text = data["full_text"].lower()
        for mention in mentions:
            text = text.replace("@" + mention["screen_name"].lower(), "")
        if any(x in text for x in ["ふぉろー", "フォロー", "follow", "ふぉろば", "フォロバ"]):
            if any(x in text for x in ["してもいいですか", "しても大丈夫ですか"]):
                return False
            try:
                legacy = user
                if "following" not in legacy and "followed_by" not in legacy:
                    user_data = get_user(user_id, main_account[1], main_account[2])
                    legacy = user_data["data"]["user_result"]["result"]["legacy"]
                if "following" in legacy and legacy["following"]:
                    return "既にフォローしています"
                if "followed_by" in legacy and legacy["followed_by"]:
                    response = create_follow(user_id, main_account[1], main_account[2])
                    if "errors" in response:
                        return 'エラーが発生しました🙇\\n時間をおいてもう一度お試しください'
                    return "フォローしました"
                else:
                    return "334Rankerをフォローしてからお試しください"
            except Exception as e:
                traceback.print_exc()
                return 'エラーが発生しました🙇\\n時間をおいてもう一度お試しください'
        else:
            return has_rank(user_id, "@ " + user["screen_name"], data)
        
    def tweet_time(id_str):
        d = TweetIdTime(int(id_str))
        return f"ツイート時刻：{d.hour:02d}:{d.minute:02d}:{d.second:02d}.{int(d.microsecond / 1000):03d}"


    # follow_request -> has_rank -> get_rank -> get_result -> (tweet_time)
    global idlist
    rep_accounts_ids = [main_account[1].split("-")[0]] + [account[1].split("-")[0] for account in rep_accounts]
    for data in reps:
        user = data["user"]
        mentions = data["entities"]["user_mentions"]
        if user["id_str"] not in rep_accounts_ids and data["id_str"] not in idlist:
            rep_text = False
            idlist.append(data["id_str"])
            if "in_reply_to_status_id_str" not in data or data["in_reply_to_status_id_str"] == None:
                rep_text = follow_request(data, mentions)  # リプライ先がリプライでない場合 検索にかかったもの全て対象
                if not rep_text:
                    rep_text = tweet_time(data["id_str"])
            else:  # リプライ先がリプライの場合
                if data["in_reply_to_user_id_str"] in rep_accounts_ids:
                    rep_text = follow_request(data, mentions)  # Rankerへのリプライの場合
                else:  # Ranker以外へのリプライの場合
                    user_id = data["in_reply_to_user_id_str"]
                    text_range = data["display_text_range"]
                    flag = False
                    for user2 in mentions:
                        if user2["id_str"] in rep_accounts_ids and text_range[0] <= user2["indices"][0] and user2["indices"][1] <= text_range[1]:
                            flag = True
                    if flag:
                        user_name = "@ " + data["in_reply_to_screen_name"]
                        rep_text = has_rank(user_id, user_name, data)
                        if not rep_text:
                            rep_text = tweet_time(data["in_reply_to_status_id_str"])

            if rep_text:
                print(user["name"])
                threading.Thread(target=reply, args=(rep_text, data["id_str"],)).start()


def get_mention_from_notion(since, end):
    """通知欄からメンションを取得"""

    cursor = None

    def loop():
        nonlocal cursor
        screen_names = [main_account[0]] + [account[0] for account in rep_accounts]
        data = get_mentions(main_account[1], main_account[2])
        if "tweets" not in data["globalObjects"]: return
        tweets = data["globalObjects"]["tweets"]
        users = data["globalObjects"]["users"]
        out = []
        for key in tweets:
            tweet = tweets[key]
            if all(str not in tweet['full_text'].lower() for str in screen_names): continue
            if since <= TweetIdTime(int(tweet['id_str'])) < end:
                tweet["user"] = users[tweet["user_id_str"]]
                out.append(tweet)
        receive(out)
        instructions = data["timeline"]["instructions"]
        for instruction in instructions:
            if "addEntries" in instruction:
                cursor = instruction["addEntries"]["entries"][0]["content"]["operation"]["cursor"]["value"]
                break

    while datetime.datetime.now() < since: time.sleep(0.01)
    counter = 0
    while datetime.datetime.now() <= end:
        start = since + datetime.timedelta(seconds = counter * 5)
        while datetime.datetime.now() < start: time.sleep(0.01)
        threading.Thread(target=loop).start()
        counter += 1


def get_mention_from_search(since, end):
    """検索からメンションを取得"""

    def loop(text, index):
        oauth_token, token_secret = search_accounts[index]
        data = search_timeline(text, oauth_token, token_secret)
        if "errors" in data and "data" not in data:
            print(datetime.datetime.now(), f"Search Error occurred at index {index}", data)
            return
        instructions = data["data"]["search"]["timeline_response"]["timeline"]["instructions"]
        screen_names = [f"@{main_account[0]}"] + [f"@{account[0]}" for account in rep_accounts]
        out = []
        for instruction in instructions:
            if "entries" in instruction:
                entries = instruction["entries"]
            elif "entry" in instruction:
                entries = [instruction["entry"]]
            else:
                continue
            for entry in entries:
                if "promoted" in entry["entryId"] or "cursor" in entry["entryId"]: continue
                try:
                    if "result" not in entry["content"]["content"]["tweetResult"]: continue
                    res = entry["content"]["content"]["tweetResult"]["result"]
                    if "tweet" in res:
                        res = res["tweet"]
                    legacy = res["legacy"]
                    legacy["id_str"] = res["rest_id"]
                    if since <= TweetIdTime(int(legacy["id_str"])) <= end:
                        if not any(element in legacy["full_text"].lower() for element in screen_names): continue
                        legacy["user"] = res["core"]["user_result"]["result"]["legacy"]
                        out.append(legacy)
                except Exception as e:
                    traceback.print_exc()
        receive(out)


    text = f'@{main_account[0]} -filter:retweets -from:{main_account[0]} ' + " ".join([f"-from:{account[0]}" for account in rep_accounts])
    while datetime.datetime.now() < since: time.sleep(0.01)
    counter = 0
    rate = max(1, 15 * 60 / len(search_accounts) / 50)
    while datetime.datetime.now() <= end:
        start = since + datetime.timedelta(seconds = counter * rate)
        index = counter % len(search_accounts)
        while datetime.datetime.now() < start: time.sleep(0.01)
        threading.Thread(target=loop, args=(text, index,)).start()
        counter += 1


def make_world_rank():
    """級位ポイント計算"""

    def sort_and_rank(input, output, records):
        """ソートして順位をつける"""

        global joined_num
        sorted_items = sorted(records.items(), key=lambda item: item[1][input], reverse=True)
        current_rank = 1
        previous_value = None
        index = 0
        for i, (key, value) in enumerate(sorted_items):
            if value[input] == 0:
                records[key][output] = '-'
                continue
            index += 1
            if value[input] != previous_value: current_rank = index
            records[key][output] = str(current_rank)
            previous_value = value[input]
        joined_num[output] = index

    def time_to_point(date, result):
        """タイムをポイントに変換"""

        days = (datetime.datetime.now() - date).days
        b = 10000 * 2 ** (-10 * float(result))
        if days >= 30: b *= (91 - days) / 61
        return b

    user_data = defaultdict(lambda: {'valid': [], 'all': []})
    for entry in past_records:
        userid, date, value, source = entry
        transformed_value = time_to_point(date, value)
        user_data[userid]['all'].append(transformed_value)
        if source in clients: user_data[userid]['valid'].append(transformed_value)

    def get_top_10(values):
        top_values = sorted(values, reverse=True)[:10]
        while len(top_values) < 10:
            top_values.append(0)
        return top_values

    top_values = {}
    for userid, entries in user_data.items():
        top_valid_values = get_top_10(entries['valid'])
        top_all_values = get_top_10(entries['all'])
        top_values[userid] = {
            'valid': top_valid_values,
            'all': top_all_values
        }

    for id in records_rank:
        if id in top_values:
            records_rank[id]['now_pt'] = sum(top_values[id]['valid']) / 10
            if records_rank[id]['max_pt'] < records_rank[id]['now_pt']: records_rank[id]['max_pt'] = records_rank[id]['now_pt']
            records_rank[id]['refer_pt'] = sum(top_values[id]['all']) / 10
        else:
            records_rank[id]['now_pt'] = 0
            records_rank[id]['refer_pt'] = 0

    sort_and_rank('max_pt', 'max_pt_rank', records_rank)
    sort_and_rank('now_pt', 'now_pt_rank', records_rank)


def make_ranking(results_dict_arr, _driver):
    """当日分のランキングの作成"""

    prepare_flag2 = True

    def make_month_rank():
        month_record, month_source = {}, {}
        n = datetime.datetime.now()
        month_days = calendar.monthrange(n.year, n.month)[1]
        response = request_php('get')
        for record in response:
            record_time = datetime.datetime.strptime(record['date'], '%Y-%m-%d') + datetime.timedelta(hours=TIME334[0], minutes=TIME334[1])
            days = (datetime.datetime.now() - record_time).days
            if days < month_days and record['source'] in clients:
                id = record['userid']
                if id not in month_record:
                    month_record[id], month_source[id] = [], []
                pt = 10000 * 2 ** (-10 * float(record['result']))
                if len(month_record[id]) < 10:
                    month_record[id].append(pt)
                elif min(month_record[id]) < pt:
                    month_record[id].remove(min(month_record[id]))
                    month_record[id].append(pt)
                month_source[id].append(record['source'])

        month_data = []
        for id in month_record:
            month_data.append([id, sum(month_record[id]) / 10])
        sorted_items = sorted(month_data, key=lambda x: x[1], reverse=True)
        rankdata = []
        current_rank = 1
        previous_value = None
        index = 0
        for value in sorted_items:
            index += 1
            if index > 30: break
            if value[1] != previous_value: current_rank = index
            url = "https://api.x.com/graphql/LWxkCeL8Hlx0-f24DmPAJw/UserByRestId"
            params = {
                "variables": f'{{"userId":"{value[0]}"}}',
                "features": '{"hidden_profile_subscriptions_enabled":true,"profile_label_improvements_pcf_label_in_post_enabled":false,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"subscriptions_feature_can_gift_premium":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}'
            }
            counter = Counter(month_source[value[0]])
            headers = { "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA" }
            try:
                response = requests.get(url, params=params, headers=headers)
                legacy = response.json()['data']['user']['result']['legacy']
                name = legacy['name']
                if name == '': name = '@' + legacy['screen_name']
                rankdata.append([current_rank, legacy['profile_image_url_https'], legacy['name'], value[1], len(month_source[value[0]]), counter.most_common(1)[0][0]])
            except:
                rankdata.append([current_rank, '', 'unknown', value[1], len(month_source[value[0]]), counter.most_common(1)[0][0]])
            previous_value = value[1]

        _driver.get(HTML_URL2)
        wait = WebDriverWait(_driver, 20).until(EC.alert_is_present())
        Alert(_driver).accept()
        for _ in range(5):
            try:
                _driver.execute_script('document.getElementById("input").value = arguments[0]; start();', str(rankdata))
                wait = WebDriverWait(_driver, 20).until(EC.alert_is_present())
            except Exception as e:
                traceback.print_exc()
                _driver.get(HTML_URL2)
                time.sleep(1)
            else:
                Alert(_driver).accept()
                bin = _driver.execute_script('return window.res')
                print('GET IMG2')
                files = {
                    "media": base64.b64decode(bin)
                }
                upload_response = oauth1.post("https://api.twitter.com/2/media/upload", files=files)
                media_id = upload_response.json().get('id')
                payload = {
                    'text': "This month's top 30",
                    'media': {
                        'media_ids': [media_id]
                    }
                }
                print("POST RANK2 :")
                tweet_by_oauth(payload)
                _driver.quit()
                break

    def retweet(id, screen_name):
        """リツイート"""
        
        payload = {
            'text': "Today's winner https://x.com/" + screen_name + "/status/" + id
        }
        print("RETWEET :")
        tweet_by_oauth(payload)

    def make_img(tweets):
        """ランキング画像の生成とアップロード"""

        for _ in range(5):
            try:
                _driver.execute_script('document.getElementById("input").value = arguments[0]; start();', tweets)
                wait = WebDriverWait(_driver, 20).until(EC.alert_is_present())
            except Exception as e:
                traceback.print_exc()
                _driver.get(HTML_URL)
                time.sleep(1)
            else:
                Alert(_driver).accept()
                bin = _driver.execute_script('return window.res')
                print('GET IMG')
                files = {
                    "media": base64.b64decode(bin)
                }
                upload_response = oauth1.post("https://api.twitter.com/2/media/upload", files=files)
                media_id = upload_response.json().get('id')
                payload = {
                    'text': "Today's top 30",
                    'media': {
                        'media_ids': [media_id]
                    }
                }
                print("POST RANK :")
                tweet_by_oauth(payload)

                next_day = datetime.datetime.now() + datetime.timedelta(days=1)
                if next_day.day == 1:
                    while prepare_flag2:
                        time.sleep(1)
                    time.sleep(1)
                    make_month_rank()
                else:
                    _driver.quit()
                break

    tweet_from_id_gt = ''

    def tweet_from_id(tweet_id):

        nonlocal tweet_from_id_gt
        if tweet_from_id_gt == '':
            headers = { "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36" }
            response = requests.get("https://x.com/?mx=2", headers=headers)
            tweet_from_id_gt = re.findall(r'gt=(.*?);', response.text)[0]
        
        params = copy.deepcopy(request_body['TweetResultByRestId'])
        params['variables']['tweetId'] = tweet_id
        for key in params:
            params[key] = json.dumps(params[key])
        headers = {
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "x-guest-token": tweet_from_id_gt
        }
        try:
            response = requests.get(request_body['TweetResultByRestId_url'], params=params, headers=headers)
            return response.json()['data']['tweetResult']['result']['source']
        except:
            traceback.print_exc()
            return 'undefined'


    #生データを扱いやすい形に変換

    global records_rank, today_result, today_joined, prepare_flag
    now = datetime.datetime.now()
    today_str = now.date().strftime('%Y-%m-%d')
    time_334 = datetime.datetime.combine(now.date(), datetime.time(TIME334[0], TIME334[1]))
    joined_users = ['1173558244607852545']
    results_for_img = []
    update_records_rank = []
    update_past_records = []
    results_dict_arr = sorted(results_dict_arr, key=lambda x: int(x['id_str']))
    current_rank = 1
    today_joined = 0
    previous_value = None
    for item in results_dict_arr:
        if item['text'] == KEYWORD and item['user']['id_str'] not in joined_users:
            joined_users.append(item['user']['id_str'])
            result_time = (TweetIdTime(int(item['id_str'])) - time_334).total_seconds()
            if 0 <= result_time < 1:
                result_str = '{:.3f}'.format(result_time)

                img_src = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
                if item['user']['profile_image_url_https'] != '': img_src = item['user']['profile_image_url_https']

                if item['source'] == 'undefined': item['source'] = tweet_from_id(item['id_str'])
                match = re.search(r'<a[^>]*>([^<]*)</a>', item['source'])
                source = match.group(1) if match else item['source']

                id = item['user']['id_str']

                results_for_img.append([
                    img_src,
                    item['user']['name'],
                    result_str,
                    source,
                    item['id_str'],
                    '@' + item['user']['screen_name'],
                    id
                ])

                today_joined += 1
                if result_str != previous_value: current_rank = today_joined
                previous_value = result_str
                today_result[id] = [current_rank, result_str]
                if id not in records_rank:
                    records_rank[id] = {
                        'best': result_str,
                        'best_count': 0,
                        'max_pt': 0.0,
                        'count': 0,
                        'f': 0,
                        's': 0,
                        't': 0,
                        'rankin': 0
                    }
                records_rank[id]['count'] += 1
                if result_time < float(records_rank[id]['best']):
                    records_rank[id]['best'] = result_str
                    records_rank[id]['best_count'] = 1
                elif result_time == float(records_rank[id]['best']):
                    records_rank[id]['best_count'] += 1
                match current_rank:
                    case 1:
                        records_rank[id]['f'] += 1
                        threading.Thread(target=retweet, args=(item['id_str'], item['user']['screen_name'],)).start()
                    case 2: records_rank[id]['s'] += 1
                    case 3: records_rank[id]['t'] += 1
                if current_rank <= 30: records_rank[id]['rankin'] += 1

                update_list = list(records_rank[id].values())[:8]
                update_list.insert(0, id)
                update_records_rank.append(update_list)

                past_records.append([id, now, result_str, source])
                update_past_records.append([id, today_str, result_str, source]) #JSONにできるよう文字列に

    print(str(results_for_img))
    threading.Thread(target=make_img, args=(str(results_for_img),)).start()
    
    make_world_rank()
    for update_record in update_records_rank:
        update_record[3] = records_rank[update_record[0]]['max_pt']

    prepare_flag = False

    response = request_php('add_rank', update_records_rank)
    print("Response:", response.status_code, response.text)
    response = request_php('add', update_past_records)
    print("Response:", response.status_code, response.text)

    prepare_flag2 = False


def get334(oauth_token, token_secret, search_only, func):
    now = datetime.datetime.now()
    time1 = datetime.datetime(now.year, now.month, now.day, TIME334[0], TIME334[1], 59) - datetime.timedelta(minutes=1)
    time2 = datetime.datetime(now.year, now.month, now.day, TIME334[0], TIME334[1], 1)
    out = []
    out2 = []
    end_flag = True

    count = 0
    def final():
        nonlocal count, out2, end_flag
        count += 1
        if count >= If (search_only, 1, 3):
            out.sort(key=lambda x: x['index'])
            ids = []
            for item in out:
                if item['id_str'] not in ids:
                    out2.append(item)
                    ids.append(item['id_str'])
            print("GET334 COMPLETE")
            end_flag = False


    def add_arr(res, arr, entry_id):
        legacy = res['legacy']
        if TweetIdTime(int(legacy['id_str'])) < time1:
            if "home" in entry_id:
                return True
            else:
                final()
                return False

        legacy['text'] = legacy['full_text']
        if legacy['text'] != KEYWORD: return True

        legacy['source'] = res['source']
        legacy['index'] = (int(legacy['id_str']) >> 22) + 1288834974657
        legacy['user'] = res['core']['user_results']['result']['legacy']
        legacy['user']['id_str'] = legacy['user_id_str']
        arr.append(legacy)
        return True


    def get_timeline(cursor = None):
        nonlocal out
        print("GET334 get_timeline  search_only:", search_only)
        try:
            data = latest_timeline_web(oauth_token, token_secret, cursor)
            entries = data['data']['home']['home_timeline_urt']['instructions'][0]['entries']

            for entry in entries:
                entry_id = entry['entryId']
                if "bottom" in entry_id:
                    get_timeline(entry['content']['value'])
                    return
                
                try:
                    if "promoted" in entry_id or "cursor" in entry_id: continue
                    if "home" in entry_id:
                        res = entry['content']['items'][0]['item']['itemContent']['tweet_results']['result']
                    else:
                        res = entry['content']['itemContent']['tweet_results']['result']
                    if "tweet" in res:
                        res = res['tweet']

                    if not add_arr(res, out, entry_id): return

                except Exception as e:
                    print(e)

            final()

        except Exception as e:
            traceback.print_exc()
            final()


    def get_search(cursor = None):
        nonlocal out
        print("GET334 get_search  search_only:", search_only)
        screen_names = f'-from:{main_account[0]} ' + ' '.join([f'-from:{account[0]}' for account in rep_accounts])
        text = f"{KEYWORD} -filter:retweets -filter:quote {screen_names} since:{time1.strftime('%Y-%m-%d_%H:%M:%S_JST')} until:{time2.strftime('%Y-%m-%d_%H:%M:%S_JST')}"
        try:
            flag = True
            data = search_timeline_web(text, oauth_token, token_secret, cursor)
            instructions = data['data']['search_by_raw_query']['search_timeline']['timeline']['instructions']

            for instruction in instructions:
                entries = []
                if 'entries' in instruction:
                    entries = instruction['entries']
                elif 'entry' in instruction:
                    entries = [instruction['entry']]
                else:
                    continue

                for entry in entries:
                    entry_id = entry['entryId']
                    if "bottom" in entry_id:
                        if flag:
                            final()
                        else:
                            get_search(entry['content']['value'])
                        return
                    
                    try:
                        if "promoted" in entry_id or "cursor" in entry_id :
                            continue

                        flag = False
                        res = entry['content']['itemContent']['tweet_results']['result']
                        if "tweet" in res:
                            res = res['tweet']
                        if not add_arr(res, out, entry_id): return

                    except Exception as e:
                        print(e)
                    
            final()

        except Exception as e:
            traceback.print_exc()
            final()


    get_time = time2 + datetime.timedelta(seconds=1)
    while datetime.datetime.now() < get_time: time.sleep(0.01)
    print("GET334 START  search_only:", search_only)
    if search_only:
        threading.Thread(target = get_search).start()
    else:
        threading.Thread(target = get_timeline).start()
        threading.Thread(target = get_search).start()
        time.sleep(2)
        threading.Thread(target = get_search).start()
    while end_flag:
        time.sleep(1)
    func(out2)


def main334(_driver):

    result = []
    count = 0
    def func(arr):
        nonlocal result, count
        result = result + arr
        count += 1
        if count >= 1 + len(rep_accounts):
            make_ranking(result, _driver)

    threading.Thread(target=get334, args=(main_account[1], main_account[2], False, func,)).start()
    for rep_account in rep_accounts:
        threading.Thread(target=get334, args=(rep_account[1], rep_account[2], True, func,)).start()


def notice():
    global today_result, prepare_flag
    today = datetime.datetime.now().date()
    notice_time = datetime.datetime.combine(today, datetime.time(TIME334[0], TIME334[1])) - datetime.timedelta(minutes=2)
    while datetime.datetime.now() < notice_time: time.sleep(5)
    today_result = {}
    prepare_flag = True
    print("NOTICE :")
    threading.Thread(target=tweet_by_oauth, args=({'text': f"334観測中 ({today.strftime('%Y/%m/%d')})"},)).start()
    _driver = {}
    
    for _ in range(5):
        try:
            options=Options()
            #options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument('--disable-dev-shm-usage')
            _driver = webdriver.Chrome(options = options)
            _driver.set_window_size(589, 1)
            _driver.get(HTML_URL)
            wait = WebDriverWait(_driver, 20).until(EC.alert_is_present())
            Alert(_driver).accept()
        except Exception as e:
            traceback.print_exc()
            time.sleep(2)
        else:
            main334(_driver)
            break


def main():

    now = datetime.datetime.now()
    base_time = datetime.datetime(now.year, now.month, now.day, TIME334[0], TIME334[1], 0) - datetime.timedelta(minutes=34)

    times = []
    for i in range(6):
        start_time = base_time + datetime.timedelta(hours=i * 4)
        end_time = start_time + datetime.timedelta(hours=4)
        times.append([start_time, end_time])

    times[-1][1] = base_time + datetime.timedelta(days=1)
    times.append([base_time + datetime.timedelta(days=1), base_time + datetime.timedelta(days=1)])

    for i in range(len(times)):
        if now < times[i][0]:
            start_time = times[i][0]
            end_time = times[i][1]
            if len(sys.argv) != 1:
                print('TEST MODE')
                start_time = '???'
                end_time = times[i][0]
            print(start_time, end_time)
            
            global past_records, today_result, today_joined, records_rank
            today_unsorted = []
            response = request_php('get')
            for record in response:
                record_time = datetime.datetime.strptime(record['date'], '%Y-%m-%d') + datetime.timedelta(hours=TIME334[0], minutes=TIME334[1])
                days = (datetime.datetime.now() - record_time).days
                if days <= 91: past_records.append([record['userid'], record_time, record['result'], record['source']])
                if days == 0: today_unsorted.append([record['userid'], record['result']])
            today_unsorted = sorted(today_unsorted, key=lambda x: float(x[1]))
            current_rank = 1
            today_joined = 0
            previous_value = None
            for record in today_unsorted:
                today_joined += 1
                if record[1] != previous_value: current_rank = today_joined
                today_result[record[0]] = [current_rank, record[1]]
                previous_value = record[1]
            
            response = request_php('get_rank')
            for record in response:
                id = record['userid']
                del record['userid']
                record['max_pt'] = float(record['max_pt'])
                records_rank[id] = {key: int(value) if key not in ['best', 'max_pt'] else value for key, value in record.items()}

            make_world_rank()
            print('LOADED RANK')
            

            if len(sys.argv) != 1:
                start_time = datetime.datetime.now().replace(microsecond = 0) + datetime.timedelta(seconds=2)
            print('START')
            
            if len(sys.argv) != 1 and sys.argv[1] == "recount":
                print('RECOUNT MODE')
                notice()
                
            else:
                threading.Thread(target = get_mention_from_notion, args=(start_time, end_time,)).start()
                threading.Thread(target = get_mention_from_search, args=(start_time, end_time,)).start()
                
                if start_time < datetime.datetime(now.year, now.month, now.day, TIME334[0], TIME334[1], 0) < end_time:
                    print('334MODE')
                    notice()
                
            break

main()
         
