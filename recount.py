import copy, datetime, json, os, requests, sys, threading, time, traceback, re, gzip, io, hmac, hashlib, base64, urllib.parse, random
from collections import defaultdict

TIME334 = [3, 34]
KEYWORD = '334'
PHP_URL = os.environ['PHP_URL']
clients = ['Twitter for iPhone',  'Twitter for Android',  'Twitter Web Client',  'TweetDeck',  'TweetDeck Web App',  'Twitter for iPad',  'Twitter for Mac',  'Twitter Web App',  'Twitter Lite',  'Mobile Web (M2)',  'Twitter for Windows',  'Janetter',  'Janetter for Android',  'Janetter Pro for iPhone',  'Janetter for Mac',  'Janetter Pro for Android',  'Tweetbot for iΟS',  'Tweetbot for iOS',  'Tweetbot for Mac',  'twitcle plus',  'ツイタマ',  'ツイタマ for Android',  'ツイタマ+ for Android',  'Sobacha',  'SobaCha',  'Metacha',  'MetaCha',  'MateCha',  'ツイッターするやつ',  'ツイッターするやつγ',  'ツイッターするやつγ pro',  'jigtwi',  'feather for iOS',  'hamoooooon',  'Hel2um on iOS',  'Hel1um Pro on iOS',  'Hel1um on iOS',  'undefined']

BEFORE = 0 ##### 何日前の計測？

records_rank, today_result, driver, request_body, request_header = {}, {}, {}, {}, {}
past_records, rep_accounts = [], []
today_joined = 0
prepare_flag = False


