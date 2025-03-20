import { useState } from 'react'
import { Calendar as BigCalendar, dateFnsLocalizer } from 'react-big-calendar'
import { EventModal } from "./EventModal"

import { format, parse, startOfWeek, getDay } from 'date-fns'
import "react-big-calendar/lib/css/react-big-calendar.css"
import styles from './Calendar.module.css'
import calendarStyles from './BigCalendar.module.css'


const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales: { 'en-US': require('date-fns/locale/en-US') },
})


interface CalendarEvent {
  title: string
  start: Date
  end: Date
  allDay?: boolean
  summary: string
  sections: Record<string, string>
}

interface Summary {
  id: number
  summary_text: string
  date_summarized: string
}

interface Event {
  id?: number
  title: string
  description: string
  start_date: Date
  end_date: Date
}

interface CalendarProps {
  summaries: Summary[]
}

const OpenAISummaryEvent = ({ event }: { event: CalendarEvent }) => {
  return (
    <div className={styles.eventWrapper}>
      <div className={styles.eventContent}>
        OpenAI Summary
      </div>
    </div>
  );
};

export const Calendar = ({ summaries }: CalendarProps) => {
  const [selectedEvent, setSelectedEvent] = useState<Summary | null>(null)
  const [showEventModal, setShowEventModal] = useState(false)
  const [newEvent, setNewEvent] = useState<Event>({
    title: '',
    description: '',
    start_date: new Date(),
    end_date: new Date()
  })

  const events = summaries.map(summary => ({
    title: summary.summary_text,
    start: new Date(summary.date_summarized),
    end: new Date(summary.date_summarized),
    resource: summary.summary_text
  }))

  const handleEventSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: API call to create event
    console.log("xx");
    setShowEventModal(false)
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
          events={events}
          components={{
            event: OpenAISummaryEvent
          }}
          startAccessor="start"
          endAccessor="end"
          style={{
            height: 'calc(100vh - 200px)',
            minHeight: '600px'
          }}
          views={['month', 'week', 'day']}
          defaultView='month'
          onSelectEvent={(event) => {
            console.log('Selected event:', event);
          }}
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
        onClose={() => setShowEventModal(false)}
        onSubmit={handleEventSubmit}
      />
    </div>
  )
}

export const CalendarComponent = () => {
  return <Calendar summaries={[]}  />
}