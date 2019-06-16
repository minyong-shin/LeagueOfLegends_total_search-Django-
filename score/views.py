from django.shortcuts import render
import requests
from django.utils import timezone
from django.shortcuts import render, get_object_or_404

# Create your views here.

#LOL 전적 검색
def score_view(request): #urls에 만들었던 함수
    return render(request,'score/score_view.html')

def search_result(request):
    if request.method == 'GET':
        summoner_name = request.GET.get('search_text') #GET방식으로 호출
        #request.args.get('name' = 'search_text') 이렇게 아이디를 입력받을 수 있음
        summoner_exist = False
        sum_result = {}
        solo_tier = {}
        team_tier = {}
        store_list = []
        game_list ={}
        game_list2 = []
        api_key = 'RGAPI-13c764c0-5c5b-47ae-b75b-32dd91590d46'

        summoner_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summoner_name)    #소환사 정보 검색
        params = {'api_key': api_key} #api를 호출하는데 중요
        res = requests.get(summoner_url, params=params)#api키를 param으로만 받아도 데이터를 불러올 수 있음
        # summoners_result = json.loads(((res.text).encode('utf-8')))
        
        if res.status_code == requests.codes.ok:                #결과값이 정상적으로 반환되었을때만 실행하도록 설정
            summoner_exist = True
            summoners_result = res.json()                        #response 값을 json 형태로 변환시키는 함수
            if summoners_result:
                sum_result['name'] = summoners_result['name']
                sum_result['level'] = summoners_result['summonerLevel']
                sum_result['profileIconId'] = summoners_result['profileIconId']
 
                tier_url = "https://kr.api.riotgames.com/lol/league/v4/positions/by-summoner/" + summoners_result['id']    #소환사 티어 검색
                tier_info = requests.get(tier_url, params=params)
                tier_info = tier_info.json()
 
                if len(tier_info) == 1:            #자유랭크 또는 솔로랭크 둘중 하나만 있는경우
                    tier_info = tier_info.pop()
                    if tier_info['queueType'] == 'RANKED_FLEX_SR':        #자유랭크인 경우
                        team_tier['rank_type'] = '자유랭크 5:5'
                        team_tier['tier'] = tier_info['tier']
                        team_tier['rank'] = tier_info['rank']
                        team_tier['points'] = tier_info['leaguePoints']
                        team_tier['wins'] = tier_info['wins']
                        team_tier['losses'] = tier_info['losses']
                    else:                                                #솔로랭크인 경우
                        solo_tier['rank_type'] = '솔로랭크 5:5'
                        solo_tier['tier'] = tier_info['tier']
                        solo_tier['rank'] = tier_info['rank']
                        solo_tier['points'] = tier_info['leaguePoints']
                        solo_tier['wins'] = tier_info['wins']
                        solo_tier['losses'] = tier_info['losses']        
                if len(tier_info) == 2:            #자유랭크, 솔로랭크 둘다 전적이 있는경우
                    for item in tier_info:
                        store_list.append(item)
                    solo_tier['rank_type'] = '솔로랭크 5:5'
                    solo_tier['tier'] = store_list[0]['tier']
                    solo_tier['rank'] = store_list[0]['rank']
                    solo_tier['points'] = store_list[0]['leaguePoints']
                    solo_tier['wins'] = store_list[0]['wins']
                    solo_tier['losses'] = store_list[0]['losses']
 
                    team_tier['rank_type'] = '자유랭크 5:5'
                    team_tier['tier'] = store_list[1]['tier']
                    team_tier['rank'] = store_list[1]['rank']
                    team_tier['points'] = store_list[1]['leaguePoints']
                    team_tier['wins'] = store_list[1]['wins']
                    team_tier['losses'] = store_list[1]['losses']
 
 
        return render (request, 'score/search_result.html', {'summoner_exist': summoner_exist, 'summoners_result': sum_result, 'solo_tier': solo_tier, 'team_tier': team_tier})