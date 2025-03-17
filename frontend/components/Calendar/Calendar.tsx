import { useState } from 'react'
import { Calendar as BigCalendar, dateFnsLocalizer } from 'react-big-calendar'
import { format, parse, startOfWeek, getDay } from 'date-fns'
import "react-big-calendar/lib/css/react-big-calendar.css"

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales: { 'en-US': require('date-fns/locale/en-US') },
})

interface Summary {
  id: number
  summary_text: string
  date_summarized: string
}

interface CalendarProps {
  summaries: Summary[]
}

export const Calendar = ({ summaries }: CalendarProps) => {
  const [selectedEvent, setSelectedEvent] = useState<Summary | null>(null)

  const events = summaries.map(summary => ({
    title: 'Summary',
    start: new Date(summary.date_summarized),
    end: new Date(summary.date_summarized),
    resource: summary
  }))

  return (
    <div className="flex flex-col gap-4">
      <div className="h-[400px]">
        <BigCalendar
          localizer={localizer}
          events={events}
          views={['month']}
          defaultView='month'
          onSelectEvent={(event) => setSelectedEvent(event.resource)}
          style={{ height: '100%' }}
        />
      </div>
      {selectedEvent && (
        <div className="p-4 bg-white shadow rounded">
          <p>{selectedEvent.summary_text}</p>
        </div>
      )}
    </div>
  )
}