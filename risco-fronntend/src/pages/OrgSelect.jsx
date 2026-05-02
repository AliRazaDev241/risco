// import { useState } from "react"

// export default function OrgSelect() {
//   const [mode, setMode] = useState(null) // "join" | "create"
//   const [orgName, setOrgName] = useState("")
//   const [error, setError] = useState("")
//   const [loading, setLoading] = useState(false)

//   const handleSubmit = (e) => {
//     e.preventDefault()
//     setError("")

//     if (!orgName.trim()) {
//       setError("Please enter an organization name")
//       return
//     }

//     setLoading(true)

//     setTimeout(() => {
//       if (mode === "join") {
//         // Mock: pretend org exists
//         if (orgName.toLowerCase() === "risco") {
//           localStorage.setItem("org", orgName)
//           alert("Joined org! Redirect to dashboard.")
//         } else {
//           setError("Organization not found")
//         }
//       } else {
//         // Mock: create org
//         localStorage.setItem("org", orgName)
//         alert("Organization created! Redirect to dashboard.")
//       }
//       setLoading(false)
//     }, 1000)
//   }

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#e8efec] to-[#d0e0da] px-4">

//       {/* Background circles */}
//       <div className="absolute w-[400px] h-[400px] border-2 border-teal-600/20 rounded-full top-[-80px] left-[-80px]" />
//       <div className="absolute w-[200px] h-[200px] border-2 border-teal-600/20 rounded-full bottom-[60px] right-[-40px]" />
//       <div className="absolute w-[80px] h-[80px] bg-teal-600/30 rounded-full top-[80px] left-[38%]" />
//       <div className="absolute w-[40px] h-[40px] bg-[#C9A84C]/30 rounded-full bottom-[120px] right-[18%]" />

//       {/* Card */}
//       <div className="relative w-full max-w-md bg-white/70 backdrop-blur-xl border border-teal-100 rounded-2xl p-8 shadow-xl">

//         {/* Header */}
//         <div className="text-center mb-8">
//           <h1 className="text-4xl font-black text-[#1a3a32] tracking-tight">
//             RIS<span className="text-[#C9A84C]">CO</span>
//           </h1>
//           <p className="text-sm font-semibold text-teal-700 mt-1">
//             Set up your workspace
//           </p>
//           <p className="text-xs text-gray-400 mt-1">
//             Join an existing organization or create a new one
//           </p>
//         </div>

//         {/* Mode picker — shown first */}
//         {!mode && (
//           <div className="space-y-3">
//             <button
//               onClick={() => setMode("join")}
//               className="w-full py-4 rounded-xl border-2 border-teal-200 bg-white/50 text-[#1a3a32] font-semibold text-sm hover:border-teal-500 hover:bg-teal-50 transition-all duration-200"
//             >
//               Join an Organization
//             </button>
//             <button
//               onClick={() => setMode("create")}
//               className="w-full py-4 rounded-xl border-2 border-[#C9A84C]/40 bg-white/50 text-[#1a3a32] font-semibold text-sm hover:border-[#C9A84C] hover:bg-[#fffbeb] transition-all duration-200"
//             >
//               Create an Organization
//             </button>
//           </div>
//         )}

//         {/* Form — shown after mode is picked */}
//         {mode && (
//           <form className="space-y-5" onSubmit={handleSubmit}>

//             {/* Back button */}
//             <button
//               type="button"
//               onClick={() => { setMode(null); setOrgName(""); setError("") }}
//               className="text-xs text-gray-400 hover:text-teal-700 transition-colors"
//             >
//               ← Back
//             </button>

//             <div>
//               <label className="text-xs font-medium text-gray-500">
//                 {mode === "join" ? "Organization Name" : "New Organization Name"}
//               </label>
//               <input
//                 type="text"
//                 placeholder={mode === "join" ? "Enter your organization name" : "e.g. Risco Labs"}
//                 value={orgName}
//                 onChange={(e) => setOrgName(e.target.value)}
//                 className="w-full mt-1 px-4 py-3 bg-white border border-teal-200 rounded-lg text-gray-800 placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-500"
//               />
//             </div>

//             {error && (
//               <p style={{ color: "red", fontSize: "13px" }}>{error}</p>
//             )}

