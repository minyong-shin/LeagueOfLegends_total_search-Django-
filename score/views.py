from django.shortcuts import render
import requests
from django.utils import timezone
from django.shortcuts import  get_object_or_404
from .models import Post
from .forms import PostForm

# Create your views here.

def post_new(request):
    form = PostForm()
    return render(request, 'score/post_edit.html', {'form': form})

def post_list(request):
    #posts = 쿼리셋의 이름 (매개변수)
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #request = 사용자가 요청하는 모든 것
    return render(request, 'score/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'score/post_detail.html', {'post': post})

#LOL 전적 검색
def score_view(request): #urls에 만들었던 함수
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'score/score_view.html',{'posts':posts})

#함수2개로 같은 html에 request를 하는 것은 불가능한 것인가? 
##만약 함수두개로 request를 했을 때 다른 한개의 함수는 html상에 return값이 불러오지 않음

#검색결과 함수
def search_result(request):
    if request.method == "GET":
        summoner_name = request.GET.get('search_text') #score_view html에서 넘겨 받은 text
 
        summoner_exist = False
        sum_result = {}
        solo_tier = {}
        team_tier = {}
        store_list1 = []
        store_list2 = []
        game_list ={}
        game_list2 = []
        api_key = 'RGAPI-005f5231-bf23-4a84-bac8-ce8169514e19' #부여받은 api
 
 
        summoner_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summoner_name)    #소환사 정보 검색 - 넘겨받은 텍스트를 이용하여
        params = {'api_key': api_key}
        res = requests.get(summoner_url, params=params)
        # summoners_result = json.loads(((res.text).encode('utf-8')))
        if res.status_code == requests.codes.ok: #결과값이 정상적으로 반환되었을때만 실행하도록 설정(response200)
            summoner_exist = True
            summoners_result = res.json() #response 값을 json 형태로 변환시키는 함수
            if summoners_result: #만약 summorners_result가 값이 존재한다면
                sum_result['name'] = summoners_result['name'] # 소환사 닉네임
                sum_result['level'] = summoners_result['summonerLevel'] #소환사 레벨
                sum_result['profileIconId'] = summoners_result['profileIconId'] #소환사 프로필코드(프로필도 api를 통해서 받아야함)
 
                tier_url = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + summoners_result['id']    #소환사 티어(랭크게임) 검색
                tier_info = requests.get(tier_url, params=params)
                tier_info = tier_info.json() #리그 정보 값을 json으로 변환
 
                if len(tier_info) == 1:     #자유랭크 또는 솔로랭크 둘중 하나만 있는경우
                    tier_info = tier_info.pop() #json의 맨 마지막 요소를 반환해주고 반환된 값을 삭제해주는 함수
                    if tier_info['queueType'] == 'RANKED_FLEX_SR':        #자유랭크인 경우
                        team_tier['rank_type'] = '자유랭크 5:5'
                        team_tier['tier'] = tier_info['tier']
                        team_tier['rank'] = tier_info['rank']
                        team_tier['points'] = tier_info['leaguePoints']
                        team_tier['wins'] = tier_info['wins']
                        team_tier['losses'] = tier_info['losses']
                    else:#솔로랭크인 경우
                        solo_tier['rank_type'] = '솔로랭크 5:5'
                        solo_tier['tier'] = tier_info['tier']
                        solo_tier['rank'] = tier_info['rank']
                        solo_tier['points'] = tier_info['leaguePoints']
                        solo_tier['wins'] = tier_info['wins']
                        solo_tier['losses'] = tier_info['losses']        
                if len(tier_info) == 2:            #자유랭크, 솔로랭크 둘다 전적이 있는경우
                    for item in tier_info:
                        if 'FLEX' in item['queueType']: #flex = 자유랭크일 떄
                            store_list1.append(item)
                        else:
                            store_list2.append(item)#솔로랭크일 때
                    solo_tier['rank_type'] = '솔로랭크 5:5'
                    solo_tier['tier'] = store_list2[0]['tier']
                    solo_tier['rank'] = store_list2[0]['rank']
                    solo_tier['points'] = store_list2[0]['leaguePoints']
                    solo_tier['wins'] = store_list2[0]['wins']
                    solo_tier['losses'] = store_list2[0]['losses']
 
                    team_tier['rank_type'] = '자유랭크 5:5'
                    team_tier['tier'] = store_list1[0]['tier']
                    team_tier['rank'] = store_list1[0]['rank']
                    team_tier['points'] = store_list1[0]['leaguePoints']
                    team_tier['wins'] = store_list1[0]['wins']
                    team_tier['losses'] = store_list1[0]['losses']
 
 
        return render (request, 'score/search_result.html', {'summoner_exist': summoner_exist, 'summoners_result': sum_result, 'solo_tier': solo_tier, 'team_tier': team_tier})
    #return에 있는 값은 html로 위와 같은 데이터를 보낸다는 뜻이다.