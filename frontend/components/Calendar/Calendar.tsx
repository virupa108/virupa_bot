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
    title: 'Summary',
    start: new Date(summary.date_summarized),
    end: new Date(summary.date_summarized),
    resource: summary
  }))

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: API call to create event
    setShowEventModal(false)
  }

  return (
    <div className="flex flex-col gap-4 p-4">
      <div className="flex justify-end mb-4">
        <button
          onClick={() => setShowEventModal(true)}
          className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 shadow-md"
        >
          + Add Event
        </button>
      </div>

      <div className="h-[600px]">
        <BigCalendar
          localizer={localizer}
          events={events}
          views={['month']}
          defaultView='month'
          onSelectEvent={(event) => setSelectedEvent(event.resource)}
          style={{ height: '100%' }}
        />
      </div>

      {/* Event Modal */}
      {showEventModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 className="text-xl font-bold mb-4">Add New Event</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block mb-1">Title</label>
                <input
                  type="text"
                  value={newEvent.title}
                  onChange={(e) => setNewEvent({...newEvent, title: e.target.value})}
                  className="w-full border rounded p-2"
                  required
                />
              </div>

              <div>
                <label className="block mb-1">Description</label>
                <textarea
                  value={newEvent.description}
                  onChange={(e) => setNewEvent({...newEvent, description: e.target.value})}
                  className="w-full border rounded p-2"
                  rows={3}
                />
              </div>

              <div>
                <label className="block mb-1">Start Date</label>
                <input
                  type="datetime-local"
                  value={format(newEvent.start_date, "yyyy-MM-dd'T'HH:mm")}
                  onChange={(e) => setNewEvent({...newEvent, start_date: new Date(e.target.value)})}
                  className="w-full border rounded p-2"
                  required
                />
              </div>

              <div>
                <label className="block mb-1">End Date</label>
                <input
                  type="datetime-local"
                  value={format(newEvent.end_date, "yyyy-MM-dd'T'HH:mm")}
                  onChange={(e) => setNewEvent({...newEvent, end_date: new Date(e.target.value)})}
                  className="w-full border rounded p-2"
                  required
                />
              </div>

              <div className="flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowEventModal(false)}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                  Save Event
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {selectedEvent && (
        <div className="p-4 bg-white shadow rounded">
          <p>{selectedEvent.summary_text}</p>
        </div>
      )}
    </div>
  )
}