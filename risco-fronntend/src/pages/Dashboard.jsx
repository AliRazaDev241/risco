// import { useState } from "react";

// const metrics = [
//   { label: "Cash Balance", value: "$124,500" },
//   { label: "Monthly Burn Rate", value: "$18,200" },
//   { label: "Runway", value: "6.8 months" },
//   { label: "Headcount", value: "12" },
//   { label: "Cash Runway Proj.", value: "Aug 2026" },
// ];

// const navItems = [
//   { id: "overview", label: "Dashboard" },
//   { id: "expense", label: "Expense Intelligence" },
//   { id: "revenue", label: "Revenue Intelligence" },
//   { id: "operations", label: "Operations" },
// ];

// export default function Dashboard() {
//   const [active, setActive] = useState("overview");

//   return (
//     <div className="min-h-screen bg-[#0B1220] flex text-white">

//       {/* Sidebar */}
//       <aside className="w-64 min-h-screen bg-[#0F1A2E] border-r border-white/10 flex flex-col justify-between px-5 py-8 fixed">
        
//         {/* Top */}
//         <div>
//           <h1 className="text-xl font-semibold tracking-widest uppercase text-white mb-8">RISCO</h1>

//           {/* Always visible metrics */}
//           <div className="mb-8 space-y-3">
//             {metrics.map((m) => (
//               <div key={m.label} className="bg-white/5 rounded-lg px-3 py-2">
//                 <p className="text-xs text-gray-500 uppercase tracking-wider">{m.label}</p>
//                 <p className="text-sm font-medium text-white mt-0.5">{m.value}</p>
//               </div>
//             ))}
//           </div>

//           {/* Nav */}
//           <nav className="space-y-1">
//             {navItems.map((item) => (
//               <button
//                 key={item.id}
//                 onClick={() => setActive(item.id)}
//                 className={`w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all duration-200 ${
//                   active === item.id
//                     ? "bg-blue-600/20 text-blue-300 border border-blue-500/30"
//                     : "text-gray-400 hover:text-white hover:bg-white/5"
//                 }`}
//               >
//                 {item.label}
//               </button>
//             ))}
//           </nav>
//         </div>

//         {/* Logout */}
//         <button className="w-full text-left px-3 py-2.5 rounded-lg text-sm text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-all duration-200">
//           Logout
//         </button>
//       </aside>

//       {/* Main content */}
//       <main className="ml-64 flex-1 p-8">

//         {active === "overview" && (
//           <div>
//             <h2 className="text-2xl font-semibold mb-1">Dashboard Overview</h2>
//             <p className="text-gray-400 text-sm mb-8">Welcome back. Here's your financial snapshot.</p>

//             <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
//               {/* Expense card */}
//               <button
//                 onClick={() => setActive("expense")}
//                 className="bg-[#0F1A2E] border border-white/10 rounded-2xl p-6 text-left hover:border-blue-500/40 hover:shadow-[0_0_20px_rgba(99,102,241,0.15)] transition-all duration-300"
//               >
//                 <div className="text-2xl mb-3">📉</div>
//                 <h3 className="text-base font-medium text-white mb-1">Expense Intelligence</h3>
//                 <p className="text-xs text-gray-400">Burn rate · Ops cost · Risk alerts</p>
//               </button>

//               {/* Revenue card */}
//               <button
//                 onClick={() => setActive("revenue")}
//                 className="bg-[#0F1A2E] border border-white/10 rounded-2xl p-6 text-left hover:border-blue-500/40 hover:shadow-[0_0_20px_rgba(99,102,241,0.15)] transition-all duration-300"
//               >
//                 <div className="text-2xl mb-3">📈</div>
//                 <h3 className="text-base font-medium text-white mb-1">Revenue Intelligence</h3>
//                 <p className="text-xs text-gray-400">MRR · Client dependency · Heatmap</p>
//               </button>

