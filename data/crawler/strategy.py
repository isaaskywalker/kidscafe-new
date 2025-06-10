# strategy.py - 마케팅 전략 생성 모듈
import json
import os
from datetime import datetime
from sentiment import get_sentiment_summary

def generate_marketing_strategy(reviews: list) -> str:
    """리뷰 분석 기반 AI 마케팅 전략 생성"""
    if not reviews:
        return "리뷰가 없어서 마케팅 전략을 생성할 수 없습니다."
    
    try:
        # Gemini AI 사용 시도
        from gemini_api import GeminiMarketingStrategist
        
        strategist = GeminiMarketingStrategist()
        ai_strategy = strategist.generate_marketing_strategy(reviews)
        return ai_strategy
        
    except Exception as e:
        print(f"⚠️ AI 전략 생성 실패: {e}")
        print("📊 기본 분석 전략으로 대체합니다...")
        
        # 기본 분석으로 대체
        return generate_basic_marketing_strategy(reviews)

def generate_basic_marketing_strategy(reviews: list) -> str:
    """기본 규칙 기반 마케팅 전략 (AI 실패시 대체)"""
    # 감정 분석 요약 통계
    summary = get_sentiment_summary(reviews)
    
    strategy = f"""# 📊 우리끼리 키즈카페 대전문화점 마케팅 전략 보고서

**생성일**: {datetime.now().strftime('%Y년 %m월 %d일')}
**분석 기간**: 2025년 6월 이후 작성된 리뷰
**총 리뷰 수**: {summary['total_reviews']}개
**분석 방식**: 기본 규칙 기반 분석

## 🎯 리뷰 감정 분석 결과

### 전체 감정 분포
- **긍정적 리뷰**: {summary['positive_count']}개 ({summary['positive_ratio']}%)
- **부정적 리뷰**: {summary['negative_count']}개 ({summary['negative_ratio']}%)
- **중립적 리뷰**: {summary['neutral_count']}개 ({summary['neutral_ratio']}%)

### 고객 만족도 지표
"""
    
    # 만족도 판단
    if summary['positive_ratio'] >= 70:
        satisfaction_level = "매우 높음"
        satisfaction_emoji = "🟢"
    elif summary['positive_ratio'] >= 50:
        satisfaction_level = "양호"
        satisfaction_emoji = "🟡"
    else:
        satisfaction_level = "개선 필요"
        satisfaction_emoji = "🔴"
    
    strategy += f"**고객 만족도**: {satisfaction_emoji} {satisfaction_level} ({summary['positive_ratio']}%)\n\n"
    
    # 주요 키워드 분석
    if summary['top_positive_keywords']:
        strategy += "### 🔥 고객들이 가장 좋아하는 점\n"
        for keyword, count in summary['top_positive_keywords']:
            strategy += f"- **{keyword}**: {count}회 언급\n"
        strategy += "\n"
    
    if summary['top_negative_keywords']:
        strategy += "### ⚠️ 개선이 필요한 점\n"
        for keyword, count in summary['top_negative_keywords']:
            strategy += f"- **{keyword}**: {count}회 언급\n"
        strategy += "\n"
    
    # 전략적 제안
    strategy += """## 🚀 마케팅 전략 제안

### 1. 즉시 실행 가능한 전략
"""
    
    if summary['positive_ratio'] > summary['negative_ratio']:
        strategy += """
#### 🎯 강점 극대화 전략
- **긍정 리뷰 활용**: 고객 후기를 SNS 및 매장 내 적극 게시
- **입소문 마케팅**: 만족한 고객들의 추천 이벤트 진행
- **리뷰 인센티브**: 네이버/구글 리뷰 작성 고객 대상 할인 혜택
"""
    else:
        strategy += """
#### 🔧 개선 우선 전략  
- **즉시 개선**: 부정적 피드백 사항 우선 해결
- **고객 소통**: 불만 고객 직접 연락하여 관계 회복
- **서비스 교육**: 직원 친절 서비스 교육 강화
"""
    
    strategy += """
### 2. 콘텐츠 마케팅 전략

#### 📱 SNS 활용 방안
- **인스타그램**: 아이들 놀이 모습 릴스 제작
- **네이버 블로그**: 키즈카페 이용 팁 포스팅
- **유튜브**: 시설 투어 및 놀이 가이드 영상

#### 🏷️ 해시태그 전략
- #우리끼리대전문화점
- #대전키즈카페
- #무인키즈카페
- #아이와함께대전

### 3. 고객 관리 전략

#### 🎁 프로모션 아이디어
- **신규 고객**: 첫 방문 할인 쿠폰
- **단골 고객**: VIP 멤버십 프로그램
- **생일 이벤트**: 아이 생일 기념 무료 이용권
- **리뷰 이벤트**: 포토 리뷰 작성시 다음 방문 할인

#### 📊 고객 피드백 시스템
- **정기 설문**: 월 1회 고객 만족도 조사
- **즉시 대응**: 부정적 리뷰 24시간 내 답변
- **개선 공지**: 고객 건의사항 반영 결과 공유

### 4. 시설 및 서비스 개선 방안
"""
    
    # 부정적 키워드 기반 개선 방안
    if summary['top_negative_keywords']:
        strategy += "\n#### 🔧 우선 개선 항목\n"
        for keyword, count in summary['top_negative_keywords'][:3]:
            if keyword in ['더럽', '청소', '냄새']:
                strategy += f"- **청결 관리**: {keyword} 관련 불만 해결을 위한 청소 횟수 증가\n"
            elif keyword in ['불친절', '직원']:
                strategy += f"- **서비스 교육**: {keyword} 관련 직원 교육 프로그램 강화\n"
            elif keyword in ['비싸', '가격']:
                strategy += f"- **가격 정책**: {keyword} 관련 합리적 요금제 검토\n"
            else:
                strategy += f"- **{keyword} 개선**: 고객 불만 사항 즉시 해결\n"
    
    strategy += """
### 5. 성과 측정 및 모니터링

#### 📈 KPI 지표
- **리뷰 평점**: 월평균 4.0점 이상 목표
- **긍정 리뷰 비율**: 70% 이상 유지
- **신규 고객 비율**: 월 20% 이상
- **재방문율**: 60% 이상

#### 🔍 모니터링 계획
- **일간**: 새로운 리뷰 확인 및 대응
- **주간**: 고객 만족도 트렌드 분석
- **월간**: 마케팅 성과 평가 및 전략 수정

---

> ⚠️ **참고**: 이 전략은 기본 분석으로 생성되었습니다. 
> 더 정교한 AI 전략을 원하시면 Gemini API 키를 설정해주세요.
"""
    
    return strategy

