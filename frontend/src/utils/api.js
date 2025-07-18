
import {useAuth} from "@clerk/clerk-react"

export const useApi = () => {
    const {getToken} = useAuth()

    const makeRequest = async (endpoint, options = {}) => {
        const token = await getToken()
        const defaultOptions = {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        }

        const response = await fetch(`http://localhost:8000/api/${endpoint}`, {
            ...defaultOptions,
            ...options,
        })

        if (!response.ok) {
            // Log the full error response
            const errorText = await response.text()
            console.log('Error status:', response.status) // Debug line
            console.log('Error response text:', errorText) // Debug line
            
            let errorData = null
            try {
                errorData = JSON.parse(errorText)
            } catch (e) {
                console.log('Could not parse error as JSON')
            }
            
            if (response.status === 429) {
                throw new Error("Daily quota exceeded")
            }
            throw new Error(errorData?.detail || errorText || "An error occurred")
        }

        return response.json()
    }

    return {makeRequest}
}
