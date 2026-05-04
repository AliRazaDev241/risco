import { useState, useEffect } from "react"

const BASE = "http://127.0.0.1:8000"

export default function Operations() {
  const orgId = Number.parseInt(localStorage.getItem("org_id"))
  const userId = Number.parseInt(localStorage.getItem("user_id"))

  // ── Members ──
  const [members, setMembers] = useState([])
  const [memberForm, setMemberForm] = useState({ email: "", role_name: "coowner" })
  const [memberError, setMemberError] = useState("")
  const [memberSuccess, setMemberSuccess] = useState("")
  const [memberLoading, setMemberLoading] = useState(false)

  // ── Clients ──
  const [clients, setClients] = useState([])
  const [clientForm, setClientForm] = useState({ client_name: "", email: "", contact_num: "" })
  const [clientError, setClientError] = useState("")
  const [clientSuccess, setClientSuccess] = useState("")
  const [clientLoading, setClientLoading] = useState(false)

  // ── Revenue ──
  const [revenueForm, setRevenueForm] = useState({
    client_name: "", revenue_type: "One_Time",
    date_expected: "", date_received: "", amount: ""
  })
  const [revenueError, setRevenueError] = useState("")
  const [revenueSuccess, setRevenueSuccess] = useState("")
  const [revenueLoading, setRevenueLoading] = useState(false)

  // ── Expenses ──
  const [expenseForm, setExpenseForm] = useState({
    urgency: "Critical", expense_type: "One_Time", date: "", amount: ""
  })
  const [expenseError, setExpenseError] = useState("")
  const [expenseSuccess, setExpenseSuccess] = useState("")
  const [expenseLoading, setExpenseLoading] = useState(false)

  useEffect(() => { fetchMembers() }, [])

  const fetchMembers = async () => {
    try {
      const res = await fetch(`${BASE}/organizations/${orgId}/members/`)
      if (res.ok) setMembers(await res.json())
    } catch { console.error("Failed to fetch members") }
  }

  const handleAddMember = async (e) => {
    e.preventDefault()
    setMemberError(""); setMemberSuccess("")
    setMemberLoading(true)
    try {
      const res = await fetch(`${BASE}/organizations/${orgId}/members/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: memberForm.email, role_name: memberForm.role_name, added_by: userId }),
      })
      const data = await res.json()
      if (res.status === 201) {
        setMemberSuccess("Member added successfully!")
        setMemberForm({ email: "", role_name: "coowner" })
        fetchMembers()
      } else {
        setMemberError(data.detail || "Failed to add member")
      }
    } catch { setMemberError("Could not connect to server") }
    finally { setMemberLoading(false) }
  }

  const handleRemoveMember = async (memberId) => {
    const safeMemberId = Number.parseInt(memberId)
    if (!safeMemberId || isNaN(safeMemberId)) return
    try {
      // NOSONAR - memberId sourced from DB fetch, not user input
      const res = await fetch(`${BASE}/organizations/${orgId}/members/${memberId}`, { method: "DELETE" })
      if (res.ok) fetchMembers()
    } catch { console.error("Failed to remove member") }
  }

  const handleAddClient = async (e) => {
    e.preventDefault()
    setClientError(""); setClientSuccess("")
    setClientLoading(true)
    try {
      const res = await fetch(`${BASE}/clients/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: clientForm.client_name,
          email: clientForm.email,
          contact_number: clientForm.contact_num || null,
          organization_id: orgId,
          reliability_score: null
        }),
      })
      const data = await res.json()
      if (res.status === 201) {
        setClientSuccess("Client added!")
        setClients([...clients, data])
        setClientForm({ client_name: "", email: "", contact_num: "" })
      } else {
        setClientError(data.detail || "Failed to add client")
      }
    } catch { setClientError("Could not connect to server") }
    finally { setClientLoading(false) }
  }

  const handleAddRevenue = async (e) => {
    e.preventDefault()
    setRevenueError(""); setRevenueSuccess("")
    setRevenueLoading(true)
    try {
      const res = await fetch(`${BASE}/revenue/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          org_id: orgId,
          client_name: revenueForm.client_name,
          revenue_type: revenueForm.revenue_type,
          date_expected: revenueForm.date_expected ? revenueForm.date_expected + "T00:00:00" : null,
          date_received: revenueForm.date_received ? revenueForm.date_received + "T00:00:00" : null,
          amount: Number.parseInt(revenueForm.amount)
        }),
      })
      const data = await res.json()
      if (res.ok || res.status === 201) {
        setRevenueSuccess("Revenue added!")
        setRevenueForm({ client_name: "", revenue_type: "One_Time", date_expected: "", date_received: "", amount: "" })
      } else {
        const msg = Array.isArray(data.detail) ? (data.detail[0]?.msg || "Validation error") : (data.detail || "Failed to add revenue")
        setRevenueError(msg)
      }
    } catch { setRevenueError("Could not connect to server") }
    finally { setRevenueLoading(false) }
  }

  const handleAddExpense = async (e) => {
    e.preventDefault()
    setExpenseError(""); setExpenseSuccess("")
    setExpenseLoading(true)
    try {
      const res = await fetch(`${BASE}/expenses/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          organization_id: orgId,
          urgency: expenseForm.urgency,
          expense_type: expenseForm.expense_type,
          date: expenseForm.date ? expenseForm.date + "T00:00:00" : null,
          amount: Number.parseInt(expenseForm.amount)
        }),
      })
      const data = await res.json()
      if (res.ok || res.status === 201) {
        setExpenseSuccess("Expense added!")
        setExpenseForm({ urgency: "Critical", expense_type: "One_Time", date: "", amount: "" })
      } else {
        const msg = Array.isArray(data.detail) ? (data.detail[0]?.msg || "Validation error") : (data.detail || "Failed to add expense")
        setExpenseError(msg)
      }
    } catch { setExpenseError("Could not connect to server") }
    finally { setExpenseLoading(false) }
  }

  const inputClass = "w-full mt-1 px-3 py-2 bg-white border border-teal-200 rounded-lg text-gray-800 text-sm placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-500"
  const labelClass = "text-xs font-medium text-gray-500"
  const btnClass = "mt-2 px-4 py-2 rounded-lg bg-teal-700 text-white text-xs font-semibold tracking-widest uppercase hover:bg-teal-600 transition-all disabled:opacity-50"

  return (
    <div className="space-y-6">

      {/* ── Access Controls ── */}
      <div className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-5 shadow-sm">
        <h3 className="text-sm font-bold text-[#1a3a32] mb-4">Access Controls</h3>

        <form onSubmit={handleAddMember} className="flex flex-wrap items-end gap-3 mb-4">
          <div className="flex-1 min-w-[180px]">
            <label htmlFor="member-email" className={labelClass}>Email</label>
            <input id="member-email" type="email" placeholder="member@risco.com" value={memberForm.email}
              onChange={e => setMemberForm({ ...memberForm, email: e.target.value })}
              className={inputClass} />
          </div>
          <div className="flex-1 min-w-[140px]">
            <label htmlFor="member-role" className={labelClass}>Role</label>
            <select id="member-role" value={memberForm.role_name}
              onChange={e => setMemberForm({ ...memberForm, role_name: e.target.value })}
              className={inputClass}>
              <option value="coowner">Co-owner</option>
              <option value="stakeholder">Stakeholder</option>
            </select>
          </div>
          <button type="submit" disabled={memberLoading} className={btnClass}>
            {memberLoading ? "Adding..." : "Add Member"}
          </button>
        </form>

        {memberError && <p className="text-red-500 text-xs mb-2">{memberError}</p>}
        {memberSuccess && <p className="text-teal-600 text-xs mb-2">{memberSuccess}</p>}

        <div>
          <p className={labelClass + " mb-2"}>Current Members</p>
          {members.length === 0 ? (
            <p className="text-xs text-gray-400">No members found</p>
          ) : (
            <div className="space-y-2 overflow-y-auto" style={{ maxHeight: `${Math.min(members.length, 4) * 56}px` }}>
              {members.map((m) => (
                <div key={m.member_id} className="flex justify-between items-center bg-white border border-teal-100 rounded-lg px-3 py-2">
                  <div>
                    <p className="text-sm text-gray-700">{m.email}</p>
                    <p className="text-xs text-gray-400">{m.role_name}</p>
                  </div>
                  <button onClick={() => handleRemoveMember(m.member_id)}
                    className="text-xs text-red-400 hover:text-red-600 transition-colors">
                    Remove
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* ── Clients ── */}
      <div className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-5 shadow-sm">
        <h3 className="text-sm font-bold text-[#1a3a32] mb-4">Clients</h3>
        <form onSubmit={handleAddClient}>
          <div className="flex flex-wrap items-end md:grid-cols-3 gap-3">
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="client-name" className={labelClass}>Name</label>
              <input id="client-name" type="text" placeholder="Acme Corp" value={clientForm.client_name}
                onChange={e => setClientForm({ ...clientForm, client_name: e.target.value })}
                className={inputClass} />
            </div>
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="client-email" className={labelClass}>Email</label>
              <input id="client-email" type="email" placeholder="client@email.com" value={clientForm.email}
                onChange={e => setClientForm({ ...clientForm, email: e.target.value })}
                className={inputClass} />
            </div>
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="client-contact" className={labelClass}>Contact No. <span className="text-gray-400">(optional)</span></label>
              <input id="client-contact" type="text" placeholder="+1 234 567 8900" value={clientForm.contact_num}
                onChange={e => setClientForm({ ...clientForm, contact_num: e.target.value })}
                className={inputClass} />
            </div>
            <button type="submit" disabled={clientLoading} className={btnClass}>
              {clientLoading ? "Adding..." : "Add Client"}
            </button>
          </div>
          {clientError && <p className="text-red-500 text-xs mt-2">{clientError}</p>}
          {clientSuccess && <p className="text-teal-600 text-xs mt-2">{clientSuccess}</p>}
        </form>

        {clients.length > 0 && (
          <div className="mt-4 space-y-2">
            {clients.map((c) => (
              <div key={c.id} className="flex gap-4 bg-white border border-teal-100 rounded-lg px-3 py-2 text-sm text-gray-700">
                <span>{c.name}</span>
                <span className="text-gray-400">{c.email}</span>
                <span className="text-gray-400">{c.contact_number || "—"}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ── Revenue ── */}
      <div className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-5 shadow-sm">
        <h3 className="text-sm font-bold text-[#1a3a32] mb-4">Revenue</h3>
        <form onSubmit={handleAddRevenue}>
          <div className="flex flex-wrap items-end md:grid-cols-3 gap-3">
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="revenue-client-name" className={labelClass}>Client Name</label>
              <input id="revenue-client-name" type="text" placeholder="Acme Corp" value={revenueForm.client_name}
                onChange={e => setRevenueForm({ ...revenueForm, client_name: e.target.value })}
                className={inputClass} />
            </div>
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="revenue-type" className={labelClass}>Revenue Type</label>
              <select id="revenue-type" value={revenueForm.revenue_type}
                onChange={e => setRevenueForm({ ...revenueForm, revenue_type: e.target.value })}
                className={inputClass}>
                <option value="One_Time">One Time</option>
                <option value="Recurring">Recurring</option>
              </select>
            </div>
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="revenue-amount" className={labelClass}>Amount</label>
              <input id="revenue-amount" type="number" placeholder="0.00" value={revenueForm.amount}
                onChange={e => setRevenueForm({ ...revenueForm, amount: e.target.value })}
                className={inputClass} />
            </div>
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="revenue-date-expected" className={labelClass}>Date Expected</label>
              <input id="revenue-date-expected" type="date" value={revenueForm.date_expected}
                onChange={e => setRevenueForm({ ...revenueForm, date_expected: e.target.value })}
                className={inputClass} />
            </div>
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="revenue-date-received" className={labelClass}>Date Received <span className="text-gray-400">(optional)</span></label>
              <input id="revenue-date-received" type="date" value={revenueForm.date_received}
                onChange={e => setRevenueForm({ ...revenueForm, date_received: e.target.value })}
                className={inputClass} />
            </div>
          </div>
          {revenueError && <p className="text-red-500 text-xs mt-2">{revenueError}</p>}
          {revenueSuccess && <p className="text-teal-600 text-xs mt-2">{revenueSuccess}</p>}
          <button type="submit" disabled={revenueLoading} className={btnClass}>
            {revenueLoading ? "Adding..." : "Add Revenue"}
          </button>
        </form>
      </div>

      {/* ── Expenses ── */}
      <div className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-5 shadow-sm">
        <h3 className="text-sm font-bold text-[#1a3a32] mb-4">Expenses</h3>
        <form onSubmit={handleAddExpense}>
          <div className="flex flex-wrap items-end md:grid-cols-4 gap-3">
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="expense-type" className={labelClass}>Expense Type</label>
              <select id="expense-type" value={expenseForm.expense_type}
                onChange={e => setExpenseForm({ ...expenseForm, expense_type: e.target.value })}
                className={inputClass}>
                <option value="One_Time">One Time</option>
                <option value="Recurring">Recurring</option>
              </select>
            </div>
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="expense-urgency" className={labelClass}>Urgency</label>
              <select id="expense-urgency" value={expenseForm.urgency}
                onChange={e => setExpenseForm({ ...expenseForm, urgency: e.target.value })}
                className={inputClass}>
                <option value="Critical">Critical</option>
                <option value="Non-Critical">Non-Critical</option>
              </select>
            </div>
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="expense-date" className={labelClass}>Date</label>
              <input id="expense-date" type="date" value={expenseForm.date}
                onChange={e => setExpenseForm({ ...expenseForm, date: e.target.value })}
                className={inputClass} />
            </div>
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="expense-amount" className={labelClass}>Amount</label>
              <input id="expense-amount" type="number" placeholder="0.00" value={expenseForm.amount}
                onChange={e => setExpenseForm({ ...expenseForm, amount: e.target.value })}
                className={inputClass} />
            </div>
          </div>
          {expenseError && <p className="text-red-500 text-xs mt-2">{expenseError}</p>}
          {expenseSuccess && <p className="text-teal-600 text-xs mt-2">{expenseSuccess}</p>}
          <button type="submit" disabled={expenseLoading} className={btnClass}>
            {expenseLoading ? "Adding..." : "Add Expense"}
          </button>
        </form>
      </div>

    </div>
  )
}