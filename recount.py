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
         

res_a = [['https://pbs.twimg.com/profile_images/1774765596644868096/ifLNoGpM_normal.jpg', 'すっしぃ', '0.010', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726283968168181', '@Sush1y', '1168514288106868737'], ['https://pbs.twimg.com/profile_images/1858170057303670784/1f0C4f_h_normal.jpg', 'すや', '0.011', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726283972256208', '@Su___8a', '1293977062181494784'], ['https://pbs.twimg.com/profile_images/1741348846582775808/HlbP3R1D_normal.jpg', 'もちきんちゃく！', '0.017', '<a href="http://twitter.com/#!/download/ipad" rel="nofollow">Twitter for iPad</a>', '1868726283997446627', '@mochikin_tdw', '1505170994033750019'], ['https://pbs.twimg.com/profile_images/1860581817788895232/D4v8zKHt_normal.jpg', 'みその', '0.018', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726284001636413', '@M5NH5K', '1601843501444259843'], ['https://pbs.twimg.com/profile_images/1861359102808727571/dXZ1Gqbu_normal.jpg', 'シャワ一ス゛𝕏334', '0.025', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1868726284030984287', '@20200202_pk', '1223924207836221440'], ['https://pbs.twimg.com/profile_images/1794098784105906177/PdotGlRs_normal.jpg', 'まめちゃん', '0.048', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1868726284127551809', '@Mame_1221s', '1278364980413227008'], ['https://pbs.twimg.com/profile_images/1868725057679511552/YIhYlZzC_normal.jpg', 'ぽて', '0.050', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726284135940233', '@yagicln', '1579506559423389696'], ['https://pbs.twimg.com/profile_images/1844656738525732864/Ugihoi-m_normal.jpg', 'dknsたけだ', '0.059', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1868726284173598844', '@darknesstakeda', '1164148705307459584'], ['https://pbs.twimg.com/profile_images/2733619244/9addec9e64135e6fec7dd039b82c3c1c_normal.png', '東方39', '0.060', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1868726284177883537', '@touhouPC', '886266235'], ['https://pbs.twimg.com/profile_images/1824129432023601152/_JtKPyWl_normal.jpg', '明治大学334サークル', '0.069', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726284215631909', '@meiji_334', '1824128548745142272'], ['https://pbs.twimg.com/profile_images/804968265650835456/ZLnztXoG_normal.png', 'かのたん🐚', '0.070', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1868726284219810248', '@kanon_ayuayu', '14743252'], ['https://pbs.twimg.com/profile_images/1860635493798752256/4iFx7TyD_normal.jpg', 'エンジェルジョーク', '0.073', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1868726284232409519', '@angeljoke', '161871065'], ['https://pbs.twimg.com/profile_images/1509738091611045889/RBw6YQ22_normal.jpg', 'し いたけ', '0.085', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726284282741059', '@mastodoner_', '1302507687389749251'], ['https://pbs.twimg.com/profile_images/1779560201059987456/EndAuo8v_normal.jpg', 'ナムジュンです。南俊秀 （ﾅﾑｼﾞｭﾝｽ）남준수', '0.088', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726284295324138', '@5VFLBuLMvn15TjD', '1539828174452060160'], ['https://pbs.twimg.com/profile_images/1811767354696826880/uZDzT88g_normal.jpg', 'らめるたん', '0.091', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726284307849608', '@r_meltyn', '1288669456344821760'], ['https://pbs.twimg.com/profile_images/1861801977698807808/p177QJ2B_normal.jpg', 'さけかす', '0.104', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1868726284362334672', '@DAMN_HUMBLE_', '1459532588750876672'], ['https://pbs.twimg.com/profile_images/1848790176220450816/AKLUpawZ_normal.jpg', 'あーる', '0.105', '<a href="http://twitter.com/#!/download/ipad" rel="nofollow">Twitter for iPad</a>', '1868726284366524896', '@r_35229', '1806074352288645120'], ['https://pbs.twimg.com/profile_images/1482689500119957504/zJONxD_2_normal.jpg', 'そこ1', '0.116', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726284412764631', '@socorahen_hito', '1482689407035801604'], ['https://pbs.twimg.com/profile_images/1842274732445696000/R9noZpIz_normal.jpg', '電池芋@工作＆DVJ', '0.116', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726284412764628', '@6_m4he', '1438635941879373831'], ['https://pbs.twimg.com/profile_images/1270727849700294661/EahcJ0DW_normal.jpg', 'きゃくと', '0.118', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1868726284421152798', '@kyakt0', '1041337350041681921'], ['https://pbs.twimg.com/profile_images/1858814635295825920/HRubu17P_normal.jpg', '青翅れおん@新人VTuber🦋⛩', '0.120', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726284429463933', '@408__2', '1752348296746790912'], ['https://pbs.twimg.com/profile_images/1801258333464313856/ottXMaVd_normal.jpg', '鼠山度優', '0.123', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1868726284442120457', '@kawahirara_BHO', '1678030148128612352'], ['https://pbs.twimg.com/profile_images/1858418180538220544/eeq2kX-3_normal.jpg', 'えがお', '0.125', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726284450512947', '@lii_ub_', '1629094379465084928'], ['https://pbs.twimg.com/profile_images/1862156507489394688/bAYBOi0W_normal.jpg', 'SugerBoy@心で工学', '0.135', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726284492423349', '@Suger_nitech', '1632771849544425472'], ['https://pbs.twimg.com/profile_images/1853039398721630208/_JNV2jQ__normal.jpg', '旧都浪.(20)', '0.144', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726284530205138', '@kua00p90', '1582328838825988097'], ['https://pbs.twimg.com/profile_images/1685179452165406720/jO3ZNPTs_normal.jpg', 'まー。②🐰師走', '0.148', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1868726284546982156', '@1010nutsA', '1365601259118596097'], ['https://pbs.twimg.com/profile_images/1844332375528046595/9-pp49QJ_normal.jpg', '四 宮 し ろ🎀🐾', '0.157', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726284584698000', '@Rikuki_spl', '1445656191812526088'], ['https://pbs.twimg.com/profile_images/1643946952500051969/xWfw4cQV_normal.jpg', 'cosecant PHI/1.00111673661...', '0.164', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1868726284614037809', '@cosecant_phi', '1382707104943853570'], ['https://pbs.twimg.com/profile_images/1774634498690551808/xt2RxGku_normal.jpg', 'シクロテト', '0.196', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1868726284748239113', '@Darewo_0', '1647128810754834434'], ['https://pbs.twimg.com/profile_images/1010763379282042881/WQ-wBxCi_normal.jpg', 'もっくる', '0.216', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1868726284832194762', '@263x031XahCyyfa', '1008954150355329024'], ['https://pbs.twimg.com/profile_images/1794292939411292160/eUU0v1R5_normal.jpg', 'けい', '0.241', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1868726284936966293', '@Kei_M_1227MK8DX', '1235067122146873346'], ['https://pbs.twimg.com/profile_images/1855213428295761920/0z4F2wM-_normal.jpg', 'ネギ塩', '0.260', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285016744431', '@negi_shio777', '1777747664182050816'], ['https://pbs.twimg.com/profile_images/1863219564076515328/I47A68UY_normal.png', 'くりにゃん😽', '0.271', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285062881765', '@ux_ec0kuri', '1625148411409481728'], ['https://pbs.twimg.com/profile_images/1770220155114819584/9xOVSdSR_normal.jpg', 'ミュートせよ！', '0.273', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1868726285071269907', '@3mdgwa', '1667866857817395201'], ['https://pbs.twimg.com/profile_images/1812877421349380096/oYbkD55P_normal.jpg', 'おぐおぐ ྀི', '0.280', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285100630107', '@oguogu8648', '1094600244984074240'], ['https://pbs.twimg.com/profile_images/1838683486519201795/tA-jNuFv_normal.jpg', 'IK', '0.280', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285100630105', '@DT02_ikejiri', '1645434969093976066'], ['https://pbs.twimg.com/profile_images/1764905595474440192/XwyIYc20_normal.jpg', '≡⺍"≠', '0.312', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285234847870', '@rkmdk_iuiui', '1715655976907689984'], ['https://pbs.twimg.com/profile_images/1846082259738415108/JSNjmYRI_normal.jpg', '怠惰な人〜卑しい+卑猥（19歳）', '0.320', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1868726285268304352', '@A18gabzhl0', '1743268948920164352'], ['https://pbs.twimg.com/profile_images/1853791259288297472/wu4ph76b_normal.jpg', '38(みや)は年末忙しい', '0.321', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285272576058', '@_38_DELTA', '1734944355595788288'], ['https://pbs.twimg.com/profile_images/1741997114501337088/O2eDgxnn_normal.jpg', 'ゆ）ゆゆゆやゆ', '0.335', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285331284157', '@yyuyuyyuyuyyyyy', '1634438681930108928'], ['https://pbs.twimg.com/profile_images/1858928615934881795/69Utx5JC_normal.jpg', 'jangajagan(ねこあつめ猫以外不定期投稿)', '0.351', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285398348233', '@jangas_drink', '1464528289993609216'], ['https://pbs.twimg.com/profile_images/1864583852788011008/qr5M1F6g_normal.jpg', 'えびふらいおじさん🐉🎏🦅鷹党\u3000バス旅大ファン\u3000南千住発メロLOVE', '0.358', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1868726285427524068', '@kirinerich10401', '1668152525126762501'], ['https://pbs.twimg.com/profile_images/1591150832481075200/jQDU8gd1_normal.jpg', '伊地知ゴマ IjichiGoma', '0.360', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1868726285436113200', '@ItyiItyi', '1591148299222147072'], ['https://pbs.twimg.com/profile_images/1851279565077037058/uwfU7Lac_normal.jpg', '草ノ者(R ʁ Я)', '0.363', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285448720508', '@kusanomonomain', '1253917768644083713'], ['https://pbs.twimg.com/profile_images/1865024134998306816/PzU1YtMq_normal.jpg', '紅生姜', '0.381', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285524255170', '@BennyGiants', '1565001569132720128'], ['https://pbs.twimg.com/profile_images/1758150780681584640/lFszs9gX_normal.jpg', 'りゆ', '0.383', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285532643579', '@Ly_ZENON', '760178020413956096'], ['https://pbs.twimg.com/profile_images/1591957486499758081/DxbBIOnJ_normal.jpg', 'ぶっし', '0.388', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285553615035', '@bussi_poke', '921376141734055936'], ['https://pbs.twimg.com/profile_images/1739299926553829376/zgzWC1yL_normal.jpg', '〒Ｔク', '0.390', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1868726285562003729', '@n_TR05', '985763706830077952'], ['https://pbs.twimg.com/profile_images/1866504205034467328/K38tkF-v_normal.jpg', '山崎武流雨舞雲天 vs 熊神', '0.410', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285645889586', '@YaMaZaKi_BlueMt', '1530973926729592832'], ['https://pbs.twimg.com/profile_images/1845247345119932417/qzIKjW4p_normal.jpg', '°ρ°(どろ゙ぉど)', '0.426', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1868726285712998412', '@Dorhodo', '1444280739579654145'], ['https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', 'yamada4649', '0.428', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', '1868726285721387395', '@yamada4649ver1', '2713779072'], ['https://pbs.twimg.com/profile_images/1862255460474396673/VhA0bJ1X_normal.jpg', '🐝はちみつクマさん🧸', '0.452', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285822050669', '@ekeymemo', '782933118177058816'], ['https://pbs.twimg.com/profile_images/1834205094386307072/lllWE2yC_normal.jpg', '2.5次元のゆきね', '0.478', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726285931102403', '@yukine_lemon1', '1550461921627090944'], ['https://pbs.twimg.com/profile_images/1774687170797977600/1SKPXHap_normal.jpg', 'おかゆ', '0.543', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726286203707538', '@h_s_256___', '1643488267340509184'], ['https://pbs.twimg.com/profile_images/1866140989779505152/f1IAxaz7_normal.jpg', 'とも@ζελέ μανταρίνι 🍊', '0.592', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726286409150755', '@tomo110104', '1476587831791583235'], ['https://pbs.twimg.com/profile_images/1062428221759602688/kgJ0--Jh_normal.jpg', 'GAKU', '0.646', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '1868726286635721039', '@GAKUm26', '1026158762082500608'], ['https://pbs.twimg.com/profile_images/1832872656938614784/fLysS9wR_normal.jpg', 'Mach', '0.673', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726286748991995', '@MotsusiMachano', '1288819327827709954'], ['https://pbs.twimg.com/profile_images/1836369640777564160/cppUMrcI_normal.jpg', 'すずﾁｹﾞ', '0.721', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726286950228162', '@Szrnk_', '1597928256149549056'], ['https://pbs.twimg.com/profile_images/1705167568020062208/_1vSl_D1_normal.jpg', 'らきさん', '0.729', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726286983872777', '@kikyo0818', '1412955518'], ['https://pbs.twimg.com/profile_images/1645061572354805762/bqfpYYPT_normal.jpg', '燻製', '0.887', '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '1868726287646572841', '@TTMMtintintin', '1645061318616166406']]

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
