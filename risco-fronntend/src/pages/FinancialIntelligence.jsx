import { useState, useEffect } from "react"
import PropTypes from 'prop-types'

const BASE = "http://127.0.0.1:8000"

// ── Gauge ──
const Gauge = ({ score }) => {
  const size = 180, cx = 90, cy = 90, r = 72, stroke = 14
  const start = Math.PI * 0.8, end = Math.PI * 2.2
  const pct = Math.min(Math.max(score / 100, 0), 1)
  const angle = start + pct * (end - start)
  const polar = (a, radius) => [cx + radius * Math.cos(a), cy + radius * Math.sin(a)]
  const arc = (a1, a2, radius) => {
    const [x1, y1] = polar(a1, radius)
    const [x2, y2] = polar(a2, radius)
    const large = (a2 - a1) > Math.PI ? 1 : 0
    return `M ${x1} ${y1} A ${radius} ${radius} 0 ${large} 1 ${x2} ${y2}`
  }
  let color
  if (score >= 70) color = "#1D9E75"
  else if (score >= 40) color = "#BA7517"
  else color = "#E24B4A"

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <path d={arc(start, end, r)} fill="none" stroke="#e5e7eb" strokeWidth={stroke} strokeLinecap="round"/>
      {pct > 0 && <path d={arc(start, angle, r)} fill="none" stroke={color} strokeWidth={stroke} strokeLinecap="round"/>}
      <text x={cx} y={cy - 6} textAnchor="middle" fontSize="28" fontWeight="500" fill={color}>{score.toFixed(0)}</text>
      <text x={cx} y={cy + 14} textAnchor="middle" fontSize="11" fill="#6b7280">out of 100</text>
    </svg>
  )
}

Gauge.propTypes = {
  score: PropTypes.number.isRequired,
}

// ── Pagination ──
const Pagination = ({ page, total, onPrev, onNext }) => (
  <div className="flex items-center justify-between mt-3 pt-2 border-t border-teal-50">
    <button onClick={onPrev} disabled={page <= 1}
      className="text-xs text-teal-700 disabled:text-gray-300 hover:underline">← Prev</button>
    <span className="text-xs text-gray-400">{page} / {total}</span>
    <button onClick={onNext} disabled={page >= total}
      className="text-xs text-teal-700 disabled:text-gray-300 hover:underline">Next →</button>
  </div>
)

Pagination.propTypes = {
  page: PropTypes.number.isRequired,
  total: PropTypes.number.isRequired,
  onPrev: PropTypes.func.isRequired,
  onNext: PropTypes.func.isRequired,
}

// ── Revenue Table ──
const RevenueTable = ({ items, type, page, totalPages, onPageChange, editingId, editDate, setEditDate, setEditingId, patchLoading, handlePatchDate, fmt, fmtDate, thClass, tdClass }) => (
  <div className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-5 shadow-sm">
    <h3 className="text-sm font-bold text-[#1a3a32] mb-4">
      {type === "Recurring" ? "Recurring Revenue" : "One Time Revenue"}
    </h3>
    {items.length === 0 ? (
      <p className="text-xs text-gray-400">No entries found</p>
    ) : (
      <table className="w-full">
        <thead>
          <tr>
            <th className={thClass}>Client</th>
            <th className={thClass}>Expected</th>
            <th className={thClass}>Received</th>
            <th className={thClass}>Amount</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id} className="border-t border-teal-50">
              <td className={tdClass}>
                <p>{item.client_name}</p>
                <p className="text-gray-400">{item.client_email}</p>
              </td>
              <td className={tdClass}>{fmtDate(item.date_expected)}</td>
              <td className={tdClass}>
                {editingId === item.id ? (
                  <div className="flex items-center gap-1">
                    <input type="date" value={editDate}
                      onChange={e => setEditDate(e.target.value)}
                      className="text-xs border border-teal-200 rounded px-1 py-0.5"/>
                    <button onClick={() => handlePatchDate(item.id, type)}
                      disabled={patchLoading}
                      className="text-xs text-teal-600 hover:underline">
                      {patchLoading ? "..." : "Save"}
                    </button>
                    <button onClick={() => setEditingId(null)}
                      className="text-xs text-gray-400 hover:underline">Cancel</button>
                  </div>
                ) : (
                  <button
                    type="button"
                    onClick={() => { setEditingId(item.id); setEditDate("") }}
                    className={`cursor-pointer bg-transparent border-none p-0 ${item.date_received ? "text-gray-700" : "text-teal-500 hover:underline"}`}>
                    {item.date_received
                      ? new Date(item.date_received).toLocaleDateString()
                      : "Set date"}
                  </button>
                )}
              </td>
              <td className={tdClass + " font-medium"}>{fmt(item.amount)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    )}
    <Pagination
      page={page} total={totalPages}
      onPrev={() => onPageChange(page - 1)}
      onNext={() => onPageChange(page + 1)}
    />
  </div>
)

