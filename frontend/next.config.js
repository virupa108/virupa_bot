/** @type {import('next').NextConfig} */
const nextConfig = {
	reactStrictMode: true,
	// Enable Turbopack
	experimental: {
		turbo: {
			// Turbopack specific options
			resolveAlias: {
				// Custom module aliases if needed
			}
		}
	},
	// Keep webpack watcher for Docker
	webpack: (config) => {
		config.watchOptions = {
			poll: 1000,
			aggregateTimeout: 300,
		}
		return config
	},
}

module.exports = nextConfig