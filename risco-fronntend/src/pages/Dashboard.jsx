import { useState, useEffect, useRef } from "react";
import { Chart, registerables } from "chart.js"
Chart.register(...registerables)
import Operations from "./Operations"
import FinancialIntelligence from "./FinancialIntelligence"

const BASE = "http://127.0.0.1:8000"

const navItems = [
  { id: "overview", label: "Dashboard" },
  { id: "finance", label: "Financial Intelligence" },
  { id: "operations", label: "Operations" },
];


function SnapshotGraph({ orgId, active }) {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  const [snapshotType, setSnapshotType] = useState("All")
  const [metricType, setMetricType] = useState("cash_balance")
  const [startDate, setStartDate] = useState(() => {
    const d = new Date()
    return `${d.getFullYear()}-01-01`
  })
  const [endDate, setEndDate] = useState(() => {
    const d = new Date()
    return `${d.getFullYear()}-12-31`
  })
  const [dateRangeMin, setDateRangeMin] = useState(null)
  const [dateRangeMax, setDateRangeMax] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [activePoint, setActivePoint] = useState(null)

  const snapshotTypes = ["Base", "Best", "Worst"]
  const lineColors = {
    Base:  { border: "#0f766e", bg: "rgba(15,118,110,0.08)", light: "#ccfbf1" },
    Best:  { border: "#3b82f6", bg: "rgba(59,130,246,0.06)", light: "#dbeafe" },
    Worst: { border: "#f43f5e", bg: "rgba(244,63,94,0.06)", light: "#ffe4e6" },
  }

  const metricLabels = {
    cash_balance: "Cash Balance",
    monthly_revenue: "Monthly Revenue",
    monthly_expense: "Monthly Expense",
  }

  const fetchData = async (types) => {
    setLoading(true); setError("")
    try {
      const results = await Promise.all(
        types.map(type =>
          fetch(`${BASE}/snapshots/graph`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              org_id: orgId,
              snapshot_type: type,
              metric_type: metricType,
              start_date: startDate + "T00:00:00",
              end_date: endDate + "T23:59:59"
            })
          }).then(r => r.json()).then(d => ({ type, ...d }))
        )
      )

      if (results[0]?.date_range_start) {
        setDateRangeMin(results[0].date_range_start.split("T")[0])
        setDateRangeMax(results[0].date_range_end.split("T")[0])
      }

      const allDates = [...new Set(
        results.flatMap(r => (r.data || []).map(d => d.snapshot_date.split("T")[0]))
      )].sort()

      const datasets = results.map(r => ({
        label: r.type,
        data: allDates.map(date => {
          const point = (r.data || []).find(d => d.snapshot_date.split("T")[0] === date)
          return point ? point.value : null
        }),
        borderColor: lineColors[r.type].border,
        backgroundColor: lineColors[r.type].bg,
        borderWidth: 2.5,
        pointRadius: 5,
        pointHoverRadius: 8,
        pointBackgroundColor: "#fff",
        pointBorderColor: lineColors[r.type].border,
        pointBorderWidth: 2.5,
        pointHoverBackgroundColor: lineColors[r.type].border,
        tension: 0.4,
        fill: false,
        spanGaps: true,
      }))

      renderChart(allDates, datasets)
    } catch {
      setError("Could not load graph data")
    } finally {
      setLoading(false)
    }
  }

  const renderChart = (labels, datasets) => {
    if (chartInstance.current) {
      chartInstance.current.destroy()
      chartInstance.current = null
    }
    if (!chartRef.current) return

    chartInstance.current = new Chart(chartRef.current, {
      type: "line",
      data: { labels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: "#1a3a32",
            titleColor: "#a7f3d0",
            bodyColor: "#fff",
            padding: 12,
            cornerRadius: 10,
            titleFont: { size: 11 },
            bodyFont: { size: 12, weight: "500" },
            callbacks: {
              label: ctx => {
                const v = ctx.parsed.y
                const abs = Math.abs(v)
                const fmt = abs >= 1000 ? (abs / 1000).toFixed(1) + "K" : abs
                return ` ${ctx.dataset.label}: ${v < 0 ? "-$" : "$"}${fmt}`
              }
            }
          }
        },
        scales: {
          x: {
            grid: { color: "rgba(0,0,0,0.03)", drawBorder: false },
            ticks: {
              font: { size: 11 },
              color: "#9ca3af",
              autoSkip: true,          // ← add this
              maxTicksLimit: 12,        // ← add this — shows max 12 labels
              callback: (_, i, vals) => {
                const label = chartInstance.current?.data.labels[i]
                if (!label) return ""
                const d = new Date(label)
                return d.toLocaleString("default", { month: "short", year: "numeric" })
              }
            },
            border: { display: false }
          },
          y: {
            grid: { color: "rgba(0,0,0,0.04)", drawBorder: false },
            ticks: {
              font: { size: 11 },
              color: "#9ca3af",
              callback: v => {
                const abs = Math.abs(v)
                const fmt = abs >= 1000 ? (abs / 1000).toFixed(0) + "K" : abs
                return (v < 0 ? "-$" : "$") + fmt
              }
            },
            border: { display: false }
          }
        }
      }
    })
  }

  useEffect(() => {
  if (active !== "overview") return
  const types = snapshotType === "All" ? snapshotTypes : [snapshotType]
  fetchData(types)
  return () => {
    if (chartInstance.current) {
      chartInstance.current.destroy()
      chartInstance.current = null
    }
  }
}, [snapshotType, metricType, startDate, endDate, active])

  return (
    <div className="mt-6 bg-white/80 backdrop-blur border border-teal-100 rounded-2xl shadow-sm overflow-hidden">

      {/* Top bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 px-6 pt-5 pb-4 border-b border-teal-50">
        <div>
          <h3 className="text-sm font-bold text-[#1a3a32]">Financial Snapshot</h3>
          <p className="text-xs text-gray-400 mt-0.5">{metricLabels[metricType]} over time</p>
        </div>

        {/* Snapshot type pills */}
        <div className="flex items-center gap-1 bg-[#f0faf6] rounded-xl p-1">
          {["All", "Base", "Best", "Worst"].map(t => (
            <button key={t} onClick={() => setSnapshotType(t)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                snapshotType === t
                  ? "bg-teal-700 text-white shadow-sm"
                  : "text-gray-500 hover:text-teal-700"
              }`}>
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Controls */}
      {/* Controls */}
      <div className="flex items-end justify-between gap-4 px-6 py-4 bg-[#fafffe] border-b border-teal-50">

        {/* Left — Metric + Date stacked */}
        <div className="flex flex-col gap-2">
          <div className="flex flex-col gap-1.5">
            <p className="text-xs text-gray-400 uppercase tracking-widest">Metric</p>
            <div className="flex bg-gray-100 rounded-xl p-1 gap-0.5">
              {Object.entries(metricLabels).map(([key, label]) => (
                <button key={key} onClick={() => setMetricType(key)}
                  className={`px-4 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${metricType === key
                      ? "bg-white text-teal-700 shadow-sm border border-teal-100"
                      : "text-gray-500 hover:text-gray-700"
                    }`}>
                  {label}
                </button>
              ))}
            </div>
          </div>

          {/* Date range below metric */}
          <div className="flex flex-col gap-1.5">
            <p className="text-xs text-gray-400 uppercase tracking-widest">Time Filter</p>
            <div className="flex items-center gap-2">
              <input type="date" value={startDate}
                min={dateRangeMin || undefined} max={endDate}
                onChange={e => setStartDate(e.target.value)}
                className="text-xs bg-white border border-gray-200 rounded-lg px-2.5 py-1.5 text-gray-600 focus:outline-none focus:border-teal-400 shadow-sm" />
              <span className="text-gray-400 text-xs">→</span>
              <input type="date" value={endDate}
                min={startDate} max={dateRangeMax || undefined}
                onChange={e => setEndDate(e.target.value)}
                className="text-xs bg-white border border-gray-200 rounded-lg px-2.5 py-1.5 text-gray-600 focus:outline-none focus:border-teal-400 shadow-sm" />
            </div>
          </div>
        </div>

        {/* Right — Legend aligned to bottom */}
        <div className="flex flex-col gap-1.5 items-end">
          <p className="text-xs text-gray-400 uppercase tracking-widest">Legend</p>
          <div className="flex items-center gap-4 bg-gray-100 rounded-xl px-4 py-2">
            {(snapshotType === "All" ? snapshotTypes : [snapshotType]).map(t => (
              <div key={t} className="flex items-center gap-1.5">
                <div className="w-6 h-0.5 rounded-full" style={{ background: lineColors[t].border }} />
                <div className="w-2 h-2 rounded-full border-2 bg-white" style={{ borderColor: lineColors[t].border }} />
                <span className="text-xs font-medium" style={{ color: lineColors[t].border }}>{t}</span>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Chart area */}
      <div className="px-6 pb-6">
        {error && <p className="text-xs text-red-400 mb-2">{error}</p>}
        {loading && (
          <div className="flex items-center gap-2 py-2 mb-2">
            <div className="w-2 h-2 rounded-full bg-teal-400 animate-pulse"/>
            <p className="text-xs text-gray-400">Loading chart...</p>
          </div>
        )}
        <div style={{ position: "relative", height: "300px" }}>
          <canvas ref={chartRef} role="img" aria-label="Financial snapshot line chart"/>
        </div>
        <p className="text-xs text-gray-300 text-center mt-3 tracking-wide uppercase">
          {metricLabels[metricType]} · Monthly Snapshots
        </p>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [active, setActive] = useState("overview");
  const orgId = parseInt(localStorage.getItem("org_id"))

  // ── Dashboard Metrics State ──
  const [dashMetrics, setDashMetrics] = useState(null)
  const [dashLoading, setDashLoading] = useState(true)
  const [dashError, setDashError] = useState("")

  useEffect(() => {
    if (active === "overview") fetchDashboard()
  }, [active])

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

            {/* Risk alert — only shows when runway is low */}
            {isLowRunway && (
              <div className="bg-red-50 border border-red-200 rounded-xl px-5 py-4">
                <p className="text-xs text-red-500 uppercase tracking-wider mb-1">⚠ Major Risk Alert</p>
                <p className="text-sm text-red-400">
                  Runway is {fmtRunway(runwayMonths)} — review burn rate immediately.
                </p>
              </div>
            )}

            {/* Graph — add this */}
            <SnapshotGraph orgId={orgId} active={active} />

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