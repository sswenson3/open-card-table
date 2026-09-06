import { useEffect, useState } from 'react'
import './App.css'

type HealthResponse = {
    name: string
    status: string
    version: string
}

function App() {
    const [health, setHealth] = useState<HealthResponse | null>(null)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function checkHealth() {
            try {
                const response = await fetch('/api/health')

                if (!response.ok) {
                    throw new Error(`Server returned ${response.status}`)
                }

                const data: HealthResponse = await response.json()
                setHealth(data)
                setError(null)
            } catch {
                setHealth(null)
                setError('Disconnected')
            }
        }

        checkHealth()
    }, [])

    return (
        <main>
            <h1>Open Card Table</h1>

            {health ? (
                <>
                    <p>Server: Connected</p>
                    <p>Application: {health.name}</p>
                    <p>Version: {health.version}</p>
                </>
            ) : (
                <p>Server: {error ?? 'Connecting...'}</p>
            )}
        </main>
    )
}

export default App