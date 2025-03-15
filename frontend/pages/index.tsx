import { useState, useEffect } from 'react'
import { format } from 'date-fns'

interface Summary {
  id: number
  summary_text: string
  date_summarized: string
}

export default function Home() {
  const [summaries, setSummaries] = useState<Summary[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchSummaries = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/summaries')
        const data = await res.json()
        setSummaries(data)
      } catch (error) {
        console.error('Error fetching summaries:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchSummaries()
  }, [])

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Daily Summaries</h1>

      {loading ? (
        <div>Loading...</div>
      ) : (
        <div className="space-y-6">
          {summaries.map((summary) => (
            <div key={summary.id} className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-2">
                {format(new Date(summary.date_summarized), 'MMMM d, yyyy')}
              </h2>
              <p className="whitespace-pre-wrap">{summary.summary_text}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}