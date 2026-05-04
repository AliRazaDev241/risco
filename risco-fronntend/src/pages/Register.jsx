import { useState } from "react"

export default function Register() {
  const [form, setForm] = useState({ email: "", password: "", first_name: "", last_name: "" })
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    setError("")
    setLoading(true)

    try {
      const response = await fetch("http://127.0.0.1:8000/users/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      })

      const data = await response.json()

      if (response.ok) {
        alert("Account created! Please login.")
        globalThis.location.href = "/"
      } else {
        setError(data.detail || "Registration failed")
      }
    } catch {
      setError("Could not connect to server. Is the backend running?")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#e8efec] to-[#d0e0da] px-4">

      <div className="absolute w-[400px] h-[400px] border-2 border-teal-600/20 rounded-full top-[-80px] left-[-80px]" />
      <div className="absolute w-[200px] h-[200px] border-2 border-teal-600/20 rounded-full bottom-[60px] right-[-40px]" />
      <div className="absolute w-[80px] h-[80px] bg-teal-600/30 rounded-full top-[80px] left-[38%]" />
      <div className="absolute w-[40px] h-[40px] bg-[#C9A84C]/30 rounded-full bottom-[120px] right-[18%]" />

      <div className="relative w-full max-w-md bg-white/70 backdrop-blur-xl border border-teal-100 rounded-2xl p-8 shadow-xl">

        <div className="text-center mb-8">
          <h1 className="text-4xl font-black text-[#1a3a32] tracking-tight">
            RIS<span className="text-[#C9A84C]">CO</span>
          </h1>
          <p className="text-sm font-semibold text-teal-700 mt-1">
            Create your account
          </p>
        </div>

        <form className="space-y-4" onSubmit={handleRegister}>
          <div className="flex gap-3">
            <div className="flex-1">
              <label htmlFor="first_name" className="text-xs font-medium text-gray-500">First Name</label>
              <input
                id="first_name"
                type="text"
                name="first_name"
                placeholder="John"
                value={form.first_name}
                onChange={handleChange}
                className="w-full mt-1 px-4 py-3 bg-white border border-teal-200 rounded-lg text-gray-800 placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>
            <div className="flex-1">
              <label htmlFor="last_name" className="text-xs font-medium text-gray-500">Last Name</label>
              <input
                id="last_name"
                type="text"
                name="last_name"
                placeholder="Doe"
                value={form.last_name}
                onChange={handleChange}
                className="w-full mt-1 px-4 py-3 bg-white border border-teal-200 rounded-lg text-gray-800 placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>
          </div>

          <div>
            <label htmlFor="email" className="text-xs font-medium text-gray-500">Email</label>
            <input
              id="email"
              type="email"
              name="email"
              placeholder="name@risco.com"
              value={form.email}
              onChange={handleChange}
              className="w-full mt-1 px-4 py-3 bg-white border border-teal-200 rounded-lg text-gray-800 placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
          </div>

          <div>
            <label htmlFor="password" className="text-xs font-medium text-gray-500">Password</label>
            <input
              id="password"
              type="password"
              name="password"
              placeholder="••••••••"
              value={form.password}
              onChange={handleChange}
              className="w-full mt-1 px-4 py-3 bg-white border border-teal-200 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
          </div>

          {error && <p className="text-red-500 text-xs text-center">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-3/4 mx-auto block py-3 rounded-lg bg-teal-700 text-white font-semibold text-sm tracking-widest uppercase hover:bg-teal-600 transition-all duration-300 shadow-md hover:shadow-teal-300/50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <div className="text-center mt-3">
          <a href="/" className="text-sm text-teal-700 hover:text-teal-400 transition-colors">
            Already have an account? Login
          </a>
        </div>

        <div className="mt-6 text-center text-xs text-gray-400">
          🔒 Protected with 256-bit encryption
        </div>
      </div>
    </div>
  )
}