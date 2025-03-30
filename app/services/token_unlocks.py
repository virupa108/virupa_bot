import aiohttp
import logging
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

logger = logging.getLogger(__name__)


class TokenUnlocksService:
    def __init__(self):
        self.base_url = "https://production-api.mobula.io/api/1"
        self.api_key = os.getenv("MOBULA_API_KEY")

    async def get_token_unlocks(self) -> List[Dict[str, Any]]:
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            formatted_events = []

            # List of tokens to check
            tokens = [
                "Sui",
                "Aptos",
                "Sei",
                "Pyth",
                "Axelar",
                "Arbitrum",
                "Optimism",
                "Solana",
                "Celestia",
                "Eigenlayer",
                "Chainlink",
                "Curve",
                "Aave",
                "Cheelee",
                "Avalanche",
                "Zksync",
            ]

            async with aiohttp.ClientSession() as session:
                for token_name in tokens:
                    try:
                        url = f"{self.base_url}/metadata?asset={token_name}"
                        async with session.get(url, headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                release_schedule = data.get("data", {}).get(
                                    "release_schedule", []
                                )

                                for unlock in release_schedule:
                                    unlock_date = datetime.fromtimestamp(
                                        unlock["unlock_date"] / 1000
                                    )
                                    if unlock_date > datetime.now():
                                        # Format allocation details
                                        allocation_str = ", ".join(
                                            [
                                                f"{k}: {v:,.0f}"
                                                for k, v in unlock.get(
                                                    "allocation_details", {}
                                                ).items()
                                            ]
                                        )

                                        formatted_events.append(
                                            {
                                                "title": f"CRYPTO: {token_name} Unlock",
                                                "description": f"{allocation_str if allocation_str else 'Amount'}: {unlock['tokens_to_unlock']:,.0f} {token_name}",
                                                "start": unlock_date.isoformat(),
                                                "end": (
                                                    unlock_date + timedelta(hours=1)
                                                ).isoformat(),
                                                "event_type": "vesting",
                                            }
                                        )
                            else:
                                logger.error(
                                    f"Failed to fetch {token_name} data: {response.status}"
                                )

                    except Exception as e:
                        logger.error(f"Error processing {token_name}: {str(e)}")
                        continue

                return formatted_events

        except Exception as e:
            logger.error(f"Error getting token unlocks: {str(e)}")
            return []


arbitrum = [
    {
        "Arbitrum": [
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2025-04-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2025-05-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2025-06-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2025-07-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2025-08-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2025-09-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2025-10-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2025-11-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2025-12-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2026-01-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2026-02-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2026-03-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2026-04-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2026-05-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2026-06-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2026-07-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2026-08-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2026-09-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2026-10-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2026-11-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2026-12-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2027-01-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2027-02-16 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 36520833.33333334,
                    "Team & Advisors": 57127766.66666667,
                },
                "tokens_to_unlock": 93648600,
                "unlock_date": "2027-03-16 00:00:00",
            },
        ]
    }
]

optimism = [
    {
        "Optimism": [
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2025-03-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2025-04-30 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2025-05-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2025-06-30 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2025-07-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2025-08-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2025-09-30 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2025-10-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2025-11-30 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2025-12-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2026-01-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2026-02-28 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2026-03-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2026-04-30 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2026-05-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2026-06-30 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2026-07-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2026-08-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2026-09-30 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2026-10-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2026-11-30 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2026-12-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2027-01-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2027-02-28 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2027-03-31 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2027-04-30 00:00:00",
            },
            {
                "allocation_details": {
                    "Investors": 11408506.88,
                    "Core Contributors": 12750684.16,
                },
                "tokens_to_unlock": 24159191.04,
                "unlock_date": "2027-05-31 00:00:00",
            },
        ]
    }
]
