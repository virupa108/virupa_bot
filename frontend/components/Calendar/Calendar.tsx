import { useState, useEffect } from 'react'
import { Calendar as BigCalendar, dateFnsLocalizer } from 'react-big-calendar'
import { EventModal } from "./EventModal"
import { SummaryModal } from './SummaryModal'
import { EventActionModal } from './EventActionModal'

import { format, parse, startOfWeek, getDay } from 'date-fns'
import "react-big-calendar/lib/css/react-big-calendar.css"
import styles from './Calendar.module.css'
import calendarStyles from './BigCalendar.module.css'
import { API_ROUTES, SUMMARY_OPENAI_TITLE } from '@/config/api'


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
const convertEventsToCalendarEvents = (events: Event[]): CalendarEvent[] => {
  return events.map(event => ({
    id: event.id,
    title: event.title,
    start: new Date(event.start),
    end: new Date(event.end),
    description: event.description
  }))
}

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
      const calendarEvents = convertEventsToCalendarEvents(eventsData);
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
          // components={{
          //   event: OpenAISummaryEvent
          // }}
          startAccessor="start"
          endAccessor="end"
          style={{
            height: 'calc(100vh - 200px)',
            minHeight: '600px'
          }}
          views={['month', 'week', 'day']}
          defaultView='month'
          onSelectEvent={handleSelectEvent}
          formats={{
            eventTimeRangeFormat: () => '',
            dayRangeHeaderFormat: ({ start, end }) =>
              `${format(start, 'MMM d')} - ${format(end, 'MMM d, yyyy')}`
          }}
          eventPropGetter={(event) => ({
            className: styles.summaryEvent
          })}
          className={calendarStyles.calendar}
          toolbarClassName={calendarStyles.toolbar}
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
            setShowEventActionModal(false);
            setSelectedEvent(null);
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