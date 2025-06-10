// pages/index.js - 핑크색 키즈카페 대시보드
import { useState } from 'react';
import Head from 'next/head';

export default function Dashboard({ reviews, strategy }) {
  const [activeTab, setActiveTab] = useState('overview');

  // 감정 분석 통계 계산
  const getSentimentStats = () => {
    if (!reviews || reviews.length === 0) return null;
    
    const positive = reviews.filter(r => r.sentiment === 'positive').length;
    const negative = reviews.filter(r => r.sentiment === 'negative').length;
    const neutral = reviews.filter(r => r.sentiment === 'neutral').length;
    const total = reviews.length;
    
    return {
      positive: { count: positive, percentage: total > 0 ? ((positive / total) * 100).toFixed(1) : 0 },
      negative: { count: negative, percentage: total > 0 ? ((negative / total) * 100).toFixed(1) : 0 },
      neutral: { count: neutral, percentage: total > 0 ? ((neutral / total) * 100).toFixed(1) : 0 },
      total
    };
  };

  const stats = getSentimentStats();

  return (
    <div className="min-h-screen pink-gradient-bg">
      <Head>
        <title>🎀 우리끼리 키즈카페 마케팅 대시보드</title>
        <meta name="description" content="실시간 리뷰 분석 및 마케팅 전략" />
      </Head>

      {/* 헤더 */}
      <header className="bg-white shadow-lg" style={{ backgroundColor: '#fff0f5' }}>
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold" style={{ color: '#d63384' }}>
              🎀 우리끼리 키즈카페 대전문화점
            </h1>
            <p className="text-xl mt-3" style={{ color: '#c2185b' }}>
              실시간 리뷰 분석 및 마케팅 전략 대시보드
            </p>
            <div className="mt-4 flex justify-center space-x-4">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-pink-100 text-pink-800">
                💖 Live Analytics
              </span>
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800">
                🚀 AI Strategy
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* 네비게이션 */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-center space-x-12">
            {[
              { id: 'overview', name: '대시보드', icon: '📊' },
              { id: 'reviews', name: '리뷰 분석', icon: '💬' },
              { id: 'strategy', name: '마케팅 전략', icon: '🎯' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-6 border-b-4 font-bold text-lg transition-all duration-200 ${
                  activeTab === tab.id
                    ? 'border-pink-400 text-pink-600 bg-pink-50'
                    : 'border-transparent text-gray-600 hover:text-pink-500 hover:bg-pink-25'
                }`}
              >
                {tab.icon} {tab.name}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* 메인 콘텐츠 */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* 통계 카드 */}
            {stats && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-white rounded-2xl shadow-lg p-6 border-l-4 border-pink-400">
                  <div className="flex items-center">
                    <div className="p-3 bg-pink-100 rounded-full">
                      <span className="text-3xl">📊</span>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">총 리뷰</p>
                      <p className="text-3xl font-bold text-pink-600">{stats.total}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-2xl shadow-lg p-6 border-l-4 border-green-400">
                  <div className="flex items-center">
                    <div className="p-3 bg-green-100 rounded-full">
                      <span className="text-3xl">😊</span>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">긍정적</p>
                      <p className="text-2xl font-bold text-green-600">
                        {stats.positive.count} <span className="text-lg">({stats.positive.percentage}%)</span>
                      </p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-2xl shadow-lg p-6 border-l-4 border-red-400">
                  <div className="flex items-center">
                    <div className="p-3 bg-red-100 rounded-full">
                      <span className="text-3xl">😞</span>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">부정적</p>
                      <p className="text-2xl font-bold text-red-600">
                        {stats.negative.count} <span className="text-lg">({stats.negative.percentage}%)</span>
                      </p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-2xl shadow-lg p-6 border-l-4 border-gray-400">
                  <div className="flex items-center">
                    <div className="p-3 bg-gray-100 rounded-full">
                      <span className="text-3xl">😐</span>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">중립적</p>
                      <p className="text-2xl font-bold text-gray-600">
                        {stats.neutral.count} <span className="text-lg">({stats.neutral.percentage}%)</span>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 만족도 차트 */}
            {stats && (
              <div className="bg-white rounded-2xl shadow-lg p-8">
                <h3 className="text-2xl font-bold text-pink-600 mb-6 text-center">
                  💖 고객 만족도 분포
                </h3>
                <div className="space-y-6">
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-lg font-medium text-green-600">😊 긍정적</span>
                      <span className="text-lg font-bold text-green-600">{stats.positive.count}개 ({stats.positive.percentage}%)</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div 
                        className="bg-gradient-to-r from-green-400 to-green-500 h-4 rounded-full transition-all duration-500" 
                        style={{ width: `${stats.positive.percentage}%` }}
                      ></div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-lg font-medium text-red-600">😞 부정적</span>
                      <span className="text-lg font-bold text-red-600">{stats.negative.count}개 ({stats.negative.percentage}%)</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div 
                        className="bg-gradient-to-r from-red-400 to-red-500 h-4 rounded-full transition-all duration-500" 
                        style={{ width: `${stats.negative.percentage}%` }}
                      ></div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-lg font-medium text-gray-600">😐 중립적</span>
                      <span className="text-lg font-bold text-gray-600">{stats.neutral.count}개 ({stats.neutral.percentage}%)</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div 
                        className="bg-gradient-to-r from-gray-400 to-gray-500 h-4 rounded-full transition-all duration-500" 
                        style={{ width: `${stats.neutral.percentage}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'reviews' && (
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-3xl font-bold text-pink-600">💬 최신 리뷰 분석</h2>
              <p className="text-gray-600 mt-2">고객들의 생생한 후기를 분석했습니다</p>
            </div>
            
            {reviews && reviews.length > 0 ? (
              <div className="grid gap-6">
                {reviews.map((review, index) => (
                  <div key={index} className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-gray-900 mb-3">
                          {review.title}
                        </h3>
                        <p className="text-gray-700 mb-4 leading-relaxed">
                          {review.content}
                        </p>
                        <div className="flex items-center space-x-4 text-sm text-gray-500">
                          <span className="flex items-center">
                            📅 {review.date}
                          </span>
                          <a 
                            href={review.link} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-pink-600 hover:text-pink-800 font-medium"
                          >
                            원문 보기 →
                          </a>
                        </div>
                      </div>
                      <div className="ml-6 flex flex-col items-end">
                        <span className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-bold ${
                          review.sentiment === 'positive' 
                            ? 'bg-green-100 text-green-800'
                            : review.sentiment === 'negative'
                            ? 'bg-red-100 text-red-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {review.sentiment === 'positive' ? '😊 긍정적' :
                           review.sentiment === 'negative' ? '😞 부정적' : '😐 중립적'}
                        </span>
                        <span className="text-sm text-gray-500 mt-2">
                          신뢰도: {Math.round((review.sentiment_confidence || 0) * 100)}%
                        </span>
                        {review.sentiment_reasoning && (
                          <p className="text-xs text-gray-400 mt-2 text-right max-w-xs">
                            {review.sentiment_reasoning}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-16">
                <span className="text-8xl">🎀</span>
                <p className="text-xl text-gray-500 mt-4">분석할 리뷰가 없습니다.</p>
                <p className="text-gray-400">크롤러를 실행해서 최신 리뷰를 수집해보세요!</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'strategy' && (
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-3xl font-bold text-pink-600">🎯 AI 마케팅 전략</h2>
              <p className="text-gray-600 mt-2">리뷰 분석을 바탕으로 생성된 맞춤 전략</p>
            </div>
            
            {strategy ? (
              <div className="bg-white rounded-2xl shadow-lg p-8">
                <div className="prose max-w-none">
                  <pre className="whitespace-pre-wrap font-sans text-gray-800 leading-relaxed text-lg">
                    {strategy}
                  </pre>
                </div>
              </div>
            ) : (
              <div className="text-center py-16">
                <span className="text-8xl">🤖</span>
                <p className="text-xl text-gray-500 mt-4">마케팅 전략을 생성 중입니다...</p>
                <p className="text-gray-400">리뷰 분석이 완료되면 자동으로 전략이 생성됩니다!</p>
              </div>
            )}
          </div>
        )}
      </main>

      {/* 푸터 */}
      <footer className="bg-white border-t-4 border-pink-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">
            <p className="text-gray-600 text-lg">
              🎀 우리끼리 키즈카페 대전문화점 마케팅 대시보드
            </p>
            <p className="text-gray-400 mt-2">
              마지막 업데이트: {new Date().toLocaleDateString('ko-KR')} • Made with 💖
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

// 정적 데이터 로딩
export async function getStaticProps() {
  let reviews = [];
  let strategy = '';

  try {
    const fs = require('fs');
    const path = require('path');
    
    // 여러 날짜 시도
    const dates = [];
    for (let i = 0; i < 3; i++) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      dates.push(date.toISOString().split('T')[0]);
    }

    // 리뷰 파일 찾기
    for (const date of dates) {
      const possiblePaths = [
        path.join(process.cwd(), 'data', 'reviews', `${date}_iframe.json`),
        path.join(process.cwd(), 'data', 'reviews', `${date}.json`)
      ];

      for (const reviewsPath of possiblePaths) {
        if (fs.existsSync(reviewsPath)) {
          const reviewsData = fs.readFileSync(reviewsPath, 'utf8');
          reviews = JSON.parse(reviewsData);
          break;
        }
      }
      if (reviews.length > 0) break;
    }

    // 전략 파일 찾기
    for (const date of dates) {
      const strategyPath = path.join(process.cwd(), 'data', 'strategies', `${date}_marketing_strategy.md`);
      if (fs.existsSync(strategyPath)) {
        strategy = fs.readFileSync(strategyPath, 'utf8');
        break;
      }
    }

  } catch (error) {
    console.error('데이터 로딩 에러:', error);
  }

  return {
    props: {
      reviews,
      strategy
    },
    revalidate: 3600 // 1시간마다 재생성
  };
}