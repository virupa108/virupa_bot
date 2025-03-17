import { useState, useEffect } from 'react'
import { Calendar } from '../components/Calendar'
import { addDays, subDays } from 'date-fns'

interface Summary {
  id: number
  summary_text: string
  date_summarized: string
}


const mockSummaries: Summary[] = [
    {
      id: 1,
      summary_text: "Started working on the new project",
      date_summarized: new Date().toISOString()
    },
    {
      id: 2,
      summary_text: "Team meeting about frontend development",
      date_summarized: addDays(new Date(), 2).toISOString()
    },
    {
      id: 3,
      summary_text: "Completed the calendar component",
      date_summarized: subDays(new Date(), 1).toISOString()
    }
  ]

export default function Home() {
  const [summaries, setSummaries] = useState<Summary[]>(mockSummaries)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // useEffect(() => {
  //   const fetchSummaries = async () => {
  //     try {
  //       const res = await fetch('http://localhost:8000/api/summaries')
  //       const data = await res.json()
  //       setSummaries(data)
  //     } catch (err: any) {
  //       setError(err.message)
  //     } finally {
  //       setIsLoading(false)
  //     }
  //   }

  //   fetchSummaries()
  // }, [])

  // if (error) {
  //   return <div className="text-red-500" role="alert">Error loading summaries: {error}</div>
  // }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Daily Summaries</h1>
      <Calendar summaries={mockSummaries} />
    </div>
  )
}