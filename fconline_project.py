import requests

BASE_URL = "https://open.api.nexon.com/fconline/v1/"
HEADERS = {
    "x-nxopen-api-key": "test_fbc4b3ca9ee071aea777537832d54e6b31fb04c5bd5c8b6da592c0fd1b54d743efe8d04e6d233bd35cf2fabdeb93fb0d"
}

def fetch_match_details(matchid):
    match_url = BASE_URL + "match-detail?matchid=" + matchid
    res = requests.get(match_url, headers=HEADERS)
    json = res.json()
    return json

def fetch_match_list(offset):
    url1 = BASE_URL + "match?matchtype=50&offset="
    url2 = "&limit=100"
    url = url1 + str(offset) + url2

    res = requests.get(url, headers=HEADERS)
    matchid_list = res.json()

    ouid_list = []

    for matchid in matchid_list:
        match_details = fetch_match_details(matchid)
        match_info_list = match_details["matchInfo"]

        if len(match_info_list) == 2:
            is_error_contain = False

            for match_info in match_info_list:
                match_end_type = match_info["matchDetail"]["matchEndType"]
                if match_end_type == 4:
                    is_error_contain = True

            if is_error_contain == False:
                ouid_list = []
                for match_info in match_info_list:
                    ouid = match_info["ouid"]
                    ouid_list.append(ouid)
            
            else:
                pass
        else:
            pass

    return(ouid_list)



id_list = []

num_repeat = 1
offset = 0

while offset < (num_repeat-1)*100+1:
    print(fetch_match_list(offset))
    offset += 100



    # ✅[기본 데이터]
    # 1) 가능한 범위 내에서 distinct ouid 수량
    # 2) 가능한 범위 내에서 ouid별 플레이 판수

    # ✅[유저 잔존 데이터]
    # 1) (n-1)월 플레이 ouid 유저가 (n)월 다시 플레이했는지 여부 열람하여 재플레이율 집계
    # 2) (n-1)월 플레이한 ouid 유저의 [승률 구간별 matchResult] (n)월 다시 플레이했는지  여부 열람하여 재플레이율 집계
    # 3) (n-1)월 플레이한 ouid 유저의 [골 개수별 (0~1), (1~2) 등등 goalTotal] (n)월 다시 플레이했는지 여부 열람하여 재플레이율 집계
    # —————— Join 필요——————
    # 4) (n-1)월 플레이한 ouid 유저의 [역대 최고 순경 등급 https://openapi.nexon.com/game/fconline/?id=15 의 /fconline/v1/user/maxdivision) 별)  (n)월 다시 플레이했는지  여부 열람하여 재플레이율 집계