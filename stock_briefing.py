import os
import json
import requests
import yfinance as yf
from bs4 import BeautifulSoup

# 1. 환경변수(GitHub Secrets 등)에서 KAKAO_TOKEN을 가져옵니다.
KAKAO_TOKEN = os.environ.get("KAKAO_TOKEN")

# 로컬에서 실행할 때 KAKAO_TOKEN 환경변수가 없으면 안내 메시지 출력 후 안전하게 종료
if not KAKAO_TOKEN:
    print("⚠️ [보안 안내] KAKAO_TOKEN 환경변수가 설정되지 않았습니다.")
    print("👉 로컬 테스트 시에는 터미널에서 아래 명령어로 환경변수를 임시 등록 후 실행하세요:")
    print("   [CMD 기준] set KAKAO_TOKEN=내토큰값")
    print("   [PowerShell 기준] $env:KAKAO_TOKEN='내토큰값'")
    exit(1)
    
# 2. 실제 보유 종목 데이터
MY_STOCKS = [
    {"code": "005930.KS", "name": "삼성전자", "buy_price": 304667},
    {"code": "006800.KS", "name": "미래에셋증권", "buy_price": 61355},
    {"code": "010140.KS", "name": "삼성중공업", "buy_price": 30241},
    {"code": "028050.KS", "name": "삼성E&A", "buy_price": 54788},
    {"code": "133690.KS", "name": "TIGER 미국나스닥100", "buy_price": 188819},
    {"code": "379800.KS", "name": "KODEX 미국S&P500TR", "buy_price": 24300},
    {"code": "091160.KS", "name": "KODEX 삼성그룹밸류", "buy_price": 14907}
]

def get_market_indices():
    """코스피, 코스닥, 나스닥 지수 수집"""
    tickers = {"코스피": "^KS11", "코스닥": "^KQ11", "나스닥": "^IXIC"}
    result = []
    for name, symbol in tickers.items():
        data = yf.Ticker(symbol).history(period="2d")
        if len(data) >= 2:
            close = data['Close'].iloc[-1]
            prev = data['Close'].iloc[-2]
            change_pct = ((close - prev) / prev) * 100
            status = "🔺" if change_pct > 0 else "🔻" if change_pct < 0 else "➖"
            result.append(f"- {name}: {close:,.2f} ({status}{change_pct:+.2f}%)")
    return "\n".join(result)

def get_my_stock_status():
    """실제 보유 종목 시세 및 수익률 수집"""
    result = []
    for stock in MY_STOCKS:
        ticker = yf.Ticker(stock['code'])
        data = ticker.history(period="2d")
        if len(data) >= 2:
            close = data['Close'].iloc[-1]
            prev = data['Close'].iloc[-2]
            change_pct = ((close - prev) / prev) * 100
            status = "🔺" if change_pct > 0 else "🔻" if change_pct < 0 else "➖"
            
            profit_pct = ((close - stock['buy_price']) / stock['buy_price']) * 100
            p_status = "🔥" if profit_pct > 0 else "💧" if profit_pct < 0 else "➖"
            
            result.append(
                f"▪️ {stock['name']}\n"
                f"  현재가: {close:,.0f}원 ({status}{change_pct:+.2f}%)\n"
                f"  수익률: {p_status} {profit_pct:+.2f}% (평단: {stock['buy_price']:,}원)"
            )
    return "\n\n".join(result)

def get_stock_news(keywords):
    """구글 뉴스 RSS를 이용해 안 끊기고 최신 뉴스 가져오기"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    news_results = []
    
    for keyword in keywords:
        # 구글 한국 뉴스 RSS 링크 활용 (크롤링 차단 및 구조 변경에 영향받지 않음)
        url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "xml")
            items = soup.find_all("item")
            if items:
                title = items[0].title.text
                # 기자/언론사 이름 깔끔하게 제거
                if " - " in title:
                    title = title.rsplit(" - ", 1)[0]
                title = title.replace('"', "'")
                news_results.append(f"📰 [{keyword}] {title}")
    
    return "\n".join(news_results) if news_results else "관련 뉴스를 불러오지 못했습니다."

def send_kakao_message(text_message):
    """안전하게 json으로 인코딩하여 카카오톡 전송"""
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": "Bearer " + KAKAO_TOKEN}
    
    template_object = {
        "object_type": "text",
        "text": text_message,
        "link": {
            "web_url": "https://m.stock.naver.com"
        }
    }
    
    payload = {
        "template_object": json.dumps(template_object)
    }
    
    res = requests.post(url, headers=headers, data=payload)
    return res.json()

if __name__ == "__main__":
    print("🔄 [방법 B] 뉴스타입 보완 후 수집 중...")
    
    indices_info = get_market_indices()
    stocks_info = get_my_stock_status()
    
    # 대표 보유 종목 3개에 대한 최신 뉴스 수집
    news_keywords = ["삼성전자", "미래에셋증권", "삼성중공업"]
    news_info = get_stock_news(news_keywords)
    
    msg_body = (
        f"📊 [종합 리포트] 주식 브리핑\n\n"
        f"[1. 주요 시장 지수]\n{indices_info}\n\n"
        f"[2. 내 보유 종목 현황]\n{stocks_info}\n\n"
        f"[3. 주요 종목 최신 뉴스]\n{news_info}"
    )
    
    print("\n--- [전송될 메시지 내용] ---")
    print(msg_body)
    print("---------------------------\n")
    
    res = send_kakao_message(msg_body)
    if res.get("result_code") == 0:
        print("✅ 성공적으로 방법 B(뉴스 포함) 브리핑이 발송되었습니다!")
    else:
        print("❌ 카카오톡 발송 실패:", res)