def request_php(url, data = None):
    for attempt in range(5):
        try:
            if data != None:
                response = requests.post(PHP_URL + url + '.php', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
                return response
            else:
                response = requests.get(PHP_URL + url + '.php')
                return response.json()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 5 - 1:
                print(f"Retrying in {60} seconds...")
                time.sleep(60)
            else:
                print("All attempts failed.")
                return None


def TweetIdTime(id):
    """ツイートIDを投稿時刻に変換"""
    return datetime.datetime.fromtimestamp(((id >> 22) + 1288834974657) / 1000.0)


def make_world_rank():
    """級位ポイント計算"""

    def time_to_point(date, result):
        """タイムをポイントに変換"""

        days = (datetime.datetime.now() - date).days - BEFORE
        b = 10000 * 2 ** (-10 * float(result))
        if days >= 30: b *= (91 - days) / 61
        return b

    user_data = defaultdict(lambda: {'valid': [], 'all': [], 'a': []})
    for entry in past_records:
        userid, date, value, source = entry
        user_data[userid]['a'].append(value)
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


def make_ranking(results_dict_arr, _driver):
    """当日分のランキングの作成"""

    #生データを扱いやすい形に変換

    global records_rank, today_result, today_joined, prepare_flag
    now = datetime.datetime.now() - datetime.timedelta(days=BEFORE, hours=TIME334[0], minutes=TIME334[1])
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
                    case 2: records_rank[id]['s'] += 1
                    case 3: records_rank[id]['t'] += 1
                if current_rank <= 30: records_rank[id]['rankin'] += 1

                update_list = list(records_rank[id].values())[:8]
                update_list.insert(0, id)
                update_records_rank.append(update_list)

                past_records.append([id, now, result_str, source])
                update_past_records.append([id, today_str, result_str, source]) #JSONにできるよう文字列に


    make_world_rank()

    prepare_flag = False

    for update_record in update_records_rank:
        update_record[3] = records_rank[update_record[0]]['max_pt']

    print(update_records_rank)
    print(update_past_records)

    response = request_php('add_rank', update_records_rank) ##### rankを保存する場合はつける
    print("Response:", response.status_code, response.text)
    response = request_php('add', update_past_records) ##### resultを保存する場合はつける
    print("Response:", response.status_code, response.text)




def main():

    global past_records, today_result, today_joined, records_rank
    today_unsorted = []
    response = request_php('get2') ##### 100日前まで取得用
    for record in response:
        record_time = datetime.datetime.strptime(record['date'], '%Y-%m-%d') + datetime.timedelta(hours=TIME334[0], minutes=TIME334[1])
        days = (datetime.datetime.now() - record_time).days - BEFORE - 1
        if 0 <= days <= 91: past_records.append([record['userid'], record_time, record['result'], record['source']])
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

main()
print("SET")
         

res_a = [['https://pbs.twimg.com/profile_images/1738736703937134592/g2ERfgAz_normal.png', 'のりさん❄️', '0.012', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451059707699206', '@FFFFFEF1', '1106604090'], ['https://pbs.twimg.com/profile_images/1451862729950564355/6SCpFJU8_normal.jpg', 'ハマチ', '0.015', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451059720270093', '@howmuch0120444', '1380448137857224705'], ['https://pbs.twimg.com/profile_images/1770269942782496768/s6TX_jlq_normal.jpg', 'わくわく', '0.021', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1869451059745497330', '@wakuwakuzukkyun', '1603269535028502529'], ['https://pbs.twimg.com/profile_images/1862031349433176064/1ZOz_M6C_normal.jpg', '陽月', '0.024', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1869451059758092654', '@Fig_MusicGamer', '1823970695933779968'], ['https://pbs.twimg.com/profile_images/1861359102808727571/dXZ1Gqbu_normal.jpg', 'シャワ一ス゛𝕏334', '0.028', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451059774791771', '@20200202_pk', '1223924207836221440'], ['https://pbs.twimg.com/profile_images/1845682383020068864/ap9B5JXG_normal.jpg', 'あおり', '0.033', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451059795779913', '@0__x26', '1838390850734428163'], ['https://pbs.twimg.com/profile_images/1860635493798752256/4iFx7TyD_normal.jpg', 'エンジェルジョーク', '0.044', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1869451059841868040', '@angeljoke', '161871065'], ['https://pbs.twimg.com/profile_images/1779560201059987456/EndAuo8v_normal.jpg', 'ナムジュンです。南俊秀 （ﾅﾑｼﾞｭﾝｽ）남준수', '0.048', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451059858714917', '@5VFLBuLMvn15TjD', '1539828174452060160'], ['https://pbs.twimg.com/profile_images/1504016355758329857/O7NDscPO_normal.jpg', '那珂ちゃ☀️', '0.060', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451059909030076', '@Hukuchi_Nakacha', '1502470777974964226'], ['https://pbs.twimg.com/profile_images/1858468612941742080/E6FZcYWY_normal.jpg', 'もっち', '0.062', '<a href="http://itunes.apple.com/us/app/twitter/id409789998?mt=12" rel="nofollow">Twitter for Mac</a>', '1869451059917418575', '@m0_ch_I', '1449729192199819264'], ['https://pbs.twimg.com/profile_images/1862156507489394688/bAYBOi0W_normal.jpg', 'SugerBoy@心で工学', '0.063', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451059921641491', '@Suger_nitech', '1632771849544425472'], ['https://pbs.twimg.com/profile_images/1848790176220450816/AKLUpawZ_normal.jpg', 'あーる', '0.063', '<a href="http://twitter.com/#!/download/ipad" rel="nofollow">Twitter for iPad</a>', '1869451059921551486', '@r_35229', '1806074352288645120'], ['https://pbs.twimg.com/profile_images/1768293753268346880/VNo1G1lz_normal.jpg', '始発快速3821M', '0.064', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451059925807161', '@Rapid_3821M', '1373177377237262340'], ['https://pbs.twimg.com/profile_images/1736619347102285824/cx7SRdyr_normal.jpg', '🎵', '0.075', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451059971948826', '@U22qun', '1725189173102227456'], ['https://pbs.twimg.com/profile_images/1869492861542248448/rN6-Sm3R_normal.jpg', '和男@精子提供者', '0.092', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451060043280885', '@3mdgwa', '1667866857817395201'], ['https://pbs.twimg.com/profile_images/1868183366182506496/T3ckX7gj_normal.jpg', 'セレン', '0.092', '<a href="http://twitter.com/#!/download/ipad" rel="nofollow">Twitter for iPad</a>', '1869451060043268346', '@Seren__k', '1765015630531731456'], ['https://pbs.twimg.com/profile_images/1794292939411292160/eUU0v1R5_normal.jpg', 'けい', '0.095', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451060055810399', '@Kei_M_1227MK8DX', '1235067122146873346'], ['https://pbs.twimg.com/profile_images/804968265650835456/ZLnztXoG_normal.png', 'かのたん🐚', '0.105', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451060097806442', '@kanon_ayuayu', '14743252'], ['https://pbs.twimg.com/profile_images/1736713357695311872/pGKOgbi8_normal.jpg', '𝑅𝑒:𝑅𝑒:てぃだ', '0.109', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451060114587800', '@ReRe_tiiiiidus', '1736712482708967424'], ['https://pbs.twimg.com/profile_images/1607950922495459330/urMMi633_normal.jpg', '⭐️ ͡° ͜ʖ ͡°💧純愛だよ💃', '0.110', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060118737367', '@660o___o099', '1544226984347455489'], ['https://pbs.twimg.com/profile_images/1864533445579558913/8tZsurla_normal.jpg', 'マイナス大凶', '0.113', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451060131340587', '@I0cm_Ita_AI', '1681543774307229696'], ['https://pbs.twimg.com/profile_images/1810684511942057984/Rb6SuXb8_normal.jpg', 'いーるけん', '0.119', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451060156535010', '@Eel_Ken', '935502914029731841'], ['https://pbs.twimg.com/profile_images/1854414813700726784/JV64zsIn_normal.jpg', 'えすぽん/SSK', '0.120', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1869451060160704677', '@espn_prsk', '1271072534339792896'], ['https://pbs.twimg.com/profile_images/1847012031586881538/kgaDPcC-_normal.jpg', '朝比奈', '0.121', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060164833731', '@a5hnb', '1839206825218158594'], ['https://pbs.twimg.com/profile_images/1818995193619927040/l2wtEvtW_normal.jpg', 'Re:ぷす', '0.129', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451060198420838', '@syamu_81111', '1769008236588605440'], ['https://pbs.twimg.com/profile_images/1853426199311319041/ds3qXLky_normal.jpg', 'えるぽてと', '0.143', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060257107975', '@Lpoteto_777', '1439815359440187392'], ['https://pbs.twimg.com/profile_images/1332487404398071808/h-gB53hO_normal.jpg', 'とりま荒野行動ゴミゲー？', '0.151', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060290695257', '@_i_am_Nc_0811', '1048881129132969984'], ['https://pbs.twimg.com/profile_images/1795406001849655296/UY0IMZPU_normal.jpg', 'いも', '0.159', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451060324307000', '@ohqvqi_2', '1795405751235817472'], ['https://pbs.twimg.com/profile_images/1705259821438824449/JXlhFMEO_normal.jpg', 'ゐんてる', '0.176', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060395581522', '@intel_765', '769367074623729665'], ['https://pbs.twimg.com/profile_images/1788578052773146625/32GepRyi_normal.jpg', 'ℂ𝕚𝕥𝕣𝕠ℕ', '0.176', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1869451060395516254', '@jingdoudaxue', '1775433206474723328'], ['https://pbs.twimg.com/profile_images/1808167674616369152/WdtdC2in_normal.jpg', 'D', '0.177', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060399788463', '@namanama20001', '1504482913160601607'], ['https://pbs.twimg.com/profile_images/1865478636922642432/aUz0D99r_normal.jpg', 'ka_araragi', '0.182', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060420792408', '@ka_araragi', '1519890562014318592'], ['https://pbs.twimg.com/profile_images/1819403699535716352/SaG2SUUx_normal.jpg', '京セラマニア', '0.187', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060441763871', '@Kyocera_Mania', '1819013439240749056'], ['https://pbs.twimg.com/profile_images/1605863262452490240/uSSKM3o9_normal.jpg', 'たんさんそ', '0.192', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060462723569', '@NaHCO3daimaoo', '1605862293069185024'], ['https://pbs.twimg.com/profile_images/1865360032680030208/pYDtHuzs_normal.jpg', 'フライゴンフライゴンフライゴンフライゴンフライゴンフライゴンフライゴンフライゴンフライゴンフライゴン', '0.209', '<a href="http://twitter.com/#!/download/ipad" rel="nofollow">Twitter for iPad</a>', '1869451060533952528', '@furaigon520', '1509847673440186370'], ['https://pbs.twimg.com/profile_images/1840984090046316544/rmTByDM7_normal.jpg', '医ノウエハルト', '0.219', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060575969784', '@OMAESANTATI', '1634024015168966657'], ['https://pbs.twimg.com/profile_images/1795018789303865344/HN0xckJy_normal.jpg', 'as', '0.227', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060609515553', '@GIGALODOON', '1549407179006148608'], ['https://pbs.twimg.com/profile_images/1858928615934881795/69Utx5JC_normal.jpg', 'jangajagan(ねこあつめ猫以外不定期投稿)', '0.258', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060739506464', '@jangas_drink', '1464528289993609216'], ['https://pbs.twimg.com/profile_images/1844419013977534464/2plarLqw_normal.jpg', '蟹巻き🦀', '0.262', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060756271328', '@kanishisurvive', '1838581412582326272'], ['https://pbs.twimg.com/profile_images/1721013062164250624/vNTmpyvc_normal.jpg', '梶木\u3000真黒', '0.275', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060810850454', '@kazisan1108', '1552514568118992896'], ['https://pbs.twimg.com/profile_images/1858294501795913728/VA9vkRoD_normal.jpg', 'ゆーら', '0.305', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060936618046', '@yuras0701', '1265907792449163264'], ['https://pbs.twimg.com/profile_images/1864386017828196354/sZ9zNwen_normal.jpg', 'わんぱくタック', '0.306', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060940849346', '@1pactak', '1503449130'], ['https://pbs.twimg.com/profile_images/1633383811844308992/8lVkrQd9_normal.jpg', 'Tsusu', '0.309', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060953440492', '@tsusu0409', '1404693864842076163'], ['https://pbs.twimg.com/profile_images/1863219564076515328/I47A68UY_normal.png', 'くりにゃん😽', '0.313', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451060970197411', '@ux_ec0kuri', '1625148411409481728'], ['https://pbs.twimg.com/profile_images/1852904069851213824/eTyqC-a2_normal.jpg', 'クッキーズ', '0.318', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451060991193495', '@jishoubblcookie', '1852903941929066496'], ['https://pbs.twimg.com/profile_images/1591957486499758081/DxbBIOnJ_normal.jpg', 'ぶっし', '0.325', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451061020528969', '@bussi_poke', '921376141734055936'], ['https://pbs.twimg.com/profile_images/1492541755329495041/dxRP5DYl_normal.jpg', 'Kotaro.Mi', '0.328', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451061033128423', '@Kotaro_sinon', '1033982495597854720'], ['https://pbs.twimg.com/profile_images/1852314978646401024/FNnlgMK__normal.jpg', '内定でるでるザウルス@26卒', '0.338', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451061075001805', '@akiyoshidai0256', '1759099051268829184'], ['https://pbs.twimg.com/profile_images/1864583852788011008/qr5M1F6g_normal.jpg', 'えびふらいおじさん🐉🎏🦅鷹党\u3000バス旅大ファン\u3000南千住発メロLOVE', '0.354', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451061141856758', '@kirinerich10401', '1668152525126762501'], ['https://pbs.twimg.com/profile_images/772845398805229570/4xCUQ9oS_normal.jpg', 'KING', '0.364', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451061184123073', '@popnneu', '320098147'], ['https://pbs.twimg.com/profile_images/1614665373181415426/1e7XNVDx_normal.jpg', 'NEETUEL V', '0.367', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451061196693948', '@shobooonchan2', '879617546114088960'], ['https://pbs.twimg.com/profile_images/1565793800592637953/07wBxvxx_normal.jpg', '山口大学334サークル\u3000常磐キャンパス支部', '0.367', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451061196410931', '@yu334_ube', '1565776565518356481'], ['https://pbs.twimg.com/profile_images/1591150832481075200/jQDU8gd1_normal.jpg', '伊地知ゴマ IjichiGoma', '0.380', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451061251235871', '@ItyiItyi', '1591148299222147072'], ['https://pbs.twimg.com/profile_images/1845249740281417728/s4no_jTm_normal.jpg', 'キャス', '0.385', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451061272219675', '@kyasly__4', '1761578867301793792'], ['https://pbs.twimg.com/profile_images/1739299926553829376/zgzWC1yL_normal.jpg', '〒Ｔク', '0.392', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451061301477840', '@n_TR05', '985763706830077952'], ['https://pbs.twimg.com/profile_images/1793013928555065344/5nRNL3tT_normal.jpg', 'めーさん＠闘病中', '0.397', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451061322547381', '@SRST223', '76051375'], ['https://pbs.twimg.com/profile_images/1824129432023601152/_JtKPyWl_normal.jpg', '明治大学334サークル', '0.423', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451061431558537', '@meiji_334', '1824128548745142272'], ['https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', 'yamada4649', '0.426', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451061444161659', '@yamada4649ver1', '2713779072'], ['https://pbs.twimg.com/profile_images/1832060660890656768/cSm5Uy9i_normal.jpg', '中々最中', '0.440', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451061502845388', '@imiwaka_nakana', '1390944803639099393'], ['https://pbs.twimg.com/profile_images/1802629966624071680/JKBKXxRe_normal.jpg', 'Remith', '0.453', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451061557383611', '@Illmth', '1421068869586735108'], ['https://pbs.twimg.com/profile_images/1811003422029795328/rmlmGC82_normal.jpg', 'でぶぅ', '0.477', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451061658018209', '@strand_06', '1569331650131283968'], ['https://pbs.twimg.com/profile_images/1853336693270863872/MGjUkq5V_normal.jpg', 'ふら🧟\u200d♀️@紫電会長', '0.492', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451061720961125', '@breakfrandle', '2650207178'], ['https://pbs.twimg.com/profile_images/1831362451537072129/H_UbCC_i_normal.png', 'ｵｻﾄｳﾁｬﾝ', '0.517', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451061825765654', '@oxragus', '1619584673260384260'], ['https://pbs.twimg.com/profile_images/1865287068970291202/v01Tk6fl_normal.jpg', 'K【旅行・虎ファン】', '0.566', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1869451062031405399', '@Traveler_K1000', '1579068928630087681'], ['https://pbs.twimg.com/profile_images/1845262717004939266/VmJwQJ3N_normal.jpg', 'りぃぷりちゃん🌱(Pinky Crush Ver.)', '0.572', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451062056513619', '@pripri_rr', '238419112'], ['https://pbs.twimg.com/profile_images/1799305800302927872/jDwYzylV_normal.jpg', '夜踊', '0.573', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451062060753179', '@odoriko185_kei', '913184068640030721'], ['https://pbs.twimg.com/profile_images/1842274732445696000/R9noZpIz_normal.jpg', '電池芋@工作＆DVJ', '0.642', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451062350168407', '@6_m4he', '1438635941879373831'], ['https://pbs.twimg.com/profile_images/1258787805351698432/myPayCMR_normal.jpg', 'らららんど', '0.643', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451062354276689', '@o_oilo_oilo_o', '1258468588068847616'], ['https://pbs.twimg.com/profile_images/1868583252543598592/yPmgzxkf_normal.jpg', '県民', '0.680', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451062509470056', '@uowwwwwwwwww', '1804101373119860738'], ['https://pbs.twimg.com/profile_images/1848613340488339458/FoH_oc_e_normal.jpg', '😆', '0.723', '<a href="http://twitter.com/#!/download/ipad" rel="nofollow">Twitter for iPad</a>', '1869451062689832961', '@LLLL_4444_L', '1848613260238675968'], ['https://pbs.twimg.com/profile_images/1838273797797109760/HRo-1bjY_normal.jpg', 'なつもん🍀 @ヘルム推し指揮官', '0.742', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451062769496199', '@Yotuba04_NATU', '1108951998404034562'], ['https://pbs.twimg.com/profile_images/1701064933310627840/3ExJM3NQ_normal.jpg', '雪', '0.755', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451062824034425', '@yukikaze_zzz', '4666217954'], ['https://pbs.twimg.com/profile_images/1848124112901926912/IR802aMz_normal.jpg', 'めんでる。', '0.812', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451063063142667', '@thk_uts', '1825500688983670784'], ['https://pbs.twimg.com/profile_images/1658072228205064192/EkvHoIcA_normal.jpg', 'ほしなつ', '0.825', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451063117709388', '@Dep_LOCAL_Last', '923545777225338881'], ['https://pbs.twimg.com/profile_images/1720063068145872896/vQ7KBk2x_normal.jpg', 'dryfruit', '0.847', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451063209988301', '@dryfruitmixtaku', '908690195796582405'], ['https://pbs.twimg.com/profile_images/1864638207826251776/s4gwo2aG_normal.jpg', 'ざわ', '0.862', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1869451063272845315', '@zawa__n', '1268100540136734720'], ['https://pbs.twimg.com/profile_images/1868308728195448832/RcE9ubJf_normal.jpg', 'いれぶん', '0.939', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451063595839620', '@elevenkun11', '1720364188823064576'], ['https://pbs.twimg.com/profile_images/1271518516546437125/yPRqy9i8_normal.jpg', '自称名探偵約100人の神絵師たち(フォロー整理中)', '0.967', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1869451063713272053', '@100ninkamieshi', '852805428022882305'], ['https://pbs.twimg.com/profile_images/1853892858216136704/4sq9VMAE_normal.jpg', 'しごん@北陸の民', '0.972', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1869451063734202621', '@shigano_geo', '1417365578868658187']]

res_b = []
for a in res_a:
    res_b.append({
                'id_str': a[4],
                'text': '334',
                'source': a[3],
                'user': {
                    'id_str': a[6],
                    'name': a[1],
                    'screen_name': a[5][1:],
                    'profile_image_url_https': a[0]
                },

    })

make_ranking(res_b, {})