RevenueTable.propTypes = {
  items: PropTypes.array.isRequired,
  type: PropTypes.string.isRequired,
  page: PropTypes.number.isRequired,
  totalPages: PropTypes.number.isRequired,
  onPageChange: PropTypes.func.isRequired,
  editingId: PropTypes.number,
  editDate: PropTypes.string.isRequired,
  setEditDate: PropTypes.func.isRequired,
  setEditingId: PropTypes.func.isRequired,
  patchLoading: PropTypes.bool.isRequired,
  handlePatchDate: PropTypes.func.isRequired,
  fmt: PropTypes.func.isRequired,
  fmtDate: PropTypes.func.isRequired,
  thClass: PropTypes.string.isRequired,
  tdClass: PropTypes.string.isRequired,
}

// ── Expense Table ──
const ExpenseTable = ({ items, type, page, totalPages, onPageChange, fmt, fmtDate, thClass, tdClass }) => (
  <div className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-5 shadow-sm">
    <h3 className="text-sm font-bold text-[#1a3a32] mb-4">
      {type === "Recurring" ? "Recurring Expenses" : "One Time Expenses"}
    </h3>
    {items.length === 0 ? (
      <p className="text-xs text-gray-400">No entries found</p>
    ) : (
      <table className="w-full">
        <thead>
          <tr>
            <th className={thClass}>Urgency</th>
            <th className={thClass}>Date</th>
            <th className={thClass}>Amount</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id} className="border-t border-teal-50">
              <td className={tdClass}>
                <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                  item.urgency === "Critical"
                    ? "bg-red-50 text-red-500"
                    : "bg-gray-100 text-gray-500"
                }`}>{item.urgency}</span>
              </td>
              <td className={tdClass}>{fmtDate(item.date)}</td>
              <td className={tdClass + " font-medium"}>{fmt(item.amount)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    )}
    <Pagination
      page={page} total={totalPages}
      onPrev={() => onPageChange(page - 1)}
      onNext={() => onPageChange(page + 1)}
    />
  </div>
)

ExpenseTable.propTypes = {
  items: PropTypes.array.isRequired,
  type: PropTypes.string.isRequired,
  page: PropTypes.number.isRequired,
  totalPages: PropTypes.number.isRequired,
  onPageChange: PropTypes.func.isRequired,
  fmt: PropTypes.func.isRequired,
  fmtDate: PropTypes.func.isRequired,
  thClass: PropTypes.string.isRequired,
  tdClass: PropTypes.string.isRequired,
}

export default function FinancialIntelligence() {
  const orgId = Number.parseInt(localStorage.getItem("org_id"))

  // ── Metrics State ──
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  // ── Revenue State ──
  const [recurringRevenue, setRecurringRevenue] = useState([])
  const [oneTimeRevenue, setOneTimeRevenue] = useState([])
  const [recurringRevPage, setRecurringRevPage] = useState(1)
  const [oneTimeRevPage, setOneTimeRevPage] = useState(1)
  const [recurringRevTotalPages, setRecurringRevTotalPages] = useState(1)
  const [oneTimeRevTotalPages, setOneTimeRevTotalPages] = useState(1)

  // ── Expense State ──
  const [recurringExp, setRecurringExp] = useState([])
  const [oneTimeExp, setOneTimeExp] = useState([])
  const [recurringExpPage, setRecurringExpPage] = useState(1)
  const [oneTimeExpPage, setOneTimeExpPage] = useState(1)
  const [recurringExpTotalPages, setRecurringExpTotalPages] = useState(1)
  const [oneTimeExpTotalPages, setOneTimeExpTotalPages] = useState(1)

  // ── Inline date edit state ──
  const [editingId, setEditingId] = useState(null)
  const [editDate, setEditDate] = useState("")
  const [patchLoading, setPatchLoading] = useState(false)

  // ── Fetch all on load ──
  useEffect(() => {
    fetchMetrics()
    fetchRevenue("Recurring", 1)
    fetchRevenue("One_Time", 1)
    fetchExpenses("Recurring", 1)
    fetchExpenses("One_Time", 1)
  }, [])

  // ── Fetch Metrics ──
  const fetchMetrics = async () => {
    setLoading(true); setError("")
    try {
      const res = await fetch(`${BASE}/financial/intelligence?org_id=${orgId}`)
      const data = await res.json()
      if (res.ok) setMetrics(data)
      else setError(data.detail || "Failed to load metrics")
    } catch { setError("Could not connect to server") }
    finally { setLoading(false) }
  }

  // ── Fetch Revenue ──
  const fetchRevenue = async (type, page) => {
    try {
      const res = await fetch(`${BASE}/revenue/?org_id=${orgId}&revenue_type=${type}&page_no=${page}`)
      const data = await res.json()
      if (res.ok) {
        if (type === "Recurring") {
          setRecurringRevenue(data.items)
          setRecurringRevTotalPages(data.total_pages)
          setRecurringRevPage(data.current_page)
        } else {
          setOneTimeRevenue(data.items)
          setOneTimeRevTotalPages(data.total_pages)
          setOneTimeRevPage(data.current_page)
        }
      }
    } catch { console.error("Failed to fetch revenue") }
  }

  // ── Fetch Expenses ──
  const fetchExpenses = async (type, page) => {
    try {
      const res = await fetch(`${BASE}/expenses/?org_id=${orgId}&expense_type=${type}&page_no=${page}`)
      const data = await res.json()
      if (res.ok) {
        if (type === "Recurring") {
          setRecurringExp(data.items)
          setRecurringExpTotalPages(data.total_pages)
          setRecurringExpPage(data.current_page)
        } else {
          setOneTimeExp(data.items)
          setOneTimeExpTotalPages(data.total_pages)
          setOneTimeExpPage(data.current_page)
        }
      }
    } catch { console.error("Failed to fetch expenses") }
  }

  // ── Patch date received ──
  const handlePatchDate = async (revenueId, type) => {
    if (!editDate) return
    setPatchLoading(true)
    try {
      const res = await fetch(`${BASE}/revenue/${revenueId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ date_received: editDate + "T00:00:00" })
      })
      if (res.ok) {
        setEditingId(null)
        setEditDate("")
        fetchRevenue(type, type === "Recurring" ? recurringRevPage : oneTimeRevPage)
        fetchMetrics()
      }
    } catch { console.error("Failed to update date") }
    finally { setPatchLoading(false) }
  }

  // ── Helpers ──
  const fmt = (n) => {
    if (n >= 1000000) return "$" + (n / 1000000).toFixed(1) + "M"
    if (n >= 1000) return "$" + (n / 1000).toFixed(1) + "K"
    return "$" + Math.round(n)
  }

  const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : null

  const riskLabel = (risk) => {
    if (risk < 0.25) return { text: "Low Risk", color: "text-teal-600" }
    if (risk < 0.5) return { text: "Moderate", color: "text-amber-500" }
    return { text: "High Risk", color: "text-red-500" }
  }

  // ── Shared styles ──
  const thClass = "text-xs text-gray-400 font-medium text-left pb-2"
  const tdClass = "text-xs text-gray-700 py-2 pr-3"

  // ── Render ──
  return (
    <div>
      {/* Header */}
      <h2 className="text-2xl font-bold text-[#1a3a32] mb-1">Financial Intelligence</h2>
      <p className="text-gray-400 text-sm mb-8">Revenue health, reliability and expense tracking.</p>

      {loading && <p className="text-sm text-gray-400">Loading metrics...</p>}
      {error && <p className="text-sm text-red-500">{error}</p>}

      {metrics && (
        <div className="flex flex-col gap-5">

          {/* ── Upper Section ── */}
          <div className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-6 shadow-sm">
            <div className="flex flex-wrap gap-6 items-center">
              <div className="flex flex-col items-center gap-2">
                <Gauge score={metrics.revenue_reliability_score || 0} />
                <p className="text-xs text-gray-500 text-center">Revenue Reliability Score</p>
              </div>
              <div className="flex-1 grid grid-cols-2 gap-4 min-w-[280px]">
                <div className="bg-[#f0faf6] rounded-xl p-4">
                  <p className="text-xs text-gray-500 mb-1">Revenue Concentration Risk</p>
                  <p className={`text-lg font-medium ${riskLabel(metrics.revenue_concentration_risk || 0).color}`}>
                    {riskLabel(metrics.revenue_concentration_risk || 0).text}
                  </p>
                  <p className="text-xs text-gray-400 mt-1">
                    {((metrics.revenue_concentration_risk || 0) * 100).toFixed(1)}% HHI index
                  </p>
                </div>
                <div className="bg-[#f0faf6] rounded-xl p-4">
                  <p className="text-xs text-gray-500 mb-1">Reliable Revenue</p>
                  <p className="text-lg font-medium text-[#1a3a32]">{fmt(metrics.reliable_revenue || 0)}</p>
                  <p className="text-xs text-gray-400 mt-1">weighted by client score</p>
                </div>
                <div className="bg-[#f0faf6] rounded-xl p-4">
                  <p className="text-xs text-gray-500 mb-1">Total Revenue Expected</p>
                  <p className="text-lg font-medium text-[#1a3a32]">{fmt(metrics.total_revenue_expected || 0)}</p>
                  <p className="text-xs text-gray-400 mt-1">this month</p>
                </div>
                <div className="bg-[#f0faf6] rounded-xl p-4">
                  <p className="text-xs text-gray-500 mb-1">Actual Revenue</p>
                  <p className="text-lg font-medium text-[#1a3a32]">{fmt(metrics.actual_revenue || 0)}</p>
                  <p className="text-xs text-gray-400 mt-1">received this month</p>
                </div>
              </div>
            </div>
          </div>

          {/* ── Revenue Tables ── */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <RevenueTable
              items={recurringRevenue} type="Recurring"
              page={recurringRevPage} totalPages={recurringRevTotalPages}
              onPageChange={(p) => { setRecurringRevPage(p); fetchRevenue("Recurring", p) }}
              editingId={editingId} editDate={editDate}
              setEditDate={setEditDate} setEditingId={setEditingId}
              patchLoading={patchLoading} handlePatchDate={handlePatchDate}
              fmt={fmt} fmtDate={fmtDate} thClass={thClass} tdClass={tdClass}
            />
            <RevenueTable
              items={oneTimeRevenue} type="One_Time"
              page={oneTimeRevPage} totalPages={oneTimeRevTotalPages}
              onPageChange={(p) => { setOneTimeRevPage(p); fetchRevenue("One_Time", p) }}
              editingId={editingId} editDate={editDate}
              setEditDate={setEditDate} setEditingId={setEditingId}
              patchLoading={patchLoading} handlePatchDate={handlePatchDate}
              fmt={fmt} fmtDate={fmtDate} thClass={thClass} tdClass={tdClass}
            />
          </div>

          {/* ── Expense Tables ── */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <ExpenseTable
              items={recurringExp} type="Recurring"
              page={recurringExpPage} totalPages={recurringExpTotalPages}
              onPageChange={(p) => { setRecurringExpPage(p); fetchExpenses("Recurring", p) }}
              fmt={fmt} fmtDate={fmtDate} thClass={thClass} tdClass={tdClass}
            />
            <ExpenseTable
              items={oneTimeExp} type="One_Time"
              page={oneTimeExpPage} totalPages={oneTimeExpTotalPages}
              onPageChange={(p) => { setOneTimeExpPage(p); fetchExpenses("One_Time", p) }}
              fmt={fmt} fmtDate={fmtDate} thClass={thClass} tdClass={tdClass}
            />
          </div>

        </div>
      )}
    </div>
  )
}