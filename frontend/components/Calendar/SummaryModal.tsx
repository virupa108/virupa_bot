import styles from './SummaryModal.module.css'
import { format } from 'date-fns'

interface SummaryModalProps {
  show: boolean
  onClose: () => void
  summary?: {
    description: string
    date: Date
  } | null
}

export const SummaryModal = ({ show, onClose, summary }: SummaryModalProps) => {
  if (!show) return null;

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
        <div className={styles.modalHeader}>
          <h3>Daily Summary - {summary?.date ? format(summary.date, 'MMMM d, yyyy') : ''}</h3>
          <button onClick={onClose} className={styles.closeButton}>×</button>
        </div>
        <div className={styles.modalBody}>
          {summary?.description ? (
            <p className={styles.summaryText}>{summary.description}</p>
          ) : (
            <p>No summary available</p>
          )}
        </div>
      </div>
    </div>
  );
};