import { useState } from "react"

export default function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e) => {
    e.preventDefault()
    setError("")
    setLoading(true)

    try {
      const response = await fetch("http://127.0.0.1:8000/users/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      })

      const data = await response.json()

      if (response.ok) {
        localStorage.setItem("token", data.token || "logged-in")
        localStorage.setItem("user_id", data.id)
        // window.location.href = "/orgselect"
        // Check if user already has an org
        const orgResponse = await fetch(`http://127.0.0.1:8000/organizations/user/${data.id}`)
        if (orgResponse.ok) {
          // User has an org, go to dashboard
          window.location.href = "/dashboard"
        } else {
          // User has no org, go to OrgSelect
          window.location.href = "/orgselect"
        }
      } else {
        setError(data.detail || "Invalid email or password")
      }
    } catch (err) {
      setError("Could not connect to server. Is the backend running?")
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#e8efec] to-[#d0e0da] px-4">

      {/* Background circles like the slide */}
      <div className="absolute w-[400px] h-[400px] border-2 border-teal-600/20 rounded-full top-[-80px] left-[-80px]" />
      <div className="absolute w-[200px] h-[200px] border-2 border-teal-600/20 rounded-full bottom-[60px] right-[-40px]" />
      <div className="absolute w-[80px] h-[80px] bg-teal-600/30 rounded-full top-[80px] left-[38%]" />
      <div className="absolute w-[40px] h-[40px] bg-[#C9A84C]/30 rounded-full bottom-[120px] right-[18%]" />

      {/* Card */}
      <div className="relative w-full max-w-md bg-white/70 backdrop-blur-xl border border-teal-100 rounded-2xl p-8 shadow-xl">

        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-black text-[#1a3a32] tracking-tight">
            RIS<span className="text-[#C9A84C]">CO</span>
          </h1>
          <p className="text-sm font-semibold text-teal-700 mt-1">
            Financial decisions, before they become risks
          </p>
          <p className="text-xs text-gray-400 mt-1">
            Secure access to your financial dashboard
          </p>
        </div>

        {/* Form */}
        <form className="space-y-5" onSubmit={handleLogin}>
          <div>
            <label className="text-xs font-medium text-gray-500">Email</label>
            <input
              type="email"
              placeholder="name@risco.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full mt-1 px-4 py-3 bg-white border border-teal-200 rounded-lg text-gray-800 placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
          </div>

          <div>
            <label className="text-xs font-medium text-gray-500">Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full mt-1 px-4 py-3 bg-white border border-teal-200 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
          </div>

          {/* Error message */}
          {error && (
            <p className="text-red-500 text-xs text-center">{error}</p>
          )}

          <div className="flex justify-between items-center text-xs text-gray-400">
            <label className="flex items-center gap-2">
              <input type="checkbox" className="accent-teal-600" />
              Remember me
            </label>
            <a href="#" className="hover:text-teal-700 transition-colors">
              Forgot password?
            </a>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-3/4 mx-auto block py-3 rounded-lg bg-teal-700 text-white font-semibold text-sm tracking-widest uppercase hover:bg-teal-600 transition-all duration-300 shadow-md hover:shadow-teal-300/50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Logging in..." : "Login to RISCO"}
          </button>
        </form>

        <div className="text-center mt-3">
          <a href="/register" className=" text-sm text-teal-700 hover:text-teal-400 transition-colors">
            Register Account
          </a>
        </div>

        {/* Security note */}
        <div className="mt-6 text-center text-xs text-gray-400">
          🔒 Protected with 256-bit encryption
        </div>
      </div>
    </div>
  )
}