//               {/* Operations card */}
//               <button
//                 onClick={() => setActive("operations")}
//                 className="bg-[#0F1A2E] border border-white/10 rounded-2xl p-6 text-left hover:border-blue-500/40 hover:shadow-[0_0_20px_rgba(99,102,241,0.15)] transition-all duration-300"
//               >
//                 <div className="text-2xl mb-3">⚙️</div>
//                 <h3 className="text-base font-medium text-white mb-1">Operations</h3>
//                 <p className="text-xs text-gray-400">Team · Clients · Entries</p>
//               </button>
//             </div>

//             {/* Risk alerts banner */}
//             <div className="mt-6 bg-red-500/10 border border-red-500/20 rounded-xl px-5 py-4">
//               <p className="text-xs text-red-400 uppercase tracking-wider mb-1">⚠ Major Risk Alert</p>
//               <p className="text-sm text-red-300">Runway below 7 months — review burn rate immediately.</p>
//             </div>
//           </div>
//         )}

//         {active === "expense" && (
//           <div>
//             <h2 className="text-2xl font-semibold mb-1">Expense Intelligence</h2>
//             <p className="text-gray-400 text-sm mb-8">Monitor and manage your spending.</p>
//             <div className="bg-[#0F1A2E] border border-white/10 rounded-2xl p-6 text-gray-400 text-sm">
//               Coming soon — expense charts and entries will go here.
//             </div>
//           </div>
//         )}

//         {active === "revenue" && (
//           <div>
//             <h2 className="text-2xl font-semibold mb-1">Revenue Intelligence</h2>
//             <p className="text-gray-400 text-sm mb-8">Track MRR, clients and revenue health.</p>
//             <div className="bg-[#0F1A2E] border border-white/10 rounded-2xl p-6 text-gray-400 text-sm">
//               Coming soon — revenue charts and entries will go here.
//             </div>
//           </div>
//         )}

//         {active === "operations" && (
//           <div>
//             <h2 className="text-2xl font-semibold mb-1">Operations</h2>
//             <p className="text-gray-400 text-sm mb-8">Manage your team, clients and entries.</p>
//             <div className="bg-[#0F1A2E] border border-white/10 rounded-2xl p-6 text-gray-400 text-sm">
//               Coming soon — operations panels will go here.
//             </div>
//           </div>
//         )}

//       </main>
//     </div>
//   );
// }

// import { useState } from "react";

// const navItems = [
//   { id: "overview", label: "Dashboard" },
//   { id: "expense", label: "Expense Intelligence" },
//   { id: "revenue", label: "Revenue Intelligence" },
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
//     <div className="min-h-screen bg-[#0B1220] flex text-white">

//       {/* Sidebar */}
//       <aside className="w-56 min-h-screen bg-[#0F1A2E] border-r border-white/10 flex flex-col justify-between px-4 py-8 fixed">
//         <div>
//           <h1 className="text-lg font-semibold tracking-widest uppercase text-white mb-8">RISCO</h1>
//           <nav className="space-y-1">
//             {navItems.map((item) => (
//               <button
//                 key={item.id}
//                 onClick={() => setActive(item.id)}
//                 className={`w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all duration-200 ${
//                   active === item.id
//                     ? "bg-blue-600/20 text-blue-300 border border-blue-500/30"
//                     : "text-gray-400 hover:text-white hover:bg-white/5"
//                 }`}
//               >
//                 {item.label}
//               </button>
//             ))}
//           </nav>
//         </div>
//         <button className="w-full text-left px-3 py-2.5 rounded-lg text-sm text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-all duration-200">
//           Logout
//         </button>
//       </aside>

//       {/* Main content */}
//       <main className="ml-56 flex-1 p-8">

//         {active === "overview" && (
//           <div>
//             <h2 className="text-2xl font-semibold mb-1">Dashboard Overview</h2>
//             <p className="text-gray-400 text-sm mb-8">Welcome back. Here's your financial snapshot.</p>

