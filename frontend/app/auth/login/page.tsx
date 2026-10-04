"use client";

import { signIn } from "next-auth/react";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-8">
      <div className="bg-white rounded-xl p-8 shadow-2xl max-w-md w-full">
        <h2 className="text-2xl font-bold mb-6 text-center">Sign In</h2>
        
        {/* Google Sign In Button */}
        <div className="mb-6">
          <button 
            onClick={() => signIn("google")}
            className="w-full bg-blue-600 text-white py-3 rounded-md font-medium hover:bg-blue-700 transition-colors">
            Continue with Google
          </button>
        </div>
        
        {/* Credentials Form */}
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Email address</label>
            <input 
              type="email" 
              placeholder="jsmith@example.com"
              className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Password</label>
            <input 
              type="password" 
              placeholder="••••••••"
              className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <button 
            type="submit"
            className="w-full bg-blue-600 text-white py-3 rounded-md font-medium hover:bg-blue-700 transition-colors">
            Sign In
          </button>
        </form>
        
        <p className="text-center text-sm mt-6">
          Don't have an account? <a href="/auth/signup" className="underline text-blue-600">Sign up</a>
        </p>
      </div>
    </div>
  );
}
