#사전 준비
#pip install flask googlemaps python-dotenv
# .env파일 내용: GOOGLE_API_KEY=여기에_발급받은_API_KEY

from flask import Flask, jsonify
import os
from dotenv import load_dotenv
import googlemaps
from datetime import datetime

# 환경변수 로드
load_dotenv()                         #.env파일에 저장한 API키(.gitignore에 있음)를 불러들임
API_KEY = os.getenv("GOOGLE_API_KEY") # 환경 변수로 가져옴

# 클라이언트 초기화
gmaps = googlemaps.Client(key=API_KEY)
app = Flask(__name__)               #앱 생성, Flask 객체 생성(Flask 웹 애플리케이션 선언)

ORIGIN = "37.3242,127.1076"       # 죽전역 위도,경도
DEST   = "37.3219,127.1093"       # 평화의광장 위도,경도

@app.route('/eta')              #웹사이트의 '/'경로에 접속하면
def eta():                      #함수 실행
    # 실시간 교통 반영(구글지도 API 호출)
    # 출발지~목적지 사이의 경로 정보를 구글 지도에서 받아옴
    routes = gmaps.directions(      
        origin=ORIGIN,
        destination=DEST,   
        departure_time="now",           #지금 출발한다고 가정
        traffic_model="best_guess"      #교통 상황을 반영해서 시간 예측
    )
    #결과 처리
    leg = routes[0]['legs'][0]
    minutes = leg['duration_in_traffic']['value'] // 60
    #JSON으로 응답(앱, 프론트엔드에서 사용하기 편함)
    return jsonify({
        "eta": leg['duration_in_traffic']['text'],
        "eta_minutes": minutes
    })

#서버 실행 (파이썬 파일을 실행하면 서버가 열림)
#(http://localhost:5000/eta로 접속 가능)
if __name__ == '__main__':
    app.run(debug=True) 
