const env = {
  development: {
    API_URL: 'http://localhost:8000/api',
  },
  production: {
    API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://your-production-api.com/api',
  },
  test: {
    API_URL: 'http://localhost:8000/api',
  }
}

const getEnvironment = () => {
  return process.env.NODE_ENV || 'development'
}

export const config = env[getEnvironment()]