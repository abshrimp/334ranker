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
    return sendAndroid("/1.1/friendships/create.json", payload, oauth_token, token_secret, "POST")


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
        'features': "%7B%22rweb_video_screen_enabled%22%3Afalse%2C%22profile_label_improvements_pcf_label_in_post_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22premium_content_api_read_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22responsive_web_grok_analyze_button_fetch_trends_enabled%22%3Afalse%2C%22responsive_web_grok_analyze_post_followups_enabled%22%3Atrue%2C%22responsive_web_jetfuel_frame%22%3Afalse%2C%22responsive_web_grok_share_attachment_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22responsive_web_grok_show_grok_translated_post%22%3Afalse%2C%22responsive_web_grok_analysis_button_from_backend%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_grok_image_annotation_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
    }
    return sendAndroid('/graphql/fL2MBiqXPk5pSrOS5ACLdA/SearchTimeline', params, oauth_token, token_secret)


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
        'features': "%7B%22rweb_video_screen_enabled%22%3Afalse%2C%22profile_label_improvements_pcf_label_in_post_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22premium_content_api_read_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22responsive_web_grok_analyze_button_fetch_trends_enabled%22%3Afalse%2C%22responsive_web_grok_analyze_post_followups_enabled%22%3Atrue%2C%22responsive_web_jetfuel_frame%22%3Afalse%2C%22responsive_web_grok_share_attachment_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22responsive_web_grok_show_grok_translated_post%22%3Afalse%2C%22responsive_web_grok_analysis_button_from_backend%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_grok_image_annotation_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
    }
    return sendAndroid('/graphql/nMyTQqsJiUGBKLGNSQamAA/HomeLatestTimeline', params, oauth_token, token_secret)

