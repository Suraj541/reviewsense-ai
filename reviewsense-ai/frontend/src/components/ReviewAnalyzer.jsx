import React, { useState } from 'react'
import { auth } from '../firebase'

const ReviewAnalyzer = () => {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [gptAnalysis, setGptAnalysis] = useState(null)

  const analyzeReview = async () => {
    try {
      const token = await auth.currentUser.getIdToken()
      
      // Basic sentiment analysis
      const sentimentResponse = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ text })
      })
      setResult(await sentimentResponse.json())

      // GPT-4 advanced analysis
      const gptResponse = await fetch('http://localhost:8000/analyze/gpt4', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ text })
      })
      setGptAnalysis(await gptResponse.json())
      
    } catch (error) {
      console.error("Analysis failed:", error)
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Review Analysis</h2>
        
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full p-3 border rounded-md mb-4"
          placeholder="Paste your review here..."
          rows="5"
        />
        
        <button
          onClick={analyzeReview}
          className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors"
        >
          Analyze Text
        </button>

        {result && (
          <div className="mt-6 p-4 bg-gray-50 rounded-md">
            <h3 className="text-lg font-medium mb-2">Basic Analysis</h3>
            <p className="mb-1">Sentiment: {result.sentiment}</p>
            <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
          </div>
        )}

        {gptAnalysis && (
          <div className="mt-6 p-4 bg-gray-50 rounded-md">
            <h3 className="text-lg font-medium mb-2">Advanced Insights</h3>
            <p className="whitespace-pre-wrap">{gptAnalysis.analysis}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default ReviewAnalyzer