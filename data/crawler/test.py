import requests

api_key = "AIzaSyCS5rtz0StCZDQisRNNtS_bMkUu8pFyPHw"

# 최신 모델들 테스트
models = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.5-flash"]

for model in models:
    print(f"\n🔄 {model} 테스트...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    data = {
        "contents": [{
            "parts": [{"text": "안녕하세요"}]
        }]
    }
    
    try:
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        print(f"상태: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result:
                print(f"✅ {model} 성공!")
                print(f"응답: {result['candidates'][0]['content']['parts'][0]['text']}")
                break
        else:
            print(f"❌ 실패: {response.text[:100]}")
            
    except Exception as e:
        print(f"오류: {e}")