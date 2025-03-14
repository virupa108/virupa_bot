# Project TODO List

## Immediate Tasks
- [ ] Generate OpenAI summaries for historical tweets
  - [ ] Add progress tracking for long-running summary generation
  - [ ] Handle rate limits and costs for bulk processing
  - [ ] summaries should run only once the day end so they cover all tweets from the day

## Database Models
- [ ] Create Event model for structured event data (dates, deadlines, etc.)
- [ ] Create Sentiment model to track market sentiment over time
- [ ] Create UserPreference model for watchlists and settings
- [ ] Add indexes for better query performance

## Data Processing
- [ ] Extract structured data from OpenAI summaries
  - [ ] Parse events and dates
  - [ ] Extract sentiment data
  - [ ] Identify mentioned assets/projects
- [ ] Implement data validation
- [ ] Add error handling for data extraction

## Telegram Integration
- [ ] Create Telegram bot commands
  - [ ] Daily/Weekly summaries
  - [ ] Query specific information
  - [ ] Set up alerts
- [ ] Implement notification system
- [ ] Add user preferences for notifications

## Web Interface
### Backend
- [ ] Set up FastAPI
- [ ] Design RESTful API endpoints
- [ ] Implement authentication
- [ ] Add caching layer

### Frontend
- [ ] Create main dashboard
  - [ ] Summary cards
  - [ ] Calendar view
  - [ ] Sentiment trends
  - [ ] Active airdrops tracker
- [ ] Add interactive features
  - [ ] Filterable timeline
  - [ ] Search functionality
  - [ ] Custom date ranges
- [ ] Implement data visualizations
  - [ ] Sentiment charts
  - [ ] Event timeline
  - [ ] Word clouds
  - [ ] Mention frequency graphs

## Features & Automation
- [ ] Calendar integration (Google Calendar/iCal)
- [ ] Automated event reminders
- [ ] Task management for airdrops
- [ ] Portfolio tracking
- [ ] Price correlation analysis
- [ ] Historical trend analysis

## Infrastructure
- [ ] Set up monitoring
- [ ] Implement logging
- [ ] Add backup system
- [ ] Configure CI/CD
- [ ] Add test coverage

## Documentation
- [ ] API documentation
- [ ] Setup instructions
- [ ] User guide
- [ ] Contributing guidelines

## Future Ideas
- Integration with other data sources
- Mobile app development
- Trading signals based on sentiment
- Risk management system
- Export functionality
- Premium features

## Current Focus
1. Extract structured data from summaries
2. Set up basic Telegram integration
3. Create minimal web interface
4. Implement event tracking system

## Notes
- Remember to maintain backwards compatibility
- Focus on modular design for easy expansion
- Consider rate limits for APIs
- Plan for scalability