def save_strategy_to_file(strategy: str, date_str: str) -> str:
    """마케팅 전략을 파일로 저장"""
    os.makedirs('data/strategies', exist_ok=True)
    path = f'data/strategies/{date_str}_marketing_strategy.md'
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(strategy)
    
    print(f"✅ Marketing strategy saved to: {path}")
    return path

def load_reviews_and_generate_strategy(reviews_file_path: str) -> str:
    """리뷰 파일을 읽어서 마케팅 전략 생성"""
    try:
        with open(reviews_file_path, 'r', encoding='utf-8') as f:
            reviews = json.load(f)
        
        strategy = generate_marketing_strategy(reviews)
        return strategy
        
    except FileNotFoundError:
        return "리뷰 파일을 찾을 수 없습니다."
    except json.JSONDecodeError:
        return "리뷰 파일을 읽는 중 오류가 발생했습니다."

if __name__ == "__main__":
    print("🎯 마케팅 전략 생성기")
    
    # 최신 리뷰 파일 찾기 (여러 형태 지원)
    from datetime import date
    today = date.today().isoformat()
    
    # 가능한 파일 경로들 (우선순위대로)
    possible_paths = [
        f'data/reviews/{today}_iframe.json',  # iframe 크롤러 결과
        f'data/reviews/{today}_simple.json',  # 간소화 크롤러 결과
        f'data/reviews/{today}.json'          # 기본 크롤러 결과
    ]
    
    reviews_path = None
    for path in possible_paths:
        if os.path.exists(path):
            reviews_path = path
            break
    
    if reviews_path:
        print(f"📂 리뷰 파일 발견: {reviews_path}")
        
        # 리뷰 개수 확인
        try:
            with open(reviews_path, 'r', encoding='utf-8') as f:
                reviews = json.load(f)
            print(f"📊 총 {len(reviews)}개 리뷰 분석 예정")
        except:
            print("❌ 리뷰 파일 읽기 실패")
            exit()
        
        # 마케팅 전략 생성
        strategy = load_reviews_and_generate_strategy(reviews_path)
        
        # 전략 저장
        strategy_path = save_strategy_to_file(strategy, today)
        
        # 미리보기
        print("\n" + "="*60)
        print("📊 마케팅 전략 미리보기")
        print("="*60)
        print(strategy[:1000] + "...")
        print(f"\n✅ 완료! 전략 파일: {strategy_path}")
        
    else:
        print("❌ 리뷰 파일이 없습니다.")
        print("다음 중 하나를 먼저 실행하세요:")
        print("  - fixed_iframe_crawler.py (권장)")
        print("  - simplified_crawler.py")
        print("  - crawler.py")