'use client'

import React, { useState, useEffect, useRef } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { IconArrowElbow } from '@/components/ui/icons'
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger
} from '@/components/ui/tooltip'
import { analyzeWithLLM } from '@/lib/regolo'
import { boolean } from 'zod'

const questions = [
  'Come si chiama la tua azienda?',
  'Quale é la tua Ragione Sociale (P.IVA)?',
  'In che settore operi?',
  'Da quanti anni è aperta e attiva la azienda?',
  'Su quali piattaforme social media è attualmente presente la vostra azienda?',
  'Avete già condotto campagne di marketing sui social media per mercati internazionali? Se sì, quali?',
  "Quali sono le vostre maggiori preoccupazioni riguardo l'esportazione in nuovi mercati?",
  'Quale prodotto e/o prodotti vorresti esportare?',
  "Vuoi spostare la produzione all'estero? Perché?",
  'Vuoi trovare nuovi fornitori per il tuo mercato? Perché?',
  ''
]

const customPrompts = [
  "Analizza il nome dell'azienda. Restutisci il nome della azienda, solamente il nome dell azienda nessuna parola extra, se non rilevi un nome azienda restituisci NO in maiuscolo cosi come ho scritto io",
  'Verifica il formato della P.IVA. È coerente con gli standard italiani? Se si, Restituisci solamente la PIVA senza nessuna parola extra, se non rilevi una pvia valida restituisci NO in minuscolo cosi come ho scritto io',
  'Analizza il settore indicato e cerca di capire se è in una di queste categorie: Agroalimentare, Moda,Lusso, Meccanica, Design, Arredamento, Nautico, Farmaceutico, Cosmetico, Tecnologico. Dammi una risposta con solo la parola del settore, solo se corrisponde senno rispondi NO, non voglio altre parole, una sola parola come risposta.',
  'Convertimi il numero in un numero intero che si avvicina di piu alla risposta, se non riescei rispondi solo NO, la risposta deve essere solo composta da un numero.',
  'Valuta la risposta fornita e dammi una risposta costituita dai nomi dei social network corretti seguiti da una , non devi aggiungere altre parole, se nessun social network e stato fornito rispondi NO',
  'Analizza la risposta e forniscimi i concetti chiavi delimitati da una virgola in caso non ci sia nulla rispondimi solo con un NO',
  'Analizza la risposta e forniscimi i concetti chiavi delimitati da una virgola in caso non ci sia nulla rispondimi solo con un NO',
  'Analizza la sentenza e fornisci una lista di prodotti. Se ci sono più prodotti, separali con una virgola. Se non vi sono prodotti identificabili, scrivi NO. La risposta deve contenere solo i nomi dei prodotti o NO.',
  'Valuta la frase e valuta se è positiva, se è positiva rispondimi SI, sennò rispondimi solamente NO',
  'Valuta la frase e valuta se è positiva, se è positiva rispondimi SI, sennò rispondimi solamente NO',
  ''
]

interface TypewriterEffectProps {
  text: string
  isDeleting: boolean
  onComplete: () => void
}

const TypewriterEffect: React.FC<TypewriterEffectProps> = ({
  text,
  isDeleting,
  onComplete
}) => {
  const [displayedText, setDisplayedText] = useState('')
  const [index, setIndex] = useState(0)

  useEffect(() => {
    if (isDeleting) {
      console.log('deleting')
      if (displayedText.length > 0) {
        const timer = setTimeout(() => {
          setDisplayedText(text.slice(0, displayedText.length - 1))
          setIndex(index - 1)
        }, 30)
        return () => clearTimeout(timer)
      } else {
        onComplete()
      }
    } else {
      if (index < text.length) {
        const timer = setTimeout(() => {
          setDisplayedText(text.slice(0, index + 1))
          setIndex(index + 1)
        }, 30)
        return () => clearTimeout(timer)
      } else {
        onComplete()
      }
    }
  }, [text, isDeleting, index, displayedText, onComplete])

  return (
    <p className="min-h-16 font-heading text-pretty text-center text-[22px] font-semibold tracking-tighter sm:text-[30px] md:text-[36px]">
      {displayedText}
    </p>
  )
}

