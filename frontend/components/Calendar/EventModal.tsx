import { useState, useRef, useEffect } from 'react'
import { format } from 'date-fns'
import styles from './EventModal.module.css'

import { CalendarEvent } from './Calendar'


interface EventModalProps {
  show: boolean
  onClose: () => void
  onSubmit: (event: CalendarEvent) => void
  initialEvent?: CalendarEvent
}

export const EventModal = ({ show, onClose, onSubmit, initialEvent }: EventModalProps) => {
  const modalRef = useRef<HTMLDivElement>(null)
  const [calendarEvent, setCalendarEvent] = useState<CalendarEvent>(initialEvent || {
    title: '',
    description: '',
    start: new Date(),
    end: new Date()
  })

  // Handle click outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (modalRef.current && !modalRef.current.contains(event.target as Node)) {
        onClose()
      }
    }

    if (show) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [show, onClose])

  if (!show) return null

  return (
    <div className={styles.modalOverlay}>
      <div ref={modalRef} className={styles.modalContainer}>
        <div className={styles.modalContent}>
          <h2 className={styles.modalTitle}>Add New Event</h2>

          <div className={styles.modalBody}>
            <form onSubmit={(e) => { e.preventDefault(); onSubmit(calendarEvent ) }}>
              <div className={styles.formGroup}>
                <label>Title</label>
                <input
                  type="text"
                  value={calendarEvent.title}
                  onChange={(e) => setCalendarEvent({...calendarEvent, title: e.target.value})}
                  className={styles.input}
                />
              </div>

              <div className={styles.formGroup}>
                <label>Description</label>
                <textarea
                  value={calendarEvent.description}
                  onChange={(e) => setCalendarEvent({...calendarEvent, description: e.target.value})}
                  className={styles.textarea}
                />
              </div>

              <div className={styles.formGroup}>
                <label>Start Date</label>
                <input
                  type="datetime-local"
                  value={format(calendarEvent.start, "yyyy-MM-dd'T'HH:mm")}
                  onChange={(e) => setCalendarEvent({...calendarEvent, start: new Date(e.target.value)})}
                  className={styles.input}
                />
              </div>

              <div className={styles.formGroup}>
                <label>End Date</label>
                <input
                  type="datetime-local"
                  value={format(calendarEvent.end, "yyyy-MM-dd'T'HH:mm")}
                  onChange={(e) => setCalendarEvent({...calendarEvent, end: new Date(e.target.value)})}
                  className={styles.input}
                />
              </div>

              <div className={styles.modalFooter}>
                <button type="button" onClick={onClose} className={styles.cancelButton}>
                  Cancel
                </button>
                <button type="submit" className={styles.submitButton}>
                  Save Event
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}