# crawler/gemini_api.py - Gemini AI 마케팅 전략 생성 (저장 기능 포함)
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
        
        # gemini-1.5-flash 모델 사용 (최신)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        # 저장 디렉토리 생성
        self.ensure_directories()
    
    def ensure_directories(self):
        """필요한 디렉토리들을 생성"""
        directories = [
            'data',
            'data/reviews',
            'data/strategies',
            'data/crawler'
        ]
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"📁 디렉토리 확인: {directory}")
            except Exception as e:
                print(f"❌ 디렉토리 생성 실패 {directory}: {e}")
    
    def generate_and_save_strategy(self, reviews_data):
        """리뷰 데이터를 바탕으로 AI 마케팅 전략 생성 및 저장"""
        print("🤖 마케팅 전략 생성 시작...")
        
        # 전략 생성
        strategy = self.generate_marketing_strategy(reviews_data)
        
        # 전략 저장
        saved_files = self.save_strategy(strategy, reviews_data)
        
        print(f"✅ 전략 생성 및 저장 완료!")
        for file_path in saved_files:
            print(f"📄 저장된 파일: {file_path}")
        
        return strategy, saved_files
    
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
    
    def save_strategy(self, strategy_text, reviews_data):
        """생성된 전략을 파일로 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        saved_files = []
        
        try:
            # 1. 마크다운 파일로 저장
            md_filename = f"marketing_strategy_{timestamp}.md"
            md_path = os.path.join('data', 'strategies', md_filename)
            
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(strategy_text)
            
            saved_files.append(md_path)
            print(f"📝 마크다운 저장: {md_path}")
            
            # 2. JSON 데이터로 저장
            json_filename = f"strategy_data_{timestamp}.json"
            json_path = os.path.join('data', 'strategies', json_filename)
            
            strategy_data = {
                'timestamp': timestamp,
                'generated_at': datetime.now().isoformat(),
                'strategy_markdown': strategy_text,
                'review_count': len(reviews_data) if reviews_data else 0,
                'reviews_analyzed': reviews_data[:3] if reviews_data else [],  # 처음 3개만
                'api_used': bool(self.api_key),
                'model': 'gemini-1.5-flash',
                'file_info': {
                    'markdown_file': md_filename,
                    'json_file': json_filename
                }
            }
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(strategy_data, f, ensure_ascii=False, indent=2)
            
            saved_files.append(json_path)
            print(f"💾 JSON 저장: {json_path}")
            
            # 3. 최신 전략을 latest.md로도 저장
            latest_path = os.path.join('data', 'strategies', 'latest.md')
            with open(latest_path, 'w', encoding='utf-8') as f:
                f.write(strategy_text)
            
            saved_files.append(latest_path)
            print(f"🔄 최신 전략 저장: {latest_path}")
            
        except Exception as e:
            print(f"❌ 저장 실패: {e}")
            
        return saved_files
    
    def load_reviews_from_file(self, file_path):
        """파일에서 리뷰 데이터를 불러오기"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reviews = json.load(f)
            print(f"📖 리뷰 데이터 로드: {file_path} ({len(reviews)}개)")
            return reviews
        except Exception as e:
            print(f"❌ 리뷰 파일 로드 실패: {e}")
            return []
    
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
{', '.join([f"{kw}({cnt}회)" for kw, cnt in summary['top_positive_keywords']]) if summary['top_positive_keywords'] else '데이터 없음'}

### 개선이 필요한 점
{', '.join([f"{kw}({cnt}회)" for kw, cnt in summary['top_negative_keywords']]) if summary['top_negative_keywords'] else '데이터 없음'}

### 주요 리뷰 내용
"""
        
        if summary['key_reviews']:
            for i, review in enumerate(summary['key_reviews'], 1):
                prompt += f"""
{i}. [{review['sentiment']}] {review['title']}
   "{review['content']}"
