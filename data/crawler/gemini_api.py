# crawler/gemini_api.py - Gemini AI 마케팅 전략 생성
import os
import json
import requests
from datetime import datetime

# 환경변수 로딩
try:
    from dotenv import load_dotenv
    load_dotenv()  # .env 파일에서 환경변수 로드
except ImportError:
    print("⚠️ python-dotenv가 설치되지 않았습니다. pip install python-dotenv로 설치하세요.")

class GeminiMarketingStrategist:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            print("⚠️ GEMINI_API_KEY가 설정되지 않았습니다.")
            print("💡 기본 전략 생성 모드로 작동합니다.")
            self.api_key = None
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    
    def generate_marketing_strategy(self, reviews_data):
        """리뷰 데이터를 바탕으로 AI 마케팅 전략 생성"""
        
        # API 키가 없으면 기본 전략 반환
        if not self.api_key:
            print("🔄 API 키가 없으므로 기본 전략을 생성합니다...")
            summary = self._create_review_summary(reviews_data)
            return self._generate_fallback_strategy(summary)
        
        # 리뷰 데이터 요약
        summary = self._create_review_summary(reviews_data)
        
        # AI 프롬프트 생성
        prompt = self._create_strategy_prompt(summary)
        
        # Gemini API 호출
        try:
            strategy = self._call_gemini_api(prompt)
            return strategy
        except Exception as e:
            print(f"❌ Gemini API 호출 실패: {e}")
            # 실패시 기본 전략 반환
            return self._generate_fallback_strategy(summary)
    
    def _create_review_summary(self, reviews):
        """리뷰 데이터 요약"""
        if not reviews:
            return {"total": 0, "positive": 0, "negative": 0, "neutral": 0, "key_points": []}
        
        positive_count = len([r for r in reviews if r.get('sentiment') == 'positive'])
        negative_count = len([r for r in reviews if r.get('sentiment') == 'negative'])
        neutral_count = len([r for r in reviews if r.get('sentiment') == 'neutral'])
        
        # 주요 키워드 추출
        all_positive_keywords = []
        all_negative_keywords = []
        key_reviews = []
        
        for review in reviews:
            all_positive_keywords.extend(review.get('positive_keywords', []))
            all_negative_keywords.extend(review.get('negative_keywords', []))
            
            # 대표적인 리뷰 내용 추출
            key_reviews.append({
                'title': review.get('title', '')[:100],
                'content': review.get('content', '')[:200],
                'sentiment': review.get('sentiment', 'neutral'),
                'date': review.get('date', '')
            })
        
        # 키워드 빈도 계산
        from collections import Counter
        top_positive = Counter(all_positive_keywords).most_common(5)
        top_negative = Counter(all_negative_keywords).most_common(5)
        
        return {
            'total_reviews': len(reviews),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'positive_ratio': round(positive_count / len(reviews) * 100, 1),
            'negative_ratio': round(negative_count / len(reviews) * 100, 1),
            'top_positive_keywords': top_positive,
            'top_negative_keywords': top_negative,
            'key_reviews': key_reviews[:3]  # 처음 3개만
        }
    
    def _create_strategy_prompt(self, summary):
        """AI용 마케팅 전략 생성 프롬프트"""
        prompt = f"""
당신은 키즈카페 마케팅 전문가입니다. 다음 리뷰 분석 데이터를 바탕으로 구체적이고 실용적인 마케팅 전략을 제안해주세요.

## 키즈카페 정보
- 업체명: 우리끼리 키즈카페 대전문화점
- 업종: 무인 키즈카페
- 지역: 대전 서구 문화점

## 리뷰 분석 데이터
- 총 리뷰 수: {summary['total_reviews']}개
- 긍정적 리뷰: {summary['positive_count']}개 ({summary['positive_ratio']}%)
- 부정적 리뷰: {summary['negative_count']}개 ({summary['negative_ratio']}%)
- 중립적 리뷰: {summary['neutral_count']}개

### 고객들이 좋아하는 점
{', '.join([f"{kw}({cnt}회)" for kw, cnt in summary['top_positive_keywords']])}

### 개선이 필요한 점
{', '.join([f"{kw}({cnt}회)" for kw, cnt in summary['top_negative_keywords']])}

### 주요 리뷰 내용
"""
        
        for i, review in enumerate(summary['key_reviews'], 1):
            prompt += f"""
{i}. [{review['sentiment']}] {review['title']}
   "{review['content']}"
"""
        
        prompt += """

## 요청사항
다음 형식으로 구체적인 마케팅 전략을 제안해주세요:

1. **현재 상황 분석** (2-3줄)
2. **핵심 전략 방향** (3가지)
3. **즉시 실행 가능한 액션 플랜** (구체적인 실행 방법 5가지)
4. **SNS 마케팅 전략** (플랫폼별 구체적 방안)
5. **고객 관리 전략** (리텐션 및 신규 유치)
6. **개선 우선순위** (가장 시급한 3가지)
7. **성과 측정 방법** (KPI 및 목표 수치)

마케팅 전략은 실제로 키즈카페 사장이 바로 적용할 수 있도록 구체적이고 실용적으로 작성해주세요.
"""
        
        return prompt
    
    def _call_gemini_api(self, prompt):
        """Gemini API 호출"""
        url = f"{self.base_url}?key={self.api_key}"
        
        print(f"🔗 API URL: {url[:50]}...") # API URL 확인
        print(f"🔑 API Key: {self.api_key[:10]}...{self.api_key[-5:]}") # API 키 일부 확인
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048,
            }
        }
        
        print("📤 API 호출 중...")
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            print(f"📊 응답 상태: {response.status_code}")
            print(f"📄 응답 내용: {response.text[:500]}...")
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    generated_text = result['candidates'][0]['content']['parts'][0]['text']
                    return self._format_strategy_output(generated_text)
                else:
                    raise Exception(f"API 응답에 생성된 텍스트가 없습니다: {result}")
            else:
                raise Exception(f"API 호출 실패: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            raise Exception("API 호출 시간 초과 (30초)")
        except requests.exceptions.ConnectionError:
            raise Exception("네트워크 연결 실패")
        except Exception as e:
            raise Exception(f"API 호출 중 오류: {str(e)}")
    
    def _format_strategy_output(self, generated_text):
        """AI 생성 전략을 마크다운 형식으로 포맷팅"""
        current_date = datetime.now().strftime('%Y년 %m월 %d일')
        
        formatted_strategy = f"""# 🤖 AI 생성 마케팅 전략 보고서

**생성일**: {current_date}
**분석 대상**: 우리끼리 키즈카페 대전문화점
**생성 모델**: Google Gemini Pro

---

{generated_text}

---

> 💡 **AI 생성 전략**: 이 전략은 Google Gemini AI가 실제 고객 리뷰를 분석하여 생성한 맞춤형 마케팅 전략입니다.
"""
        
        return formatted_strategy
    
    def _generate_fallback_strategy(self, summary):
        """API 실패시 기본 전략 반환"""
        return f"""# 📊 키즈카페 마케팅 전략 보고서 (기본 분석)

**생성일**: {datetime.now().strftime('%Y년 %m월 %d일')}
**총 리뷰 수**: {summary['total_reviews']}개

## 현재 상황
- 긍정 리뷰 비율: {summary['positive_ratio']}%
- 부정 리뷰 비율: {summary['negative_ratio']}%

## 기본 전략 제안
1. 고객 만족도 향상을 위한 서비스 개선
2. 긍정적 후기 확산을 위한 SNS 마케팅
3. 정기적인 고객 피드백 수집 및 대응

⚠️ **주의**: Gemini API 연결 실패로 기본 전략이 제공되었습니다.
API 키를 확인하고 다시 시도해주세요.
"""

if __name__ == "__main__":
    # 테스트 실행
    print("🤖 Gemini AI 마케팅 전략 생성기 테스트")
    
    # 테스트용 더미 데이터
    test_reviews = [
        {
            "title": "우리끼리 키즈카페 후기",
            "content": "아이들이 정말 좋아해요! 깨끗하고 안전합니다.",
            "sentiment": "positive",
            "positive_keywords": ["좋아", "깨끗", "안전"],
            "negative_keywords": []
        }
    ]
    
    try:
        strategist = GeminiMarketingStrategist()
        strategy = strategist.generate_marketing_strategy(test_reviews)
        print("\n✅ AI 전략 생성 성공!")
        print(strategy[:300] + "...")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")