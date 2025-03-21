import React, { useState } from 'react';
import { format } from 'date-fns';
import styles from './EventActionModal.module.css';

interface EventActionModalProps {
  show: boolean;
  onClose: () => void;
  event: CalendarEvent;
  onEdit: (event: CalendarEvent) => void;
  onDelete: (eventId: number) => void;
}

export const EventActionModal = ({ show, onClose, event, onEdit, onDelete }: EventActionModalProps) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(event?.title || '');
  const [description, setDescription] = useState(event?.description || '');
  const [start, setStart] = useState<Date>(event?.start || new Date());
  const [end, setEnd] = useState<Date>(event?.end || new Date());
  const eventId = event?.id;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onEdit({
      ...event,
      title,
      description,
      start,
      end
    });
    onClose();
  };

  const handleDelete = () => {
    console.log("event");
    console.log(event);
    console.log(eventId);
    console.log("event");

    if (window.confirm('Are you sure you want to delete this event?')) {
      onDelete(event.id!);
      onClose();
    }
  };

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
        {!isEditing ? (
          <>
            <div className={styles.modalHeader}>
              <h3>{event.title}</h3>
              <button onClick={onClose} className={styles.closeButton}>×</button>
            </div>
            <div className={styles.modalBody}>
              <p>{event.description}</p>
              <p>Start: {format(event.start, 'PPpp')}</p>
              <p>End: {format(event.end, 'PPpp')}</p>
            </div>
            <div className={styles.modalFooter}>
              <button
                onClick={() => setIsEditing(true)}
                className={styles.editButton}
              >
                Edit
              </button>
              <button
                onClick={handleDelete}
                className={styles.deleteButton}
              >
                Delete
              </button>
            </div>
          </>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className={styles.modalHeader}>
              <h3>Edit Event</h3>
              <button type="button" onClick={onClose} className={styles.closeButton}>×</button>
            </div>
            <div className={styles.modalBody}>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Event title"
                className={styles.input}
              />
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Event description"
                className={styles.textarea}
              />
              <input
                type="datetime-local"
                value={format(start, "yyyy-MM-dd'T'HH:mm")}
                onChange={(e) => setStart(new Date(e.target.value))}
                className={styles.input}
              />
              <input
                type="datetime-local"
                value={format(end, "yyyy-MM-dd'T'HH:mm")}
                onChange={(e) => setEnd(new Date(e.target.value))}
                className={styles.input}
              />
            </div>
            <div className={styles.modalFooter}>
              <button type="submit" className={styles.saveButton}>Save</button>
              <button
                type="button"
                onClick={() => setIsEditing(false)}
                className={styles.cancelButton}
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};