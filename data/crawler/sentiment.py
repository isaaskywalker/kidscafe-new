# sentiment.py - 감정 분석 모듈
import re
from collections import Counter

def analyze_sentiment(text: str) -> dict:
    """
    입력된 텍스트의 감정을 분석하여 상세한 결과를 반환합니다.
    
    Returns:
        dict: {
            'sentiment': 'positive'|'negative'|'neutral',
            'confidence': float,
            'reasoning': str,
            'positive_keywords': list,
            'negative_keywords': list
        }
    """
    
    # 긍정적 키워드 (더 포괄적으로)
    positive_keywords = [
        '좋다', '좋아요', '좋았어요', '추천', '깨끗', '친절', '만족', '훌륭',
        '최고', '완벽', '재미있', '즐거', '행복', '사랑', '감동', '대박',
        '멋지', '신나', '괜찮', '나쁘지않', '편리', '안전', '넓', '다양',
        '시설', '굿', '짱', '웃음', '기쁘', '좋네', '맘에들', '예쁘'
    ]
    
    # 부정적 키워드 (더 포괄적으로)
    negative_keywords = [
        '별로', '나쁘', '불편', '아쉽', '실망', '더럽', '불친절', '비싸',
        '작다', '좁', '시끄럽', '위험', '냄새', '짜증', '화', '엉망',
        '최악', '문제', '고장', '망했', '불만', '개선', '아니다', '싫',
        '힘들', '어려', '복잡', '지저분', '관리안됨', '별점낮', '추천안함'
    ]
    
    # 텍스트 전처리
    text_lower = text.lower()
    
    # 키워드 매칭
    found_positive = [kw for kw in positive_keywords if kw in text_lower]
    found_negative = [kw for kw in negative_keywords if kw in text_lower]
    
    positive_count = len(found_positive)
    negative_count = len(found_negative)
    
    # 감정 판단 로직
    if positive_count > negative_count:
        sentiment = 'positive'
        confidence = min(0.95, 0.6 + (positive_count - negative_count) * 0.1)
        reasoning = f"긍정 키워드 {positive_count}개 발견: {', '.join(found_positive[:3])}"
        
    elif negative_count > positive_count:
        sentiment = 'negative'
        confidence = min(0.95, 0.6 + (negative_count - positive_count) * 0.1)
        reasoning = f"부정 키워드 {negative_count}개 발견: {', '.join(found_negative[:3])}"
        
    else:
        sentiment = 'neutral'
        confidence = 0.5
        reasoning = f"긍정({positive_count})과 부정({negative_count}) 키워드 균형"
    
    return {
        'sentiment': sentiment,
        'confidence': round(confidence, 2),
        'reasoning': reasoning,
        'positive_keywords': found_positive,
        'negative_keywords': found_negative
    }

def analyze_sentiment_simple(text: str) -> str:
    """
    간단한 감정 분석 (기존 함수와 호환)
    """
    result = analyze_sentiment(text)
    return result['sentiment']

def batch_analyze_reviews(reviews: list) -> list:
    """
    여러 리뷰를 한번에 감정 분석
    
    Args:
        reviews: [{'title': str, 'content': str, ...}, ...]
    
    Returns:
        list: 감정 분석 결과가 추가된 리뷰 리스트
    """
    analyzed_reviews = []
    
    for review in reviews:
        # 제목과 내용을 합쳐서 분석
        full_text = f"{review.get('title', '')} {review.get('content', '')}"
        
        # 감정 분석 실행
        sentiment_result = analyze_sentiment(full_text)
        
        # 기존 리뷰에 감정 분석 결과 추가
        analyzed_review = review.copy()
        analyzed_review.update({
            'sentiment': sentiment_result['sentiment'],
            'sentiment_confidence': sentiment_result['confidence'],
            'sentiment_reasoning': sentiment_result['reasoning'],
            'positive_keywords': sentiment_result['positive_keywords'],
            'negative_keywords': sentiment_result['negative_keywords']
        })
        
        analyzed_reviews.append(analyzed_review)
    
    return analyzed_reviews

def get_sentiment_summary(reviews: list) -> dict:
    """
    리뷰들의 감정 분석 요약 통계
    """
    if not reviews:
        return {}
    
    sentiments = [r.get('sentiment', 'neutral') for r in reviews]
    sentiment_counts = Counter(sentiments)
    
    total = len(reviews)
    positive_ratio = sentiment_counts.get('positive', 0) / total * 100
    negative_ratio = sentiment_counts.get('negative', 0) / total * 100
    neutral_ratio = sentiment_counts.get('neutral', 0) / total * 100
    
    # 전체 키워드 통계
    all_positive_keywords = []
    all_negative_keywords = []
    
    for review in reviews:
        all_positive_keywords.extend(review.get('positive_keywords', []))
        all_negative_keywords.extend(review.get('negative_keywords', []))
    
    top_positive = Counter(all_positive_keywords).most_common(5)
    top_negative = Counter(all_negative_keywords).most_common(5)
    
    return {
        'total_reviews': total,
        'positive_count': sentiment_counts.get('positive', 0),
        'negative_count': sentiment_counts.get('negative', 0),
        'neutral_count': sentiment_counts.get('neutral', 0),
        'positive_ratio': round(positive_ratio, 1),
        'negative_ratio': round(negative_ratio, 1),
        'neutral_ratio': round(neutral_ratio, 1),
        'top_positive_keywords': top_positive,
        'top_negative_keywords': top_negative
    }

if __name__ == "__main__":  # 🔥 수정된 부분
    # 테스트 실행
    print("=== 감정 분석 테스트 ===")
    
    test_cases = [
        "시설이 깨끗하고 좋아요! 아이들이 정말 좋아해요 추천합니다",
        "주차가 불편했어요. 시설도 별로고 직원도 불친절해요",
        "그냥 그랬어요. 보통 수준입니다",
        "우리끼리 키즈카페 대전문화점 정말 최고예요! 깨끗하고 안전하고 아이들이 즐거워해요"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n--- 테스트 {i} ---")
        print(f"텍스트: {text}")
        
        result = analyze_sentiment(text)
        print(f"감정: {result['sentiment']}")
        print(f"신뢰도: {result['confidence']}")
        print(f"근거: {result['reasoning']}")
        
        # 간단한 버전도 테스트
        simple_result = analyze_sentiment_simple(text)
        print(f"간단 분석: {simple_result}")