import type { NextConfig } from 'next';

const basePath = '/frontend'; // default '' for root
const assetPrefix = basePath ? `${basePath}/` : '';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  basePath,
  assetPrefix,
};

export default nextConfig;
