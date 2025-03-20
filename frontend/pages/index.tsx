import { useState, useEffect } from 'react'
import 'react-big-calendar/lib/css/react-big-calendar.css'
import { Calendar } from '../components/Calendar'
import { API_ROUTES } from '@/config/api'


export default function Home() {

  return (
    <Calendar />
  )
}