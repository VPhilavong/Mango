'use client';

import React from 'react';

const LoginPage = () => {
  const handleSpotifyLogin = () => {
    window.location.href = 'http://localhost:8000/login';
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <button
        onClick={handleSpotifyLogin}
        className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded"
      >
        Login with Spotify
      </button>
    </div>
  );
};

export default LoginPage;