const COINGECKO_API = 'https://api.coingecko.com/api/v3';

export async function getTokenPrice(symbol: string): Promise<number> {
  try {
    const tokenIds: { [key: string]: string } = {
      'ARB': 'arbitrum',
      'SUI': 'sui',
      'OP': 'optimism',
      // Add more tokens as needed
    };

    const id = tokenIds[symbol.toUpperCase()];
    if (!id) return 0;

    const response = await fetch(
      `${COINGECKO_API}/simple/price?ids=${id}&vs_currencies=usd`
    );
    const data = await response.json();
    return data[id]?.usd || 0;
  } catch (error) {
    console.error('Error fetching token price:', error);
    return 0;
  }
}