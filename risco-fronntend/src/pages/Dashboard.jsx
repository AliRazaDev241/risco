// import { useState } from "react";
// import Operations from "./Operations"
// import FinancialIntelligence from "./FinancialIntelligence"

// const navItems = [
//   { id: "overview", label: "Dashboard" },
//   { id: "finance", label: "Financial Intelligence" },
//   { id: "operations", label: "Operations" },
// ];

// const metrics = [
//   { label: "Cash Balance", value: "$124,500" },
//   { label: "Monthly Burn Rate", value: "$18,200" },
//   { label: "Runway", value: "6.8 months" },
//   { label: "Headcount", value: "12" },
//   { label: "Cash Runway Proj.", value: "Aug 2026" },
// ];

// export default function Dashboard() {
//   const [active, setActive] = useState("overview");

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-[#e8efec] to-[#d0e0da] flex text-[#1a3a32]">

//       {/* Sidebar */}
//       <aside className="w-56 min-h-screen bg-white/70 backdrop-blur-xl border-r border-teal-100 flex flex-col justify-between px-4 py-8 fixed">
//         <div>
//           <h1 className="text-lg font-black tracking-widest uppercase text-[#1a3a32] mb-2">RISCO</h1>
//           <p className="text-xs text-teal-600 font-medium mb-8">Financial Intelligence</p>

//           <nav className="space-y-1">
//             {navItems.map((item) => (
//               <button
//                 key={item.id}
//                 onClick={() => setActive(item.id)}
//                 className={`w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all duration-200 ${
//                   active === item.id
//                     ? "bg-teal-700 text-white font-medium shadow-sm"
//                     : "text-gray-500 hover:text-teal-800 hover:bg-teal-50"
//                 }`}
//               >
//                 {item.label}
//               </button>
//             ))}
//           </nav>
//         </div>

//         <button className="w-full text-left px-3 py-2.5 rounded-lg text-sm text-red-400 hover:bg-red-50 hover:text-red-500 transition-all duration-200">
//           Logout
//         </button>
//       </aside>

//       {/* Main content */}
//       <main className="ml-56 flex-1 p-8">

//         {active === "overview" && (
//           <div>
//             <h2 className="text-2xl font-bold text-[#1a3a32] mb-1">Dashboard Overview</h2>
//             <p className="text-gray-400 text-sm mb-8">Welcome back. Here's your financial snapshot.</p>

//             {/* Metrics row */}
//             <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-8">
//               {metrics.map((m) => (
//                 <div key={m.label} className="bg-white/70 backdrop-blur border border-teal-100 rounded-xl px-4 py-3 shadow-sm">
//                   <p className="text-xs text-gray-400 uppercase tracking-wider">{m.label}</p>
//                   <p className="text-base font-semibold text-[#1a3a32] mt-1">{m.value}</p>
//                 </div>
//               ))}
//             </div>

//             {/* Section cards */}
//             <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
//                <button
//                 onClick={() => setActive("finance")}
//                 className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-6 text-left hover:border-teal-400 hover:shadow-md transition-all duration-300"
//               >
//                 <div className="text-2xl mb-3">📉</div>
//                 <h3 className="text-base font-semibold text-[#1a3a32] mb-1">Financial Intelligence</h3>
//                 <p className="text-xs text-gray-400">Revenue · Reliability · Risk analysis</p>
//               </button>

//               <button
//                 onClick={() => setActive("operations")}
//                 className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-6 text-left hover:border-teal-400 hover:shadow-md transition-all duration-300"
//               >
//                 <div className="text-2xl mb-3">⚙️</div>
//                 <h3 className="text-base font-semibold text-[#1a3a32] mb-1">Operations</h3>
//                 <p className="text-xs text-gray-400">Team · Clients · Entries</p>
//               </button>
//             </div>

//             {/* Risk alert */}
//             <div className="bg-red-50 border border-red-200 rounded-xl px-5 py-4">
//               <p className="text-xs text-red-500 uppercase tracking-wider mb-1">⚠ Major Risk Alert</p>
//               <p className="text-sm text-red-400">Runway below 7 months — review burn rate immediately.</p>
//             </div>
//           </div>
//         )}

//         {active === "finance" && <FinancialIntelligence />}

//         {active === "operations" && (
//           <div>
//             <h2 className="text-2xl font-bold text-[#1a3a32] mb-1">Operations</h2>
//             <p className="text-gray-400 text-sm mb-8">Manage your team, clients and entries.</p>
//             <Operations />
//           </div>
//         )}

//       </main>
//     </div>
//   );
// }


import { useState, useEffect } from "react";
import Operations from "./Operations"
import FinancialIntelligence from "./FinancialIntelligence"

const BASE = "http://127.0.0.1:8000"

const navItems = [
  { id: "overview", label: "Dashboard" },
  { id: "finance", label: "Financial Intelligence" },
  { id: "operations", label: "Operations" },
];

export default function Dashboard() {
  const [active, setActive] = useState("overview");
  const orgId = parseInt(localStorage.getItem("org_id"))

  // ── Dashboard Metrics State ──
  const [dashMetrics, setDashMetrics] = useState(null)
  const [dashLoading, setDashLoading] = useState(true)
  const [dashError, setDashError] = useState("")

  useEffect(() => { fetchDashboard() }, [])

  const fetchDashboard = async () => {
    setDashLoading(true); setDashError("")
    try {
      const res = await fetch(`${BASE}/financial/dashboard?org_id=${orgId}`)
      const data = await res.json()
      if (res.ok) setDashMetrics(data)
      else setDashError(data.detail || "Failed to load dashboard")
    } catch { setDashError("Could not connect to server") }
    finally { setDashLoading(false) }
  }

  // ── Helpers ──
  const fmt = (n) => {
    if (n === null || n === undefined) return "—"
    if (n >= 1000000) return "$" + (n / 1000000).toFixed(1) + "M"
    if (n >= 1000) return "$" + (n / 1000).toFixed(1) + "K"
    return "$" + Math.round(n)
  }

  const fmtRunway = (months) => {
    if (months === null || months === undefined) return "—"
    return months.toFixed(1) + " months"
  }

  const fmtRunwayDate = (months) => {
    if (months === null || months === undefined) return "—"
    const d = new Date()
    d.setMonth(d.getMonth() + Math.round(months))
    return d.toLocaleString("default", { month: "short", year: "numeric" })
  }

  const metrics = dashMetrics ? [
    { label: "Cash Balance", value: fmt(dashMetrics.cash_balance) },
    { label: "Monthly Burn Rate", value: fmt(dashMetrics.burn_rate) },
    { label: "Runway", value: fmtRunway(dashMetrics.cash_runway) },
    { label: "Monthly Revenue", value: fmt(dashMetrics.monthly_revenue) },
    { label: "Headcount", value: dashMetrics.headcount?.toString() || "0" },
  ] : [
    { label: "Cash Balance", value: "..." },
    { label: "Monthly Burn Rate", value: "..." },
    { label: "Runway", value: "..." },
    { label: "Monthly Revenue", value: "..." },
    { label: "Headcount", value: "..." },
  ]

  const runwayMonths = dashMetrics?.cash_runway
  const isLowRunway = runwayMonths !== null && runwayMonths !== undefined && runwayMonths < 7

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#e8efec] to-[#d0e0da] flex text-[#1a3a32]">

      {/* Sidebar */}
      <aside className="w-56 min-h-screen bg-white/70 backdrop-blur-xl border-r border-teal-100 flex flex-col justify-between px-4 py-8 fixed">
        <div>
          <h1 className="text-lg font-black tracking-widest uppercase text-[#1a3a32] mb-2">RISCO</h1>
          <p className="text-xs text-teal-600 font-medium mb-8">Financial Intelligence</p>

          <nav className="space-y-1">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => setActive(item.id)}
                className={`w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all duration-200 ${
                  active === item.id
                    ? "bg-teal-700 text-white font-medium shadow-sm"
                    : "text-gray-500 hover:text-teal-800 hover:bg-teal-50"
                }`}
              >
                {item.label}
              </button>
            ))}
          </nav>
        </div>

        <button className="w-full text-left px-3 py-2.5 rounded-lg text-sm text-red-400 hover:bg-red-50 hover:text-red-500 transition-all duration-200">
          Logout
        </button>
      </aside>

      {/* Main content */}
      <main className="ml-56 flex-1 p-8">

        {/* ── Dashboard Overview ── */}
        {active === "overview" && (
          <div>
            <h2 className="text-2xl font-bold text-[#1a3a32] mb-1">Dashboard Overview</h2>
            <p className="text-gray-400 text-sm mb-8">Welcome back. Here's your financial snapshot.</p>

            {dashError && <p className="text-sm text-red-500 mb-4">{dashError}</p>}

            {/* Metrics row */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-8">
              {metrics.map((m) => (
                <div key={m.label} className="bg-white/70 backdrop-blur border border-teal-100 rounded-xl px-4 py-3 shadow-sm">
                  <p className="text-xs text-gray-400 uppercase tracking-wider">{m.label}</p>
                  <p className={`text-base font-semibold mt-1 ${dashLoading ? "text-gray-300" : "text-[#1a3a32]"}`}>
                    {m.value}
                  </p>
                </div>
              ))}
            </div>

            {/* Section cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <button
                onClick={() => setActive("finance")}
                className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-6 text-left hover:border-teal-400 hover:shadow-md transition-all duration-300"
              >
                <div className="text-2xl mb-3">📉</div>
                <h3 className="text-base font-semibold text-[#1a3a32] mb-1">Financial Intelligence</h3>
                <p className="text-xs text-gray-400">Revenue · Reliability · Risk analysis</p>
              </button>

              <button
                onClick={() => setActive("operations")}
                className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-6 text-left hover:border-teal-400 hover:shadow-md transition-all duration-300"
              >
                <div className="text-2xl mb-3">⚙️</div>
                <h3 className="text-base font-semibold text-[#1a3a32] mb-1">Operations</h3>
                <p className="text-xs text-gray-400">Team · Clients · Entries</p>
              </button>
            </div>

            {/* Risk alert — only shows when runway is low */}
            {isLowRunway && (
              <div className="bg-red-50 border border-red-200 rounded-xl px-5 py-4">
                <p className="text-xs text-red-500 uppercase tracking-wider mb-1">⚠ Major Risk Alert</p>
                <p className="text-sm text-red-400">
                  Runway is {fmtRunway(runwayMonths)} — review burn rate immediately.
                </p>
              </div>
            )}
          </div>
        )}

        {/* ── Financial Intelligence ── */}
        {active === "finance" && <FinancialIntelligence />}

        {/* ── Operations ── */}
        {active === "operations" && (
          <div>
            <h2 className="text-2xl font-bold text-[#1a3a32] mb-1">Operations</h2>
            <p className="text-gray-400 text-sm mb-8">Manage your team, clients and entries.</p>
            <Operations />
          </div>
        )}

      </main>
    </div>
  );
}