//             {/* Metrics row */}
//             <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-8">
//               {metrics.map((m) => (
//                 <div key={m.label} className="bg-[#0F1A2E] border border-white/10 rounded-xl px-4 py-3">
//                   <p className="text-xs text-gray-500 uppercase tracking-wider">{m.label}</p>
//                   <p className="text-base font-medium text-white mt-1">{m.value}</p>
//                 </div>
//               ))}
//             </div>

//             {/* Section cards */}
//             <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
//               <button
//                 onClick={() => setActive("expense")}
//                 className="bg-[#0F1A2E] border border-white/10 rounded-2xl p-6 text-left hover:border-blue-500/40 hover:shadow-[0_0_20px_rgba(99,102,241,0.15)] transition-all duration-300"
//               >
//                 <div className="text-2xl mb-3">📉</div>
//                 <h3 className="text-base font-medium text-white mb-1">Expense Intelligence</h3>
//                 <p className="text-xs text-gray-400">Burn rate · Ops cost · Risk alerts</p>
//               </button>

//               <button
//                 onClick={() => setActive("revenue")}
//                 className="bg-[#0F1A2E] border border-white/10 rounded-2xl p-6 text-left hover:border-blue-500/40 hover:shadow-[0_0_20px_rgba(99,102,241,0.15)] transition-all duration-300"
//               >
//                 <div className="text-2xl mb-3">📈</div>
//                 <h3 className="text-base font-medium text-white mb-1">Revenue Intelligence</h3>
//                 <p className="text-xs text-gray-400">MRR · Client dependency · Heatmap</p>
//               </button>

//               <button
//                 onClick={() => setActive("operations")}
//                 className="bg-[#0F1A2E] border border-white/10 rounded-2xl p-6 text-left hover:border-blue-500/40 hover:shadow-[0_0_20px_rgba(99,102,241,0.15)] transition-all duration-300"
//               >
//                 <div className="text-2xl mb-3">⚙️</div>
//                 <h3 className="text-base font-medium text-white mb-1">Operations</h3>
//                 <p className="text-xs text-gray-400">Team · Clients · Entries</p>
//               </button>
//             </div>

//             {/* Risk alert */}
//             <div className="bg-red-500/10 border border-red-500/20 rounded-xl px-5 py-4">
//               <p className="text-xs text-red-400 uppercase tracking-wider mb-1">⚠ Major Risk Alert</p>
//               <p className="text-sm text-red-300">Runway below 7 months — review burn rate immediately.</p>
//             </div>
//           </div>
//         )}

//         {active === "expense" && (
//           <div>
//             <h2 className="text-2xl font-semibold mb-1">Expense Intelligence</h2>
//             <p className="text-gray-400 text-sm mb-8">Monitor and manage your spending.</p>
//             <div className="bg-[#0F1A2E] border border-white/10 rounded-2xl p-6 text-gray-400 text-sm">
//               Coming soon — expense charts and entries will go here.
//             </div>
//           </div>
//         )}

//         {active === "revenue" && (
//           <div>
//             <h2 className="text-2xl font-semibold mb-1">Revenue Intelligence</h2>
//             <p className="text-gray-400 text-sm mb-8">Track MRR, clients and revenue health.</p>
//             <div className="bg-[#0F1A2E] border border-white/10 rounded-2xl p-6 text-gray-400 text-sm">
//               Coming soon — revenue charts and entries will go here.
//             </div>
//           </div>
//         )}

//         {active === "operations" && (
//           <div>
//             <h2 className="text-2xl font-semibold mb-1">Operations</h2>
//             <p className="text-gray-400 text-sm mb-8">Manage your team, clients and entries.</p>
//             <div className="bg-[#0F1A2E] border border-white/10 rounded-2xl p-6 text-gray-400 text-sm">
//               Coming soon — operations panels will go here.
//             </div>
//           </div>
//         )}