"""
        else:
            prompt += "\n리뷰 데이터가 없습니다."
        
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
        """Gemini API 호출 (개선된 오류 처리)"""
        url = f"{self.base_url}?key={self.api_key}"
        
        # API 키 확인 (보안을 위해 일부만 표시)
        if len(self.api_key) > 10:
            masked_key = f"{self.api_key[:10]}...{self.api_key[-5:]}"
        else:
            masked_key = f"{self.api_key[:3]}***"
            
        print(f"🔑 API Key 확인: {masked_key}")
        print("🤖 모델: gemini-1.5-flash")
        
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
            response = requests.post(url, headers=headers, json=data, timeout=60)
            
            print(f"📊 응답 상태: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ API 호출 성공!")
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        generated_text = candidate['content']['parts'][0]['text']
                        return self._format_strategy_output(generated_text)
                    else:
                        raise Exception(f"응답 구조가 예상과 다릅니다: {result}")
                else:
                    raise Exception(f"API 응답에 생성된 텍스트가 없습니다: {result}")
            
            elif response.status_code == 400:
                error_detail = response.json()
                raise Exception(f"잘못된 요청 (400): {error_detail}")
            
            elif response.status_code == 403:
                raise Exception("API 키가 유효하지 않거나 권한이 없습니다 (403)")
            
            elif response.status_code == 429:
                raise Exception("API 호출 한도를 초과했습니다 (429)")
            
            else:
                raise Exception(f"API 호출 실패: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            raise Exception("API 호출 시간 초과 (60초)")
        except requests.exceptions.ConnectionError:
            raise Exception("네트워크 연결 실패")
        except json.JSONDecodeError:
            raise Exception(f"응답 JSON 파싱 실패: {response.text[:200]}...")
        except Exception as e:
            raise Exception(f"API 호출 중 오류: {str(e)}")
    
    def _format_strategy_output(self, generated_text):
        """AI 생성 전략을 마크다운 형식으로 포맷팅"""
        current_date = datetime.now().strftime('%Y년 %m월 %d일')
        
        formatted_strategy = f"""# 🤖 AI 생성 마케팅 전략 보고서

**생성일**: {current_date}
**분석 대상**: 우리끼리 키즈카페 대전문화점
**생성 모델**: Google Gemini 1.5 Flash

---

{generated_text}

---

> 💡 **AI 생성 전략**: 이 전략은 Google Gemini 1.5 Flash가 실제 고객 리뷰를 분석하여 생성한 맞춤형 마케팅 전략입니다.
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

def main():
    """메인 실행 함수"""
    print("🚀 키즈카페 마케팅 전략 생성기 (Gemini 1.5 Flash)")
    print("=" * 60)
    
    # Gemini 전략가 초기화
    strategist = GeminiMarketingStrategist()
    
    # 리뷰 데이터 로드 시도
    review_files = [
        'data/reviews/reviews.json',
        'data/crawler/reviews.json',
        'reviews.json',
        '../data/reviews/reviews.json'
    ]
    
    reviews_data = []
    used_file = None
    
    for file_path in review_files:
        if os.path.exists(file_path):
            reviews_data = strategist.load_reviews_from_file(file_path)
            if reviews_data:
                used_file = file_path
                break
    
    # 리뷰 데이터가 없으면 테스트 데이터 사용
    if not reviews_data:
        print("📋 실제 리뷰 데이터가 없어 테스트 데이터를 사용합니다.")
        reviews_data = [
            {
                "title": "우리끼리 키즈카페 후기",
                "content": "아이들이 정말 좋아해요! 깨끗하고 안전합니다.",
                "sentiment": "positive",
                "positive_keywords": ["좋아", "깨끗", "안전"],
                "negative_keywords": [],
                "date": "2024-06-10"
            },
            {
                "title": "재방문 의사",
                "content": "시설이 좋고 아이가 재미있어 해요. 다시 올 예정입니다.",
                "sentiment": "positive", 
                "positive_keywords": ["좋고", "재미있어", "다시"],
                "negative_keywords": [],
                "date": "2024-06-09"
            }
        ]
        used_file = "테스트 데이터"
    
    print(f"📊 데이터 소스: {used_file}")
    print(f"📈 분석할 리뷰: {len(reviews_data)}개")
    print("=" * 60)
    
    # 마케팅 전략 생성 및 저장
    try:
        strategy, saved_files = strategist.generate_and_save_strategy(reviews_data)
        
        print("\n" + "=" * 60)
        print("🎉 마케팅 전략 생성 및 저장 완료!")
        print(f"📁 저장된 파일: {len(saved_files)}개")
        
        for file_path in saved_files:
            print(f"  📄 {file_path}")
        
        # 전략 미리보기
        print("\n📖 전략 미리보기:")
        print("-" * 40)
        preview_lines = strategy.split('\n')[:12]
        for line in preview_lines:
            print(line)
        print("...")
        print("-" * 40)
        
        print(f"\n💡 전체 전략 확인: data/strategies/latest.md")
        
    except Exception as e:
        print(f"❌ 전략 생성 실패: {e}")
        print("\n🔧 문제 해결 방법:")
        print("  1. GEMINI_API_KEY 환경변수 설정 확인")
        print("  2. 인터�net 연결 상태 확인")
        print("  3. Google AI Studio에서 API 키 재발급")

if __name__ == "__main__":
    main()
