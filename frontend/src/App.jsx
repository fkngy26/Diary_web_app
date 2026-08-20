import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import ActionList from "./pages/ActionList";
import ActionEditor from "./pages/ActionEditor";
import DiaryList from "./pages/DiaryList";
import Diary from "./pages/Diary";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/actions" element={<ActionList />} />
          <Route path="/actions/new" element={<ActionEditor />} />
          <Route path="/actions/:actionId" element={<ActionEditor />} />
          <Route path="/diaries" element={<DiaryList />} />
          <Route path="/diaries/:date" element={<Diary />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