//       </main>
//     </div>
//   );
// }

import { useState } from "react";

const navItems = [
  { id: "overview", label: "Dashboard" },
  { id: "expense", label: "Expense Intelligence" },
  { id: "revenue", label: "Revenue Intelligence" },
  { id: "operations", label: "Operations" },
];

const metrics = [
  { label: "Cash Balance", value: "$124,500" },
  { label: "Monthly Burn Rate", value: "$18,200" },
  { label: "Runway", value: "6.8 months" },
  { label: "Headcount", value: "12" },
  { label: "Cash Runway Proj.", value: "Aug 2026" },
];

export default function Dashboard() {
  const [active, setActive] = useState("overview");

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

        {active === "overview" && (
          <div>
            <h2 className="text-2xl font-bold text-[#1a3a32] mb-1">Dashboard Overview</h2>
            <p className="text-gray-400 text-sm mb-8">Welcome back. Here's your financial snapshot.</p>

            {/* Metrics row */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-8">
              {metrics.map((m) => (
                <div key={m.label} className="bg-white/70 backdrop-blur border border-teal-100 rounded-xl px-4 py-3 shadow-sm">
                  <p className="text-xs text-gray-400 uppercase tracking-wider">{m.label}</p>
                  <p className="text-base font-semibold text-[#1a3a32] mt-1">{m.value}</p>
                </div>
              ))}
            </div>

            {/* Section cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <button
                onClick={() => setActive("expense")}
                className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-6 text-left hover:border-teal-400 hover:shadow-md transition-all duration-300"
              >
                <div className="text-2xl mb-3">📉</div>
                <h3 className="text-base font-semibold text-[#1a3a32] mb-1">Expense Intelligence</h3>
                <p className="text-xs text-gray-400">Burn rate · Ops cost · Risk alerts</p>
              </button>

              <button
                onClick={() => setActive("revenue")}
                className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-6 text-left hover:border-teal-400 hover:shadow-md transition-all duration-300"
              >
                <div className="text-2xl mb-3">📈</div>
                <h3 className="text-base font-semibold text-[#1a3a32] mb-1">Revenue Intelligence</h3>
                <p className="text-xs text-gray-400">MRR · Client dependency · Heatmap</p>
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

            {/* Risk alert */}
            <div className="bg-red-50 border border-red-200 rounded-xl px-5 py-4">
              <p className="text-xs text-red-500 uppercase tracking-wider mb-1">⚠ Major Risk Alert</p>
              <p className="text-sm text-red-400">Runway below 7 months — review burn rate immediately.</p>
            </div>
          </div>
        )}

        {active === "expense" && (
          <div>
            <h2 className="text-2xl font-bold text-[#1a3a32] mb-1">Expense Intelligence</h2>
            <p className="text-gray-400 text-sm mb-8">Monitor and manage your spending.</p>
            <div className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-6 text-gray-400 text-sm shadow-sm">
              Coming soon — expense charts and entries will go here.
            </div>
          </div>
        )}

        {active === "revenue" && (
          <div>
            <h2 className="text-2xl font-bold text-[#1a3a32] mb-1">Revenue Intelligence</h2>
            <p className="text-gray-400 text-sm mb-8">Track MRR, clients and revenue health.</p>
            <div className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-6 text-gray-400 text-sm shadow-sm">
              Coming soon — revenue charts and entries will go here.
            </div>
          </div>
        )}

        {active === "operations" && (
          <div>
            <h2 className="text-2xl font-bold text-[#1a3a32] mb-1">Operations</h2>
            <p className="text-gray-400 text-sm mb-8">Manage your team, clients and entries.</p>
            <div className="bg-white/70 backdrop-blur border border-teal-100 rounded-2xl p-6 text-gray-400 text-sm shadow-sm">
              Coming soon — operations panels will go here.
            </div>
          </div>
        )}

      </main>
    </div>
  );
}