export default function Component() {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState<number>(0)
  const [answers, setAnswers] = useState<string[]>([])
  const [currentAnswer, setCurrentAnswer] = useState<string>('')
  const [isTypingComplete, setIsTypingComplete] = useState<boolean>(false)
  const [isDeleting, setIsDeleting] = useState<boolean>(false)
  const [isAnswerSubmitted, setIsAnswerSubmitted] = useState<boolean>(false)
  const [displayedQuestion, setDisplayedQuestion] = useState<string>(
    questions[0]
  )
  const [displayNone, setDisplayNone] = useState<boolean>(false)
  const scrollAreaRef = useRef<HTMLDivElement | null>(null)
  const inputRef = useRef<HTMLInputElement | null>(null)

  function LoadingToCTA() {
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
      // Simulate a loading period of 3 seconds
      const timer = setTimeout(() => {
        setIsLoading(false)
        setDisplayNone(true)
      }, 2500)

      // Cleanup timer on unmount
      return () => clearTimeout(timer)
    }, [])

    return (
      <div className="h-10 w-10 relative flex flex-col items-center justify-center">
        <div
          className={`absolute top-1/4 left-1/2 transform -translate-x-1/2 -translate-y-1/2 transition-opacity duration-500 ease-in-out ${
            isLoading ? 'opacity-100' : 'opacity-0'
          }`}
        >
          <svg
            className="w-10 h-10 text-gray-300 animate-spin"
            viewBox="0 0 64 64"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
          >
            <path
              d="M32 3C35.8083 3 39.5794 3.75011 43.0978 5.20749C46.6163 6.66488 49.8132 8.80101 52.5061 11.4939C55.199 14.1868 57.3351 17.3837 58.7925 20.9022C60.2499 24.4206 61 28.1917 61 32C61 35.8083 60.2499 39.5794 58.7925 43.0978C57.3351 46.6163 55.199 49.8132 52.5061 52.5061C49.8132 55.199 46.6163 57.3351 43.0978 58.7925C39.5794 60.2499 35.8083 61 32 61C28.1917 61 24.4206 60.2499 20.9022 58.7925C17.3837 57.3351 14.1868 55.199 11.4939 52.5061C8.801 49.8132 6.66487 46.6163 5.20749 43.0978C3.7501 39.5794 3 35.8083 3 32C3 28.1917 3.75011 24.4206 5.2075 20.9022C6.66489 17.3837 8.80101 14.1868 11.4939 11.4939C14.1868 8.80099 17.3838 6.66487 20.9022 5.20749C24.4206 3.7501 28.1917 3 32 3L32 3Z"
              stroke="currentColor"
              strokeWidth="5"
              strokeLinecap="round"
              strokeLinejoin="round"
            ></path>
            <path
              d="M32 3C36.5778 3 41.0906 4.08374 45.1692 6.16256C49.2477 8.24138 52.7762 11.2562 55.466 14.9605C58.1558 18.6647 59.9304 22.9531 60.6448 27.4748C61.3591 31.9965 60.9928 36.6232 59.5759 40.9762"
              stroke="currentColor"
              strokeWidth="5"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="text-gray-900"
            ></path>
          </svg>
        </div>

        <div
          className={`absolute top-1/4 left-1/2 transform -translate-x-1/2 -translate-y-1/2 transition-opacity duration-500 ease-in-out ${
            isLoading ? 'opacity-0' : 'opacity-100'
          }`}
        >
          {/* Call-to-Action Button */}
          <a
            href="
http://localhost:8088/superset/dashboard/1/?native_filters_key=oG5qD9eSUsOarU6H582fpOtqcWYjE9_Ls3FYkMDZtKWCupfom0Zn9Sq3J14JN_xO"
            //se vuoi che si apra in una nuova finestra
            //target="_blank"
            rel="noopener noreferrer"
          >
            <Button
              className={`${isLoading ? 'cursor-default' : 'cursor-pointer'}`}
            >
              Accedi alla tua dashboard personalizzata
            </Button>
          </a>
        </div>
      </div>
    )
  }

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight
    }
  }, [currentQuestionIndex, isTypingComplete, isAnswerSubmitted])

  useEffect(() => {
    if (isTypingComplete && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isTypingComplete])

  useEffect(() => {
    // Update displayedQuestion when currentQuestionIndex changes
    setDisplayedQuestion(questions[currentQuestionIndex])
  }, [currentQuestionIndex])

  const handleSubmit = () => {
    if (currentAnswer.trim() === '') return
    setAnswers(prev => [...prev, currentAnswer])
    const question = questions[currentQuestionIndex]
    const customPrompt = customPrompts[currentQuestionIndex]
    analyzeWithLLM(question, currentAnswer, customPrompt)
    setIsAnswerSubmitted(true)
    setIsDeleting(true)
  }

  const handleTypingComplete = () => {
    setIsTypingComplete(true)
  }

  const handleDeletingComplete = () => {
    setCurrentAnswer('')
    setCurrentQuestionIndex(prev => prev + 1)
    setIsTypingComplete(false)
    setIsAnswerSubmitted(false)
    setIsDeleting(false)
  }

  return (
    <div className="relative flex min-h-[285px] w-full max-w-[49rem] flex-col items-stretch justify-center px-6 sm:min-h-[270px]">
      <div
        ref={scrollAreaRef}
        className="h-[60vh] overflow-hidden"
        style={{ scrollBehavior: 'smooth' }}
      >
        {currentQuestionIndex > questions.length - 2 ? (
          <div className="absolute top-1/4 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <LoadingToCTA />
          </div>
        ) : (
          ''
        )}
        <div
          className={`${displayNone ? 'hidden' : ''} space-y-12 transition-all duration-300 ease-in-out ${currentQuestionIndex > questions.length - 2 ? 'opacity-0' : 'opacity-100	'}`}
        >
          <div className={`transition-all duration-500 opacity-100`}>
            <div className="space-y-2">
              <TypewriterEffect
                text={displayedQuestion}
                isDeleting={isDeleting}
                onComplete={
                  isDeleting ? handleDeletingComplete : handleTypingComplete
                }
              />

              <div className="mt-2 transition-opacity duration-500 ease-in-out">
                <div className="relative">
                  <Input
                    ref={inputRef}
                    type="text"
                    value={currentAnswer}
                    disabled={isTypingComplete && !isDeleting ? false : true}
                    onChange={e => setCurrentAnswer(e.target.value)}
                    placeholder="Scrivi la tua risposta qui..."
                    className="pr-10 resize-none bg-transparent ring-0 focus-visible:ring-0 focus:ring-0 placeholder-blue-200"
                    onKeyPress={e => {
                      if (e.key === 'Enter') {
                        e.preventDefault()
                        handleSubmit()
                      }
                    }}
                  />
                  <div className="absolute right-0 top-[6px] sm:right-4">
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button onClick={handleSubmit} className="size-6 px-0">
                          <IconArrowElbow />
                          <span className="sr-only">Send message</span>
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent>Send message</TooltipContent>
                    </Tooltip>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
