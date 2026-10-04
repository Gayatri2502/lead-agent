"use client";

import { signIn } from "next-auth/react";

export default function SignupPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-8">
      <div className="bg-white rounded-xl p-8 shadow-2xl max-w-md w-full">
        <h2 className="text-2xl font-bold mb-6 text-center">Sign Up</h2>
        
        <p className="text-center text-sm mb-8">
          Welcome! Please sign in with your Google account or complete the form below.
        </p>
        
        {/* Google Sign In Button */}
        <div className="mb-6">
          <button 
            onClick={() => signIn("google")}
            className="w-full bg-blue-600 text-white py-3 rounded-md font-medium hover:bg-blue-700 transition-colors">
            Continue with Google
          </button>
        </div>
        
        <p className="text-center text-sm mt-8">
          Already have an account? <a href="/auth/login" className="underline text-blue-600">Sign in</a>
        </p>
      </div>
    </div>
  );
}
