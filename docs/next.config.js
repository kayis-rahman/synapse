const nextConfig = {
  output: 'export',
  basePath: '/synapse',
  trailingSlash: true,
  transpilePackages: ['fumadocs-ui'],
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig;
