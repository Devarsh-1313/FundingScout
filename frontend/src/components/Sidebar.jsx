import { NavLink } from "react-router-dom";
import { Database, LayoutDashboard, Sparkles, Newspaper, Calendar, Landmark, Rocket, Users, Clock, X } from "lucide-react";

const navItems = [
  { path: "/", label: "Dashboard", icon: LayoutDashboard },
  { path: "/investors", label: "Investor Database", icon: Database },
  { path: "/new-updated", label: "New & Updated", icon: Clock },
  { path: "/idea-match", label: "Idea Match", icon: Sparkles },
  { path: "/news", label: "News Aggregator", icon: Newspaper },
  { path: "/events", label: "Events Tracker", icon: Calendar },
  { path: "/govt-schemes", label: "Govt Schemes", icon: Landmark },
  { path: "/accelerators", label: "Accelerators", icon: Rocket },
  { path: "/startups", label: "Startup Portal", icon: Users },
];

export default function Sidebar({ open, onClose }) {
  return (
    <>
      {/* Overlay for mobile */}
      {open && (
        <div className="fixed inset-0 bg-black/60 z-30 lg:hidden" onClick={onClose} />
      )}
      <aside className={`sidebar ${open ? "open" : ""}`} data-testid="sidebar">
        {/* Logo */}
        <div className="p-6 border-b border-zinc-800">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="font-heading text-xl font-bold tracking-tight text-white uppercase">
                Capital Compass
              </h1>
              <p className="text-[10px] font-mono text-zinc-500 tracking-widest uppercase mt-1">
                Investor Intelligence
              </p>
            </div>
            <button className="lg:hidden text-zinc-400 hover:text-white" onClick={onClose}>
              <X size={18} />
            </button>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4 px-3">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              data-testid={`nav-${item.path.replace("/", "") || "dashboard"}`}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 mb-1 rounded-sm text-xs font-medium tracking-wide transition-all duration-200 ${
                  isActive
                    ? "bg-blue-600/15 text-blue-400 border-l-2 border-blue-500"
                    : "text-zinc-400 hover:text-white hover:bg-zinc-900"
                }`
              }
              end={item.path === "/"}
            >
              <item.icon size={16} />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-zinc-800">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-[10px] font-mono text-zinc-500 tracking-wider uppercase">
              Auto-updating daily
            </span>
          </div>
        </div>
      </aside>
    </>
  );
}
