const analyzeWithLLM = async (
  question: string,
  userResponse: string,
  customPrompt: string
) => {
  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question, userResponse, customPrompt })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const result = await response.json()
    console.log(result.content)
    return result.content
  } catch (error) {
    console.error('Error:', error)
    return 'Error analyzing response'
  }
}

export { analyzeWithLLM }
