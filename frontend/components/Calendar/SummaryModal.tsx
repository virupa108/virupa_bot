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

  const formatText = (text: string) => {
    // Format usernames
    const formattedText = text.replace(
      /@(\w+)/g,
      '<span class="' + styles.username + '">@$1</span>'
    );

    // Format section titles with the same style as "For Crypto Traders:"
    return formattedText.replace(
      /^(Crypto Traders|For Crypto Traders:|Airdrops:|Stocks:)$/gm,
      '<div class="' + styles.mainSectionTitle + '">$1</div>'
    ).replace(
      /^- (Insights|Events|News|Updates|Projects|New projects|New Airdrops|Deadlines|Tasks|New airdrops|Earnings|Speculation|Mentioned stocks):/gm,
      '<div class="' + styles.subTitle + '">$1:</div>'
    );
  };

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
        <div className={styles.modalHeader}>
          <h3>Daily Summary - {summary?.date ? format(summary.date, 'MMMM d, yyyy') : ''}</h3>
          <button onClick={onClose} className={styles.closeButton}>×</button>
        </div>
        <div className={styles.modalBody}>
          {summary?.description ? (
            <div
              className={styles.summaryText}
              dangerouslySetInnerHTML={{
                __html: formatText(summary.description)
              }}
            />
          ) : (
            <p>No summary available</p>
          )}
        </div>
      </div>
    </div>
  );
};