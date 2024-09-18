import { NextResponse } from 'next/server'

const REGOLO_TOKEN = process.env.REGOLO_TOKEN

export async function POST(request: Request) {
  const { question, userResponse, customPrompt } = await request.json()

  const prompt = `Analizza la seguente risposta alla domanda '${question}': '${userResponse}'. ${customPrompt}`

  const headers = {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    Authorization: `Bearer ${REGOLO_TOKEN}`
  }

  const data = {
    model: 'llama3.1:70b-instruct-q8_0',
    messages: [
      {
        role: 'system',
        content:
          'Sei un assistente esperto in commercio internazionale e analisi di business.'
      },
      { role: 'user', content: prompt }
    ]
  }

  try {
    const response = await fetch('https://api.regolo.ai/v1/chat/completions', {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(data)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const result = await response.json()
    return NextResponse.json({ content: result.choices[0].message.content })
  } catch (error) {
    console.error('Error:', error)
    return NextResponse.json(
      { message: 'Error analyzing response' },
      { status: 500 }
    )
  }
}
