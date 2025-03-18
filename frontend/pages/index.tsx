import { useState, useEffect } from 'react'
import { Calendar as BigCalendar, dateFnsLocalizer } from 'react-big-calendar'
import { format, parse, startOfWeek, getDay } from 'date-fns'
import 'react-big-calendar/lib/css/react-big-calendar.css'
import styles from '../components/Calendar/Calendar.module.css'

interface Summary {
  id: number
  summary_text: string
  date_summarized: string
}

interface CalendarEvent {
  title: string
  start: Date
  end: Date
  allDay?: boolean
  summary: string
  sections: Record<string, string>
}

const locales = {
  'en-US': require('date-fns/locale/en-US')
}

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
})

const CustomEvent = ({ event }: { event: CalendarEvent }) => {
  return (
    <div className={styles.eventWrapper}>
      <div className={styles.eventContent}>
        OpenAI Summary
      </div>
      <div className={styles.customTooltip}>
        <div className={styles.tooltipContent}>
          {/* Parse and display sections */}
          {Object.entries(event.sections).map(([section, content]) => (
            <div key={section} className={styles.section}>
              <h3 className={styles.sectionTitle}>{section}</h3>
              <div className={styles.sectionContent}>{content}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default function Home() {
  const [summaries, setSummaries] = useState<Summary[]>([])
  const [events, setEvents] = useState<CalendarEvent[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchSummaries = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/summaries')
        const data: Summary[] = await res.json()
        setSummaries(data)

        // Convert summaries to calendar events
        const calendarEvents = data.map(summary => ({
          title: summary.summary_text,
          start: new Date(summary.date_summarized),
          end: new Date(summary.date_summarized),
          allDay: true,
          summary: summary.summary_text,
          sections: {}
        }))
        setEvents(calendarEvents)
      } catch (err: any) {
        setError(err.message)
      } finally {
        setIsLoading(false)
      }
    }

    fetchSummaries()
  }, [])

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div className={styles.calendarContainer}>
      <div className={styles.calendar}>
        <BigCalendar
          localizer={localizer}
          events={events}
          components={{
            event: CustomEvent
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
            style: {
              backgroundColor: '#0969da',
              border: 'none',
              borderRadius: '4px',
              color: 'white'
            }
          })}
        />
      </div>
    </div>
  )
}