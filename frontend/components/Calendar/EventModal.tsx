import { useState, useRef, useEffect } from 'react'
import { format } from 'date-fns'
import styles from './EventModal.module.css'


interface Event {
  title: string
  description: string
  start_date: Date
  end_date: Date
}

interface EventModalProps {
  show: boolean
  onClose: () => void
  onSubmit: (event: Event) => void
  initialEvent?: Event
}

export const EventModal = ({ show, onClose, onSubmit, initialEvent }: EventModalProps) => {
  const modalRef = useRef<HTMLDivElement>(null)
  const [event, setEvent] = useState<Event>(initialEvent || {
    title: '',
    description: '',
    start_date: new Date(),
    end_date: new Date()
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
            <form onSubmit={(e) => { e.preventDefault(); onSubmit(event) }}>
              <div className={styles.formGroup}>
                <label>Title</label>
                <input
                  type="text"
                  value={event.title}
                  onChange={(e) => setEvent({...event, title: e.target.value})}
                  className={styles.input}
                />
              </div>

              <div className={styles.formGroup}>
                <label>Description</label>
                <textarea
                  value={event.description}
                  onChange={(e) => setEvent({...event, description: e.target.value})}
                  className={styles.textarea}
                />
              </div>

              <div className={styles.formGroup}>
                <label>Start Date</label>
                <input
                  type="datetime-local"
                  value={format(event.start_date, "yyyy-MM-dd'T'HH:mm")}
                  onChange={(e) => setEvent({...event, start_date: new Date(e.target.value)})}
                  className={styles.input}
                />
              </div>

              <div className={styles.formGroup}>
                <label>End Date</label>
                <input
                  type="datetime-local"
                  value={format(event.end_date, "yyyy-MM-dd'T'HH:mm")}
                  onChange={(e) => setEvent({...event, end_date: new Date(e.target.value)})}
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