def get_user_by_id(id, oauth_token, token_secret):
    params = {
        'variables': "%7B%22userId%22%3A%22" + id + "%22%7D",
        'features': "%7B%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22profile_label_improvements_pcf_label_in_post_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22responsive_web_twitter_article_notes_tab_enabled%22%3Atrue%2C%22subscriptions_feature_can_gift_premium%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D"
    }
    return sendAndroid('/graphql/WJ7rCtezBVT6nk6VM5R8Bw/UserByRestId', params, oauth_token, token_secret)
    
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
        data = get_mentions(main_account[1], main_account[2], cursor)
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
            counter = Counter(month_source[value[0]])
            try:
                response = get_user(value[0], main_account[1], main_account[2])
                legacy = response['data']['user']['result']['legacy']
                name = legacy['name']
                if name == '': name = '@' + legacy['screen_name']
                rankdata.append([current_rank, legacy['profile_image_url_https'], legacy['name'], value[1], len(month_source[value[0]]), counter.most_common(1)[0][0]])
                time.sleep(1)
            except:
                rankdata.append([current_rank, '', 'unknown', value[1], len(month_source[value[0]]), counter.most_common(1)[0][0]])
            previous_value = value[1]

        print(str(rankdata))
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
                upload_response = oauth1.post("https://upload.twitter.com/1.1/media/upload.json", files=files)
                media_id = upload_response.json()["media_id_string"]
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
                upload_response = oauth1.post("https://upload.twitter.com/1.1/media/upload.json", files=files)
                try:
                    media_id = upload_response.json()["media_id_string"]
                except ValueError:
                    print("JSON decode error:", upload_response.status_code, upload_response.text)
                    make_month_rank()
                    return
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

    results_for_img = [['https://pbs.twimg.com/profile_images/1810684511942057984/Rb6SuXb8_normal.jpg', 'いーるけん', '0.005', 'Twitter Web App', '1928520281770889711', '@Eel_Ken', '935502914029731841'], ['https://pbs.twimg.com/profile_images/1906904444136312832/3YGUlJWJ_normal.jpg', 'お茶(きょ〜じゅ)', '0.015', 'Twitter for iPhone', '1928520281812774965', '@Kyojyunokimot', '1480898324643577863'], ['https://pbs.twimg.com/profile_images/1893252144075063296/AF5N4BW5_normal.jpg', '@Umibe.', '0.016', 'Twitter for Android', '1928520281816969641', '@umibejin_k', '1797913362661294080'], ['https://pbs.twimg.com/profile_images/1909049048683941889/HhY2WW8r_normal.jpg', 'まこと', '0.016', 'Twitter for iPhone', '1928520281817231840', '@TNyusei223742', '1909048195507974144'], ['https://pbs.twimg.com/profile_images/1270727849700294661/EahcJ0DW_normal.jpg', 'きゃくと', '0.024', 'Twitter Web App', '1928520281850794175', '@kyakt0', '1041337350041681921'], ['https://pbs.twimg.com/profile_images/1907870176357580800/Z1xvawWS_normal.jpg', 'しゅーどん1ごう', '0.026', 'Twitter Web App', '1928520281859273063', '@shuudonn', '971970443455246337'], ['https://pbs.twimg.com/profile_images/1690219713052413952/CBh3Prda_normal.jpg', 'すびあ', '0.028', 'Twitter for iPad', '1928520281867362361', '@Air2_LOVE', '1295280723499216897'], ['https://pbs.twimg.com/profile_images/1907270101302419456/KnkrrujW_normal.jpg', '윤승', '0.039', 'Twitter for iPhone', '1928520281913425966', '@SEUNG_QS', '1440296934'], ['https://pbs.twimg.com/profile_images/1653687014947176448/pHUFvfhM_normal.jpg', 'バラン', '0.042', 'Twitter Web App', '1928520281926128062', '@baran5144347080', '1653686759677624320'], ['https://pbs.twimg.com/profile_images/1877073803047743489/eofSFRit_normal.jpg', 'あじらす', '0.045', 'Twitter for iPhone', '1928520281938608329', '@Ajirasu1127', '1747598951526830080'], ['https://pbs.twimg.com/profile_images/1925794348047728640/bz9byAnN_normal.jpg', '7-17🦊', '0.055', 'Twitter for iPhone', '1928520281980633569', '@0824_no_Seras', '1815746497469935616'], ['https://pbs.twimg.com/profile_images/1862156507489394688/bAYBOi0W_normal.jpg', 'SugerBoy@心で工学', '0.061', 'Twitter Web App', '1928520282005975257', '@Suger_nitech', '1632771849544425472'], ['https://pbs.twimg.com/profile_images/1900893596779507714/G-R2moRH_normal.jpg', '限界まで足掻いた人生', '0.062', 'Twitter for iPhone', '1928520282009903276', '@genkai_uts1', '1733703776928980992'], ['https://pbs.twimg.com/profile_images/1768293753268346880/VNo1G1lz_normal.jpg', '始発快速3821M', '0.065', 'Twitter Web App', '1928520282022486265', '@Rapid_3821M', '1373177377237262340'], ['https://pbs.twimg.com/profile_images/1904858258231508992/ijr6Vy5o_normal.jpg', 'あおたく', '0.068', 'Twitter Web App', '1928520282035179554', '@uxlpp', '1796825765692268544'], ['https://pbs.twimg.com/profile_images/1906946412207841280/otm5TDa__normal.jpg', '愛葉🐧💕', '0.069', 'Twitter for iPhone', '1928520282039325182', '@Loveleaf0622', '1645807110461214723'], ['https://pbs.twimg.com/profile_images/1724683320188186624/SpPyAuwI_normal.png', 'おのたかし（めっぽうきさく）', '0.071', 'Twitter for iPhone', '1928520282047652187', '@onotakashi', '106727219'], ['https://pbs.twimg.com/profile_images/1921590494976684032/p4R43dOJ_normal.jpg', '十六夜', '0.083', 'Twitter for Android', '1928520282098004209', '@hu_1zay01', '1898224587990798336'], ['https://pbs.twimg.com/profile_images/1747538735741419520/U_8ar2hI_normal.jpg', 'えら釘数学ららじばら', '0.085', 'Twitter Web App', '1928520282106638359', '@swimming_year', '1654899695280623616'], ['https://pbs.twimg.com/profile_images/1904755515206623232/JG4jppG-_normal.jpg', 'さんせっとぐろう', '0.094', 'Twitter for iPhone', '1928520282144153912', '@himaja____', '1507517971736166403'], ['https://pbs.twimg.com/profile_images/1327372430302531589/rBwGMftz_normal.jpg', 'し～まる', '0.095', 'Twitter Web App', '1928520282148389030', '@seamaru_pro', '977008069119901696'], ['https://pbs.twimg.com/profile_images/1797637008090890240/lfbZLeA__normal.jpg', 'わどわど', '0.100', 'Twitter for iPhone', '1928520282169552938', '@wado_8', '1729843579135385600'], ['https://pbs.twimg.com/profile_images/1902239567102844928/zHaMJ4yw_normal.jpg', '学歴浪だりんぐ', '0.104', 'Twitter for Android', '1928520282186330374', '@rondal_04', '1836223002838732802'], ['https://pbs.twimg.com/profile_images/1800827861642969088/nAtBkZ3z_normal.jpg', 'たすあいらぁ =TAS= IsLa.', '0.109', 'Twitter for iPhone', '1928520282207113691', '@IQ465', '3167571098'], ['https://pbs.twimg.com/profile_images/1918910840708968448/q5m4U3S5_normal.jpg', 'ぱこっ多浪', '0.112', 'Twitter Web App', '1928520282219884974', '@no_friends_rou', '1910810622398459904'], ['https://pbs.twimg.com/profile_images/1845570939775594496/W1_BZ0mX_normal.jpg', 'ちょこ', '0.131', 'Twitter for iPhone', '1928520282299371811', '@jjeicne', '1664942160993738754'], ['https://pbs.twimg.com/profile_images/1809029614230253571/xspA6laC_normal.jpg', 'エクセキューターれいひ❄', '0.136', 'Twitter for Android', '1928520282320548127', '@reifwia_bwp', '1250649243917770752'], ['https://pbs.twimg.com/profile_images/1909967059326582784/xtAoeRkp_normal.jpg', 'たかはし（23）🎖️', '0.141', 'Twitter Web App', '1928520282341298671', '@tktk1807', '1572242187219501059'], ['https://pbs.twimg.com/profile_images/1805599911121240064/ujF3hV1C_normal.jpg', 'てん', '0.143', 'Twitter for iPhone', '1928520282349727786', '@tenzehn_', '1772992889372766208'], ['https://pbs.twimg.com/profile_images/1893185859765039104/buQUUsmo_normal.jpg', 'う', '0.147', 'Twitter Web App', '1928520282366685376', '@Wny_3', '4113094998'], ['https://pbs.twimg.com/profile_images/1711678969144311808/zhbHQOGn_normal.jpg', 'cl', '0.180', 'Twitter for iPhone', '1928520282505204062', '@clsmm2', '1683300704155467776'], ['https://pbs.twimg.com/profile_images/847720699863093248/IxomgF0X_normal.jpg', 'へいたく', '0.185', 'Twitter for iPhone', '1928520282525888970', '@heitaku_', '623335558'], ['https://pbs.twimg.com/profile_images/1915449238131269638/WqS5FgyA_normal.jpg', '가로쉬세로쉬연구소', '0.195', 'Twitter Web App', '1928520282568069425', '@fundamental_of', '1478510830836920320'], ['https://pbs.twimg.com/profile_images/1770076875630809088/jE_umPRg_normal.jpg', 'いろ', '0.201', 'Twitter for iPhone', '1928520282592907332', '@ir_025', '1759232154435989504'], ['https://pbs.twimg.com/profile_images/1924726119074562049/mbU6aUjK_normal.jpg', 'ねむふる', '0.210', 'Twitter for iPhone', '1928520282630689022', '@unrunnuh', '1666088289089261572'], ['https://pbs.twimg.com/profile_images/1585189734791360512/gAMS5HCt_normal.jpg', 'KtaK', '0.213', 'Twitter Web App', '1928520282643308545', '@KtaK721', '1585189460815204353'], ['https://pbs.twimg.com/profile_images/1923031538498695168/FisWtc_G_normal.jpg', '爆泣きひよこ', '0.215', 'Twitter for iPhone', '1928520282651623446', '@halstakeomu0902', '1908192290151219200'], ['https://pbs.twimg.com/profile_images/1906905062406082560/KVN4MMEA_normal.jpg', 'ハム大のありす', '0.216', 'Twitter for iPhone', '1928520282655932431', '@hamualice', '1773885631917400064'], ['https://pbs.twimg.com/profile_images/1913619152243412992/n75t-9KI_normal.jpg', 'だい', '0.218', 'Twitter Web App', '1928520282664247321', '@Ou42OTmFFGLTPoi', '841948919642902528'], ['https://pbs.twimg.com/profile_images/1919347459291328512/b2BcPY6s_normal.jpg', 'エンジェルジョーク', '0.225', 'Twitter for Android', '1928520282693574824', '@angeljoke', '161871065'], ['https://pbs.twimg.com/profile_images/1924448071427162112/GBMzMjNt_normal.jpg', 'たくてぃー', '0.241', 'Twitter for iPhone', '1928520282760790349', '@takty_1438', '1898622339845419008'], ['https://pbs.twimg.com/profile_images/1824129432023601152/_JtKPyWl_normal.jpg', '明治大学334サークル', '0.242', 'Twitter for iPhone', '1928520282764869760', '@meiji_334', '1824128548745142272'], ['https://pbs.twimg.com/profile_images/1293089491855400961/o__W9b-z_normal.jpg', '農林漁業用揮発油税財源身替農道', '0.257', 'Twitter for iPhone', '1928520282827858429', '@bZYiPrp2sr4oTOQ', '1260404747166605314'], ['https://pbs.twimg.com/profile_images/1905233017574137856/5ceIEy5G_normal.jpg', 'するめ', '0.258', 'Twitter Web App', '1928520282832077162', '@SRM_108', '1904505214021009409'], ['https://pbs.twimg.com/profile_images/1876992348099575808/V3qbAp69_normal.jpg', 'cipher', '0.260', 'Twitter Web App', '1928520282840379598', '@cipher703516247', '1655909210184617987'], ['https://pbs.twimg.com/profile_images/1927785254003339264/IkQtQ2ac_normal.jpg', 'ことねﾁｬ❕', '0.279', 'Twitter for iPhone', '1928520282920079535', '@Hiy95_ri', '1926213193887543296'], ['https://pbs.twimg.com/profile_images/1690013076727234560/1glnK-Kw_normal.jpg', 'あはあさらた', '0.311', 'Twitter Web App', '1928520283054285117', '@1tlY5v2lGE2NNTr', '1600126054194360321'], ['https://pbs.twimg.com/profile_images/1900170704974479360/0VfTCx5z_normal.jpg', '努力不足の女々しいクズ(にしんぱい)', '0.319', 'Twitter Web App', '1928520283087925264', '@kirby_love828', '1516338052423032837'], ['https://pbs.twimg.com/profile_images/1923747583450570753/UJGgYdrM_normal.jpg', 'まる🍙(曇のち曇🌥️)ご依頼ぼしゅ', '0.331', 'Twitter for iPhone', '1928520283138256965', '@Rice__Maru', '1415653640807751680'], ['https://pbs.twimg.com/profile_images/1878890588663345152/gFP7L8jH_normal.jpg', 'とも❄', '0.335', 'Twitter Web App', '1928520283155214656', '@Liyna912', '1223941234630115328'], ['https://pbs.twimg.com/profile_images/1914184570842537984/INOfMdy__normal.jpg', '鏡にーれ', '0.349', 'Twitter for Android', '1928520283213709704', '@Nire_Kagami', '1841712660670513155'], ['https://pbs.twimg.com/profile_images/1928517756468502529/sCjJdhcv_normal.jpg', '小小藍白@MMFC', '0.353', 'Twitter for Android', '1928520283230543980', '@sakuyayorunashi', '966607944262459392'], ['https://pbs.twimg.com/profile_images/1923756643788947456/GuTg_qLg_normal.jpg', '甘食トロピカルファンタジー(ななㄘʓ\u200e〜ドウㄘʓ\u200e〜ｶﾛㄘʓ\u200e〜)', '0.372', 'Twitter for iPhone', '1928520283310182564', '@amsk_amazing', '1858542903896977409'], ['https://pbs.twimg.com/profile_images/1724351248739229696/gzKJfxD8_normal.jpg', '𓂸 → 𓂹 → 𓂺 ࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰ ࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰࣰ', '0.386', 'Twitter for iPhone', '1928520283368923259', '@bot_n_i_k_i', '1516057772991053824'], ['https://pbs.twimg.com/profile_images/1155986875871461377/tZv-ti62_normal.png', 'Raspel(ラスペル)', '0.390', 'Twitter for Android', '1928520283385901089', '@raspel_balma', '154586655'], ['https://pbs.twimg.com/profile_images/1770446033061040128/EAI7GyDq_normal.jpg', '緒山まひろぅ', '0.395', 'Twitter for iPhone', '1928520283406684620', '@mahiro_ronin', '1043840848650072066'], ['https://pbs.twimg.com/profile_images/1881120093146607616/H8dGeDbk_normal.jpg', 'わず', '0.399', 'Twitter for iPhone', '1928520283423650177', '@was_handai', '1860464921240371200'], ['https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', '競馬すき', '0.406', 'Twitter for iPhone', '1928520283452784854', '@keibasukiiiiiii', '1783074592900452352'], ['https://pbs.twimg.com/profile_images/1899054983661977600/cLzJK4rz_normal.jpg', 'おまどぅー', '0.415', 'Twitter for Android', '1928520283490758911', '@omadouma1001', '1899053275091226624'], ['https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', 'yamada4649', '0.425', 'Twitter Web App', '1928520283532484728', '@yamada4649ver1', '2713779072'], ['https://pbs.twimg.com/profile_images/1917852226166616064/Gae1YPZQ_normal.jpg', '黄金豆次郎', '0.431', 'Twitter for Android', '1928520283557650705', '@mamemame_labo', '1900135369615826944'], ['https://pbs.twimg.com/profile_images/1919764205198364672/Es6xLR1-_normal.jpg', 'みんみんぜみ', '0.433', 'Twitter for iPhone', '1928520283566010666', '@miinnmiinnzemii', '1919762931753046016'], ['https://pbs.twimg.com/profile_images/1921301710020198400/gpskbYjM_normal.jpg', 'あかにし州', '0.433', 'Twitter for iPhone', '1928520283566256472', '@akanicity', '1921301392842747904'], ['https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', 'Me', '0.443', 'Twitter for iPhone', '1928520283607965720', '@MemexxX05', '1918659800533176320'], ['https://pbs.twimg.com/profile_images/3514487404/43c39408cdb111ec0532a0a1303e8eab_normal.gif', 'しずくβ', '0.444', 'Twitter Web App', '1928520283612393795', '@siz33', '383311855'], ['https://pbs.twimg.com/profile_images/1739299926553829376/zgzWC1yL_normal.jpg', '〒Ｔク', '0.449', 'Twitter Web App', '1928520283633148144', '@n_TR05', '985763706830077952'], ['https://pbs.twimg.com/profile_images/1923675455414009856/ivv6Al34_normal.jpg', 'かズMAX｜6/1 J1#19 vs横浜FC @埼スタ', '0.460', 'Twitter for iPhone', '1928520283679342793', '@Kazumax_0125', '919556253797326848'], ['https://pbs.twimg.com/profile_images/1879855122454593536/wn63VPm__normal.jpg', 'No|く○', '0.466', 'Twitter for Android', '1928520283704434849', '@4meiatowazuka', '1833019453120094208'], ['https://pbs.twimg.com/profile_images/1883435200027455489/XWQwzjGN_normal.jpg', 'てん', '0.477', 'Twitter for Android', '1928520283750551721', '@li6qr4', '1882783254312628224'], ['https://pbs.twimg.com/profile_images/1926308416839979009/POfDiPzL_normal.jpg', '名前募集バーガー', '0.494', 'Twitter for iPhone', '1928520283821904258', '@st402nd4', '1730641844416245760'], ['https://pbs.twimg.com/profile_images/1915708295840751619/XNKeZ7p4_normal.jpg', '仮浪', '0.495', 'Twitter for iPhone', '1928520283826110501', '@karoh_nin', '1883196143062171648'], ['https://pbs.twimg.com/profile_images/1898789543878500352/sEbjAnUT_normal.jpg', 'きな', '0.545', 'Twitter for iPhone', '1928520284035752347', '@mochikinako00', '1593197876603420673'], ['https://pbs.twimg.com/profile_images/1920386751803068417/bK5ZqPD9_normal.jpg', 'チ。', '0.585', 'Twitter for iPhone', '1928520284203561279', '@1killxx_', '1653106158868234241'], ['https://pbs.twimg.com/profile_images/1801224449913704448/wARvt64B_normal.jpg', '_', '0.601', 'Twitter for iPhone', '1928520284270678430', '@___v4qn', '1212050535655723009'], ['https://pbs.twimg.com/profile_images/1882954696127881216/w92zMZhv_normal.jpg', '生涯収支マイナス ｻﾝ', '0.627', 'Twitter for iPhone', '1928520284379951293', '@rumi_otaku', '1028166407651975178'], ['https://pbs.twimg.com/profile_images/772845398805229570/4xCUQ9oS_normal.jpg', 'KING', '0.634', 'Twitter for iPhone', '1928520284409074002', '@popnneu', '320098147'], ['https://pbs.twimg.com/profile_images/1188789134665474048/-h7so-kD_normal.jpg', 'コドモ', '0.667', 'Twitter for Android', '1928520284547473577', '@Kodomo913', '862000370'], ['https://pbs.twimg.com/profile_images/1539190382910914561/FCcSntgp_normal.jpg', 'ふゆなさん❄️', '0.680', 'Twitter for iPhone', '1928520284602048840', '@Fuyu7a', '1052442615814258689'], ['https://pbs.twimg.com/profile_images/1484540746921553923/0VVi0_-b_normal.jpg', 'す', '0.693', 'Twitter for Android', '1928520284656521402', '@K3qCBWSkHSIrcsl', '1484540452259135490'], ['https://pbs.twimg.com/profile_images/1902231176263487488/3jXB5Ia2_normal.jpg', 'あまりんご', '0.695', 'Twitter for iPhone', '1928520284664930449', '@Ama__1221', '1706278770926338048'], ['https://pbs.twimg.com/profile_images/1918494665449586690/sWi6LClX_normal.jpg', 'とけないぱん', '0.728', 'Twitter for Android', '1928520284803362923', '@Oishisoupan', '1918492942001684480'], ['https://pbs.twimg.com/profile_images/1854899049037778944/jOIZdfx1_normal.jpg', 'ちょーた', '0.739', 'Twitter for iPhone', '1928520284849451040', '@chouta_1221_', '1751247433030656000'], ['https://pbs.twimg.com/profile_images/1912693306083143682/Nlpf86OA_normal.jpg', 'オワタ', '0.739', 'Twitter for iPhone', '1928520284849713654', '@owata083', '1420008689545531394'], ['https://pbs.twimg.com/profile_images/1923842414701096960/B9Nkwlvu_normal.jpg', '旋光性', '0.740', 'Twitter for iPhone', '1928520284853682666', '@jinseiminus', '1899859015863328771'], ['https://pbs.twimg.com/profile_images/1890722569994768384/uJLl-LFU_normal.jpg', 'むらさめ＠フォロー制限なう', '0.765', 'Twitter for iPhone', '1928520284958572821', '@m_pro_1', '1615634251126542336'], ['https://pbs.twimg.com/profile_images/1906628307065688064/gQXCKgVQ_normal.jpg', '三上', '0.785', 'Twitter for iPhone', '1928520285042663831', '@skli_mt', '1829156191827791872'], ['https://pbs.twimg.com/profile_images/1900667189512073217/vJkBBTQf_normal.jpg', 'やなみ', '0.787', 'Twitter for iPhone', '1928520285051039935', '@yana_maimai', '1688676847796760578'], ['https://pbs.twimg.com/profile_images/1922463186789531650/w37PBM1t_normal.jpg', 'むきむき', '0.792', 'Twitter for iPhone', '1928520285072011716', '@mikiwameru_me', '1868102908535050240'], ['https://pbs.twimg.com/profile_images/1843595657866817536/uX0zMbwl_normal.jpg', 'ふらんすあ', '0.802', 'Twitter for iPhone', '1928520285113713069', '@Franzua_97', '1239410681155207170'], ['https://pbs.twimg.com/profile_images/1711263392227524609/NpV9DrcM_normal.jpg', 'ふくろう', '0.822', 'Twitter for iPhone', '1928520285197869309', '@Hukurou029', '3286724640'], ['https://pbs.twimg.com/profile_images/1763427098570764288/QHCVczzZ_normal.jpg', '牛乳好き', '0.830', 'Twitter for iPhone', '1928520285231395286', '@gyu_nyu_su_ki', '1751944953432084480'], ['https://pbs.twimg.com/profile_images/1884752483366703105/MNKKmNUO_normal.jpg', 'ネコピク', '0.840', 'Twitter for iPhone', '1928520285273338266', '@neko_kantai', '972643488666861569'], ['https://pbs.twimg.com/profile_images/1848940637535801345/THZWdC6F_normal.jpg', 'ふうり', '0.844', 'Twitter for iPhone', '1928520285289914409', '@kymv0', '1843528019170000896'], ['https://pbs.twimg.com/profile_images/1670243122230743042/SvkJRGK-_normal.jpg', 'ふっく@美学', '0.889', 'Twitter for iPhone', '1928520285478629391', '@senaruax_inpo', '1354074114454118403'], ['https://pbs.twimg.com/profile_images/1803941386577940481/-PdRnZyL_normal.jpg', 'ごっちー', '0.893', 'Twitter for iPhone', '1928520285495636149', '@JK__dao', '2517605377'], ['https://pbs.twimg.com/profile_images/1928443880611172352/bPGNsrEu_normal.jpg', 'あ', '0.901', 'Twitter for iPhone', '1928520285529190450', '@4srola', '1723958640934322177'], ['https://pbs.twimg.com/profile_images/1906928702858108928/b8M5DuIm_normal.jpg', '揚げ豆腐', '0.927', 'Twitter for iPhone', '1928520285638074542', '@Sk69197207', '1548640627461881861'], ['https://pbs.twimg.com/profile_images/1889946474114580480/_wEL1BuL_normal.jpg', 'らむね．', '0.954', 'Twitter for iPhone', '1928520285751275939', '@Rara_prsk_01', '1875370429583671296']]
    threading.Thread(target=make_img, args=(str(results_for_img),)).start()


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
    make_ranking(result, _driver)


def notice():
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
    
    notice()
    return

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
         
