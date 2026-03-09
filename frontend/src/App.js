import { BrowserRouter, Routes, Route } from "react-router-dom";
import "@/App.css";
import { Toaster } from "@/components/ui/sonner";
import Sidebar from "@/components/Sidebar";
import Dashboard from "@/pages/Dashboard";
import InvestorDatabase from "@/pages/InvestorDatabase";
import InvestorProfile from "@/pages/InvestorProfile";
import NewUpdated from "@/pages/NewUpdated";
import IdeaMatch from "@/pages/IdeaMatch";
import NewsAggregator from "@/pages/NewsAggregator";
import EventsTracker from "@/pages/EventsTracker";
import GovtSchemes from "@/pages/GovtSchemes";
import Accelerators from "@/pages/Accelerators";
import StartupRegistration from "@/pages/StartupRegistration";
import { useState } from "react";

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <BrowserRouter>
      <div className="app-layout">
        <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        <main className="main-content">
          {/* Mobile menu toggle */}
          <button
            data-testid="mobile-menu-btn"
            className="lg:hidden fixed top-4 left-4 z-50 bg-zinc-900 border border-zinc-800 p-2 rounded-sm"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
              <path d="M3 12h18M3 6h18M3 18h18" />
            </svg>
          </button>
          <div className="p-6 md:p-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/investors" element={<InvestorDatabase />} />
              <Route path="/investors/:id" element={<InvestorProfile />} />
              <Route path="/new-updated" element={<NewUpdated />} />
              <Route path="/idea-match" element={<IdeaMatch />} />
              <Route path="/news" element={<NewsAggregator />} />
              <Route path="/events" element={<EventsTracker />} />
              <Route path="/govt-schemes" element={<GovtSchemes />} />
              <Route path="/accelerators" element={<Accelerators />} />
              <Route path="/startups" element={<StartupRegistration />} />
            </Routes>
          </div>
        </main>
        <Toaster position="bottom-right" theme="dark" />
      </div>
    </BrowserRouter>
  );
}

export default App;
