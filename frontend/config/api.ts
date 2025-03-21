import { config } from './env'

export const API_ROUTES = {
  SUMMARIES_GET: `${config.API_URL}/summaries`,
  EVENTS_POST: `${config.API_URL}/events`,
  EVENTS_GET: `${config.API_URL}/events`,
  EVENTS_PUT: `${config.API_URL}/events/`,
  EVENTS_DELETE: `${config.API_URL}/events/`,
  // Add more endpoints here
} as const

export const SUMMARY_OPENAI_TITLE = "OpenAI Summary"
