import React from 'react'
import { auth, googleProvider } from '../firebase'
import { signInWithPopup, signOut } from 'firebase/auth'

const Auth = () => {
  const handleGoogleLogin = async () => {
    try {
      await signInWithPopup(auth, googleProvider)
    } catch (error) {
      console.error("Google login error:", error)
    }
  }

  return (
    <div className="space-y-4">
      <button
        onClick={handleGoogleLogin}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
      >
        Continue with Google
      </button>
      
      <button
        onClick={() => signOut(auth)}
        className="w-full bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition-colors"
      >
        Logout
      </button>
    </div>
  )
}

export default Auth