import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "./pages/login"
import Register from "./pages/Register"
import OrgSelect from "./pages/OrgSelect"
import Dashboard from "./pages/Dashboard"
import Operations from "./pages/Operations"
import FinancialIntelligence from "./pages/FinancialIntelligence"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/orgselect" element={<OrgSelect />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/operations" element={<Operations />} />
        <Route path="/financial-intelligence" element={<FinancialIntelligence />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App