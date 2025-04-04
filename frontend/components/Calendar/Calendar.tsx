import { useState, useEffect } from 'react'
import { Calendar as BigCalendar, dateFnsLocalizer } from 'react-big-calendar'
import { EventModal } from "./EventModal"
import { SummaryModal } from './SummaryModal'
import { EventActionModal } from './EventActionModal'

import { format, formatInTimeZone } from 'date-fns-tz'
import { parse, startOfWeek, getDay } from 'date-fns'
import "react-big-calendar/lib/css/react-big-calendar.css"
import styles from './Calendar.module.css'
import calendarStyles from './BigCalendar.module.css'
import { API_ROUTES, SUMMARY_OPENAI_TITLE } from '@/config/api'
import { getTokenPrice } from '@/services/tokenPrices'


const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales: { 'en-US': require('date-fns/locale/en-US') },
})

export interface CalendarEvent {
  id?: number
  title: string
  start: Date
  end: Date
  description: string
  event_type?: string
}

interface Summary {
  id: number
  summary_text: string
  date_summarized: string
}

interface Event { // this is the event from the backend
  id: number
  title: string
  description: string
  start: string
  end: string
  event_type?: string  // Add this
}


      // Convert summaries to calendar events
const convertSummariesToCalendarEvents = (summaries: Summary[]): CalendarEvent[] => {
    return summaries.map(summary => ({
      // I wont eddit summaries, so i dont need id
        title: SUMMARY_OPENAI_TITLE,
        start: new Date(summary.date_summarized),
        end: new Date(summary.date_summarized),
        description: summary.summary_text
    }))
}

function convertUTCDateToLocalDate(date: Date): Date {
    const newDate = new Date(date.getTime() + date.getTimezoneOffset() * 60 * 1000);
    const offset = date.getTimezoneOffset() / 60;
    const hours = date.getHours();
    newDate.setHours(hours - offset);
    return newDate;
}

const convertEventsToCalendarEvents = async (events: Event[]): Promise<CalendarEvent[]> => {
  const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;

  const processedEvents = await Promise.all(events.map(async event => {
    let title = event.title;
    let description = event.description;

    // Check if this is a token unlock event
    if (event.event_type === 'vesting') {
      // Extract token amount and symbol using regex
      // Updated regex to handle "Team and Advisor Tokens: 450,000,000 ARB" format
      const match = event.description.match(/:\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*([A-Z]+)/);
      if (match) {
        const amount = parseFloat(match[1].replace(/,/g, ''));
        const symbol = match[2];

        try {
          // Fetch token price
          const price = await getTokenPrice(symbol);
          if (price > 0) {
            const value = price * amount;
            // Add value to description
            description = `${event.description}\nEstimated Value: $${value.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            })}`;
          }
        } catch (error) {
          console.error(`Error fetching price for ${symbol}:`, error);
        }
      }
    }

    return {
      id: event.id,
      title: `${title} (${formatInTimeZone(convertUTCDateToLocalDate(new Date(event.start)), tz, 'HH:mm')})`,
      start: new Date(event.start),
      end: new Date(event.end),
      description,
      event_type: event.event_type
    };
  }));

  return processedEvents;
};