//             <button
//               type="submit"
//               disabled={loading}
//               className="w-3/4 mx-auto block py-3 rounded-lg bg-teal-700 text-white font-semibold text-sm tracking-widest uppercase hover:bg-teal-600 transition-all duration-300 shadow-md hover:shadow-teal-300/50 disabled:opacity-50 disabled:cursor-not-allowed"
//             >
//               {loading
//                 ? "Please wait..."
//                 : mode === "join"
//                 ? "Join Organization"
//                 : "Create Organization"}
//             </button>
//           </form>
//         )}

//         {/* Footer */}
//         <div className="mt-6 text-center text-xs text-gray-400">
//           🔒 Protected with 256-bit encryption
//         </div>
//       </div>
//     </div>
//   )
// }

import { useState } from "react"

export default function OrgSelect() {
  const [mode, setMode] = useState(null)
  const [orgName, setOrgName] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const userId = localStorage.getItem("user_id")

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")

    if (!orgName.trim()) {
      setError("Please enter an organization name")
      return
    }

    setLoading(true)

    try {
      if (mode === "join") {
        const response = await fetch("http://127.0.0.1:8000/organizations/join", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ org_name: orgName, user_id: parseInt(userId) }),
        })
        const data = await response.json()
        if (response.ok) {
          // localStorage.setItem("org", data.org_name)
          localStorage.setItem("org", data.org_name)
          localStorage.setItem("org_id", data.id)
          window.location.href = "/dashboard"
        } else {
          setError(data.detail || "Could not join organization")
        }

      } else {
        const response = await fetch(`http://127.0.0.1:8000/organizations/?creator_id=${userId}&role_id=1`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ org_name: orgName }),
        })
        const data = await response.json()
        if (response.ok) {
          // localStorage.setItem("org", data.org_name)
          localStorage.setItem("org", data.org_name)
          localStorage.setItem("org_id", data.id)
          window.location.href = "/dashboard"
        } else {
          setError(data.detail || "Could not create organization")
        }
      }
    } catch (err) {
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
            Set up your workspace
          </p>
          <p className="text-xs text-gray-400 mt-1">
            Join an existing organization or create a new one
          </p>
        </div>

        {!mode && (
          <div className="space-y-3">
            <button
              onClick={() => setMode("join")}
              className="w-full py-4 rounded-xl border-2 border-teal-200 bg-white/50 text-[#1a3a32] font-semibold text-sm hover:border-teal-500 hover:bg-teal-50 transition-all duration-200"
            >
              Join an Organization
            </button>
            <button
              onClick={() => setMode("create")}
              className="w-full py-4 rounded-xl border-2 border-[#C9A84C]/40 bg-white/50 text-[#1a3a32] font-semibold text-sm hover:border-[#C9A84C] hover:bg-[#fffbeb] transition-all duration-200"
            >
              Create an Organization
            </button>
          </div>
        )}

        {mode && (
          <form className="space-y-5" onSubmit={handleSubmit}>
            <button
              type="button"
              onClick={() => { setMode(null); setOrgName(""); setError("") }}
              className="text-xs text-gray-400 hover:text-teal-700 transition-colors"
            >
              ← Back
            </button>

            <div>
              <label className="text-xs font-medium text-gray-500">
                {mode === "join" ? "Organization Name" : "New Organization Name"}
              </label>
              <input
                type="text"
                placeholder={mode === "join" ? "Enter your organization name" : "e.g. Risco Labs"}
                value={orgName}
                onChange={(e) => setOrgName(e.target.value)}
                className="w-full mt-1 px-4 py-3 bg-white border border-teal-200 rounded-lg text-gray-800 placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>

            {error && <p className="text-red-500 text-xs text-center">{error}</p>}

            <button
              type="submit"
              disabled={loading}
              className="w-3/4 mx-auto block py-3 rounded-lg bg-teal-700 text-white font-semibold text-sm tracking-widest uppercase hover:bg-teal-600 transition-all duration-300 shadow-md hover:shadow-teal-300/50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Please wait..." : mode === "join" ? "Join Organization" : "Create Organization"}
            </button>
          </form>
        )}

        <div className="mt-6 text-center text-xs text-gray-400">
          🔒 Protected with 256-bit encryption
        </div>
      </div>
    </div>
  )
}