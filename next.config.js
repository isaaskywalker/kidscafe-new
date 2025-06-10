/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // 정적 파일 경로 설정
  trailingSlash: false,
  
  // 이미지 최적화 설정
  images: {
    unoptimized: true
  },

  // 환경 변수
  env: {
    CUSTOM_KEY: 'kidscafe-dashboard',
  },
}

module.exports = nextConfig