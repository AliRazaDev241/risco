// import Login from "./pages/login";

// function App() {
//   return <Login />;
// }

// export default App;

// // import Register from "./pages/Register";

// // function App() {
// //   return <Register />;
// // }

// // export default App;

// // import Dashboard from "./pages/Dashboard";

// // function App() {
// //   return <Dashboard />;
// // }

// // export default App;

// // import OrgSelect  from "./pages/OrgSelect";

// // function App() {
// //   return <OrgSelect />;
// // }

// // export default App;

import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "./pages/login"
import Register from "./pages/Register"
import OrgSelect from "./pages/OrgSelect"
import Dashboard from "./pages/Dashboard"
import Operations from "./pages/Operations"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/orgselect" element={<OrgSelect />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/operations" element={<Operations />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App