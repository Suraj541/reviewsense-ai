import React, { useEffect, useState } from 'react';
import { auth } from './firebase';
import Auth from './components/Auth';
import ReviewAnalyzer from './components/ReviewAnalyzer';
import ReviewChart from './components/ReviewChart';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged(user => {
      setUser(user);
    });
    return () => unsubscribe();
  }, []);

  return (
    <div className="container mx-auto p-4 min-h-screen">
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-blue-600">ReviewSense AI</h1>
        {user && (
          <p className="mt-2 text-gray-600">
            Welcome, {user.email}!
          </p>
        )}
      </header>

      {user ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <ReviewAnalyzer />
          <ReviewChart />
        </div>
      ) : (
        <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
          <Auth />
        </div>
      )}
    </div>
  );
}

export default App;