export const Calendar = () => {
  const [calendarEvents, setCalendarEvents] = useState<CalendarEvent[]>([])
  const [showEventModal, setShowEventModal] = useState(false)
  const [selectedEvent, setSelectedEvent] = useState<CalendarEvent | null>(null)
  const [showSummaryModal, setShowSummaryModal] = useState(false)
  const [selectedSummary, setSelectedSummary] = useState<{description: string, date: Date} | null>(null)
  const [showEventActionModal, setShowEventActionModal] = useState(false)


  const fetchEventsAndSummaries = async () => {
    try {
      const [summariesResponse, eventsResponse] = await Promise.all([
        fetch(API_ROUTES.SUMMARIES_GET),
        fetch(API_ROUTES.EVENTS_GET)
      ]);

      if (!summariesResponse.ok) throw new Error('Failed to fetch summaries');
      if (!eventsResponse.ok) throw new Error('Failed to fetch events');

      const [summariesData, eventsData] = await Promise.all([
        summariesResponse.json(),
        eventsResponse.json()
      ]);

      const summaryEvents = convertSummariesToCalendarEvents(summariesData);
      const calendarEvents = await convertEventsToCalendarEvents(eventsData);
      setCalendarEvents([...summaryEvents, ...calendarEvents]);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  const handleCalendarEventSubmit = async (event: CalendarEvent) => {
    try {
      if (!event.title || !event.start || !event.end) {
        throw new Error('fields are required');
      }
      const response = await fetch(API_ROUTES.EVENTS_POST, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(event)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to create event')
      }

      setShowEventModal(false)
      // Refresh calendarEvent after creating new event
      // yes i fetch redundantly summaries, but it's a small app and i don't want to complicate the code
      await fetchEventsAndSummaries()

    } catch (error) {
      console.error('Error creating event:', error)
    }
  }

  const handleSelectEvent = (event: CalendarEvent) => {
    if (event.title === SUMMARY_OPENAI_TITLE) {
      setSelectedSummary({
        description: event.description,
        date: event.start
      });
      setShowSummaryModal(true);
    } else {
      setSelectedEvent(event);
      setShowEventActionModal(true);
    }
  }

  const handleEditEvent = async (updatedEvent: CalendarEvent) => {
    try {
      const response = await fetch(`${API_ROUTES.EVENTS_PUT}${updatedEvent.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedEvent),
      });

      if (!response.ok) throw new Error('Failed to update event');
      await fetchEventsAndSummaries() // refresh calendar
    } catch (error) {
      console.error('Error updating event:', error);
    }
  };

  const handleDeleteEvent = async (eventId: number) => {
    try {
      const response = await fetch(`${API_ROUTES.EVENTS_DELETE}${eventId}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Failed to delete event');
      await fetchEventsAndSummaries() // refresh calendar
    } catch (error) {
      console.error('Error deleting event:', error);
    }
  };

  useEffect(() => {
    fetchEventsAndSummaries()
  }, [])

  const dayPropGetter = (date: Date) => {
    const isToday = new Date().toDateString() === date.toDateString()
    return {
      className: isToday ? styles.currentDay : '',
      className: isToday ? styles.todayCell : styles.dayCell
    }
  }

  return (
    <div className={styles.calendarContainer}>
      <div className={styles.buttonContainer}>
        <button
          onClick={() => setShowEventModal(true)}
          className={styles.addButton}
        >
          + Add Event
        </button>
      </div>

      <div className={calendarStyles.calendar}>
        <BigCalendar
          localizer={localizer}
          events={calendarEvents}
          startAccessor="start"
          endAccessor="end"
          style={{
            height: 'calc(100vh - 200px)',
            minHeight: '600px'
          }}
          views={['month', 'week', 'day']}
          defaultView='month'
          onSelectEvent={handleSelectEvent}
          dayPropGetter={dayPropGetter}
          eventPropGetter={(event) => ({
            className: event.event_type === 'vesting' ? styles.vestingEvent : styles.summaryEvent
          })}
        />
      </div>

      <EventModal
        show={showEventModal}
        onClose={() => {
          setShowEventModal(false)
          setSelectedEvent(null)
        }}
        event={selectedEvent}
        readOnly={selectedEvent?.title === SUMMARY_OPENAI_TITLE}
        onSubmit={handleCalendarEventSubmit}
      />

      <SummaryModal
        show={showSummaryModal}
        onClose={() => {
          setShowSummaryModal(false)
          setSelectedSummary(null)
        }}
        summary={selectedSummary}
      />

      {selectedEvent && (
        <EventActionModal
          show={showEventActionModal}
          onClose={() => {
            setShowEventActionModal(false)
            setSelectedEvent(null)
          }}
          event={selectedEvent}
          onEdit={handleEditEvent}
          onDelete={handleDeleteEvent}
        />
      )}
    </div>
  )
}

export const CalendarComponent = () => {
  return <Calendar />
}