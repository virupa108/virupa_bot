import type { AppProps } from 'next/app'
// Alternative approach - no CSS imports here
// We'll handle styles in the Calendar component

function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}

export default MyApp