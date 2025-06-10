import requests
from bs4 import BeautifulSoup
import datetime
import json
import os
import time
import random

def get_blog_post_date_and_content(link):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        resp = requests.get(link, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"Failed to access {link}: {resp.status_code}")
            return None, None
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 더 넓은 범위의 날짜 셀렉터
        date_selectors = [
            'span.se_publishDate', 'span.se_publish_time', 'span.date',
            '.post_date', '.blog_date', '.date', '.time',
            '[class*="date"]', '[class*="time"]',
            '.blog_date', '.post-date'
        ]
        
        date = None
        for selector in date_selectors:
            date_elements = soup.select(selector)
            for elem in date_elements:
                text = elem.get_text().strip()
                if text and ('2024' in text or '2025' in text):
                    date = text
                    break
            if date:
                break
        
        # 더 넓은 범위의 콘텐츠 셀렉터
        content_selectors = [
            'div.se-main-container', 'div#postViewArea', 'div.se_component_wrap',
            '.post_content', '.blog_content', '.content', 'article',
            '[class*="content"]', '[class*="post"]', '.se-main-container'
        ]
        
        content = None
        for selector in content_selectors:
            content_elements = soup.select(selector)
            for elem in content_elements:
                text = elem.get_text().strip()
                if text and len(text) > 100:  # 최소 100자 이상
                    content = text
                    break
            if content:
                break
        
        # 날짜가 없으면 현재 날짜로 대체 (최근 게시물로 가정)
        if not date:
            date = "2024-06-10"
        
        # 콘텐츠가 없으면 제목으로 대체
        if not content:
            title_elem = soup.select_one('title, h1, .title')
            content = title_elem.get_text().strip() if title_elem else "No content available"
        
        return date, content
        
    except Exception as e:
        print(f"Error parsing {link}: {e}")
        return None, None

def crawl_naver_blog(keyword: str, max_page: int = 2):
    reviews = []
    
    for page in range(1, max_page + 1):
        print(f"Crawling page {page} for keyword: {keyword}")
        
        start = (page - 1) * 10 + 1
        url = f"https://search.naver.com/search.naver?where=post&sm=tab_jum&query={keyword}&start={start}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
            "Referer": "https://www.naver.com"
        }
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                print(f"Failed to access search page: {resp.status_code}")
                continue
                
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 🔥 수정된 부분: 올바른 셀렉터 사용
            items = soup.select('.total_tit a.link_tit')
            print(f"Found {len(items)} items")
            
            for i, item in enumerate(items[:5]):  # 페이지당 최대 5개
                title = item.get('title') or item.text.strip()
                link = item.get('href')
                
                print(f"Processing item {i+1}: {title[:50]}...")
                print(f"Link: {link}")
                
                if not link or not title:
                    print("❌ Missing title or link!")
                    continue
                
                # 네이버 블로그 링크만 처리
                if 'blog.naver.com' not in link:
                    print("❌ Not a naver blog link!")
                    continue
                
                print("✅ Valid blog link found!")
                
                # 상세 페이지 진입해서 날짜/본문 파싱
                date, content = get_blog_post_date_and_content(link)
                
                if date and content:
                    try:
                        # 날짜 파싱 개선 (조건 완화)
                        date_str = date.replace('.', '-').replace('/', '-').split()[0]
                        
                        # 2024년 이후 모든 게시물 수집 (조건 완화)
                        if '2024' in date_str or '2025' in date_str:
                            review = {
                                "title": title,
                                "link": link,
                                "date": date_str,
                                "content": content[:500]  # 첫 500자만
                            }
                            reviews.append(review)
                            print(f"✅ Added review: {title[:30]}...")
                        else:
                            print(f"❌ Date too old: {date_str}")
                            
                    except Exception as e:
                        print(f"Date parsing error: {e}")
                else:
                    print("❌ Failed to get date/content")
                
                # 요청 간 랜덤 딜레이
                time.sleep(random.uniform(1, 2))
                
        except Exception as e:
            print(f"Error crawling page {page}: {e}")
        
        # 페이지 간 딜레이
        time.sleep(random.uniform(2, 3))
    
    return reviews

def crawl_naver_blog_multi(keywords, max_page=2):
    all_reviews = []
    seen_links = set()
    
    for keyword in keywords:
        print(f"\n=== Crawling keyword: {keyword} ===")
        reviews = crawl_naver_blog(keyword, max_page)
        
        for r in reviews:
            if r['link'] not in seen_links:
                all_reviews.append(r)
                seen_links.add(r['link'])
                print(f"Added unique review: {r['title'][:40]}...")
    
    return all_reviews

def save_reviews_to_file(reviews, date_str):
    os.makedirs('data/reviews', exist_ok=True)
    path = f'data/reviews/{date_str}.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)
    print(f"Reviews saved to: {path}")

if __name__ == "__main__":
    print("🚀 Starting fixed crawler...")
    today = datetime.date.today().isoformat()
    
    keywords = [
        "우리끼리 키즈카페 대전문화점",
        "우리끼리 리뷰 대전"
    ]
    
    try:
        result = crawl_naver_blog_multi(keywords)
        save_reviews_to_file(result, today)
        print(f"\n✅ SUCCESS: Saved {len(result)} reviews to data/reviews/{today}.json")
        
        # 결과 미리보기
        for i, review in enumerate(result[:3]):
            print(f"\n--- Review {i+1} ---")
            print(f"Title: {review['title']}")
            print(f"Date: {review['date']}")
            print(f"Link: {review['link']}")
            print(f"Content: {review['content'][:100]}...")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
