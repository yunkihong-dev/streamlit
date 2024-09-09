# # API 호출을 위해 requests 모듈을 사용
# import requests
# import json
# from urllib import parse # 한글
# api_key = "RGAPI-5c7b73e1-d6e5-43c9-808e-9d9ba18d2f09" # 새로 발급받은 api_key
# REQUEST_HEADERS = {
# "X-Riot-Token": api_key
# }
# userNickname="sareed"
# tagLine="KR1"
# encodedName = parse.quote(userNickname)
# print(encodedName)
# url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{encodedName}/{tagLine}"

# player_id = requests.get(url, headers=REQUEST_HEADERS).json()
# print(player_id)

# puuid = player_id['puuid']
# url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
# player = requests.get(url, headers=REQUEST_HEADERS).json()
# print(player)

# playerInfo = requests.get("https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+player['id'], headers = REQUEST_HEADERS).json();

# n_wins = playerInfo[0]['wins']
# n_losses = playerInfo[0]['losses']
# n_total = n_wins + n_losses;
# print(n_wins); print(n_losses); print(n_total)

# r = n_total // 100
# other = n_total % 100

# all_gamesID = []
# for i in range(r+1):
#     start = i*100
#     if i != r :
#         tmp_gamesID = requests.get(f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{player['puuid']}/ids?type=ranked&start={start}&count={100}", headers = REQUEST_HEADERS).json();
#     else :
#         tmp_gamesID = requests.get(f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{player['puuid']}/ids?type=ranked&start={start}&count={other}", headers = REQUEST_HEADERS).json();

#     all_gamesID.extend(tmp_gamesID)
# gameInfo =requests.get("https://asia.api.riotgames.com/lol/match/v5/matches/"+all_gamesID[0], headers = REQUEST_HEADERS).json();
# print(gameInfo)

# ================================================================
# import streamlit as st

# # HTML과 CSS를 포함한 코드
# st.markdown(
#     """
#     <style>
#     .big-font {
#         font-size:50px !important;
#         color: brown;
#     }
#     .box {
#         background-color: #f0f0f0;
#         padding: 20px;
#         border-radius: 10px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # HTML에 클래스 적용
# st.markdown('<p class="big-font">Faker</p>', unsafe_allow_html=True)

# # 다른 HTML 요소에 CSS 적용
# st.markdown('<div class="box">This is a styled box</div>', unsafe_allow_html=True)
# ================================================================
import streamlit as st
import requests
from urllib import parse  # 한글 처리용

# Riot API 설정
api_key = "RGAPI-5c7b73e1-d6e5-43c9-808e-9d9ba18d2f09"  # 자신의 API 키로 변경
REQUEST_HEADERS = {
    "X-Riot-Token": api_key
}

# API 요청 함수들 정의
def get_player_id(userNickname, tagLine):
    """ 소환사 닉네임과 태그라인을 통해 PUUID 조회 """
    encoded_name = parse.quote(userNickname)  # 한글 처리
    url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{encoded_name}/{tagLine}"
    response = requests.get(url, headers=REQUEST_HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("소환사 정보를 가져올 수 없습니다.")
        return None

def get_summoner_info(puuid):
    """ PUUID로 소환사 정보 조회 """
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    response = requests.get(url, headers=REQUEST_HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("소환사 정보를 가져올 수 없습니다.")
        return None

def get_rank_info(summoner_id):
    """ 소환사 ID로 랭크 정보 조회 """
    url = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    response = requests.get(url, headers=REQUEST_HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("랭크 정보를 가져올 수 없습니다.")
        return None

def get_match_history(puuid, total_games):
    """ 소환사 PUUID로 게임 기록 조회 """
    all_game_ids = []
    r = total_games // 100
    other = total_games % 100

    for i in range(r + 1):
        start = i * 100
        if i != r:
            url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start={start}&count=100"
        else:
            url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start={start}&count={other}"
        
        response = requests.get(url, headers=REQUEST_HEADERS)
        if response.status_code == 200:
            all_game_ids.extend(response.json())
        else:
            st.error("게임 기록을 가져올 수 없습니다.")
            return None
    
    return all_game_ids

def get_match_info(game_id):
    """ 게임 ID로 게임 정보 조회 """
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{game_id}"
    response = requests.get(url, headers=REQUEST_HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("게임 정보를 가져올 수 없습니다.")
        return None


# Streamlit 인터페이스 구성
st.title("Riot Games 소환사 정보 조회")
st.write("Riot API를 사용하여 소환사 정보와 랭크, 게임 기록을 확인합니다.")
# 입력받은 소환사 닉네임과 태그라인
userNickname = st.text_input("소환사 이름을 입력하세요", "sareed")
tagLine = st.text_input("태그라인을 입력하세요", "KR1")

# 소환사 검색 버튼
if st.button("검색"):
    if userNickname and tagLine:
        # 1. 소환사 정보 조회
        player_id = get_player_id(userNickname, tagLine)
        
        if player_id:
            puuid = player_id['puuid']
            summoner_info = get_summoner_info(puuid)

            if summoner_info:
                print(summoner_info)
                st.subheader(f"소환사 이름: {summoner_info['name']}")
                st.write(f"레벨: {summoner_info['summonerLevel']}")
                
                # 2. 랭크 정보 조회
                rank_info = get_rank_info(summoner_info['id'])
                if rank_info:
                    wins = rank_info[0]['wins']
                    losses = rank_info[0]['losses']
                    st.write(f"승리: {wins} / 패배: {losses}")
                    st.write(f"총 경기 수: {wins + losses}")
                    
                    # 3. 게임 기록 조회
                    all_game_ids = get_match_history(puuid, wins + losses)
                    if all_game_ids:
                        st.write(f"최근 {len(all_game_ids)} 게임의 기록을 확인했습니다.")
                        
                        # 4. 첫 번째 게임 정보 출력
                        game_info = get_match_info(all_game_ids[0])
                        if game_info:
                            st.write("첫 번째 게임 정보:", game_info)
    else:
        st.error("소환사 이름과 태그라인을 입력하세요.")
