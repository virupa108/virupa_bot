import { useState, useEffect } from 'react'
import 'react-big-calendar/lib/css/react-big-calendar.css'
import { Calendar } from '../components/Calendar'
interface Summary {
  id: number
  summary_text: string
  date_summarized: string
}




export default function Home() {
  const [summaries, setSummaries] = useState<Summary[]>([])
  const [events, setEvents] = useState<CalendarEvent[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

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

  useEffect(() => {
    fetchSummaries()
  }, [])

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <Calendar summaries={summaries} />
  )
}