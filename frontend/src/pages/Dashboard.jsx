import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { Database, Users, TrendingUp, Clock, Newspaper, Calendar, Landmark, Rocket, ArrowRight } from "lucide-react";
import axios from "axios";

const API = "/api";
const CHART_COLORS = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#06B6D4", "#F97316"];

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`${API}/stats`)
  .then(r => {
    console.log("STATS API:", r.data); // DEBUG

    const data =
      Array.isArray(r.data) ? r.data[0] :
      r.data.stats ? r.data.stats :
      r.data;

    setStats(data || {});
    setLoading(false);
  })
  .catch((err) => {
    console.error("Stats error:", err);
    setLoading(false);
  });
  }, []);

  if (loading) return (
    <div className="animate-fade-in" data-testid="dashboard-loading">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[...Array(8)].map((_, i) => <div key={i} className="bg-[#0A0A0A] border border-zinc-800 h-28 animate-pulse rounded-sm" />)}
      </div>
    </div>
  );

  const statCards = [
    { label: "Total Investors", value: stats?.total_investors || 0, icon: Database, color: "text-blue-400", path: "/investors" },
    { label: "VCs", value: stats?.total_vc || 0, icon: TrendingUp, color: "text-emerald-400" },
    { label: "Angels", value: stats?.total_angel || 0, icon: Users, color: "text-yellow-400" },
    { label: "New (24h)", value: stats?.new_last_24h || 0, icon: Clock, color: "text-purple-400", path: "/new-updated" },
    { label: "News Articles", value: stats?.total_news || 0, icon: Newspaper, color: "text-cyan-400", path: "/news" },
    { label: "Events", value: stats?.total_events || 0, icon: Calendar, color: "text-pink-400", path: "/events" },
    { label: "Govt Schemes", value: stats?.total_schemes || 0, icon: Landmark, color: "text-orange-400", path: "/govt-schemes" },
    { label: "High Priority", value: stats?.high_priority || 0, icon: Rocket, color: "text-red-400" },
  ];

  return (
    <div className="animate-fade-in max-w-[1920px]" data-testid="dashboard">
      <div className="mb-8">
        <h1 className="font-heading text-4xl sm:text-5xl font-black tracking-tight uppercase text-white">
          Dashboard
        </h1>
        <p className="text-sm text-zinc-400 mt-2 font-medium">Real-time investor intelligence overview</p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {statCards.map((s) => (
          <div
            key={s.label}
            data-testid={`stat-${s.label.toLowerCase().replace(/[^a-z0-9]/g, "-")}`}
            className="bg-[#0A0A0A] border border-zinc-800 p-5 rounded-sm cursor-pointer hover:border-zinc-600 transition-colors group"
            onClick={() => s.path && navigate(s.path)}
          >
            <div className="flex items-center justify-between mb-3">
              <s.icon size={18} className={s.color} />
              {s.path && <ArrowRight size={14} className="text-zinc-700 group-hover:text-zinc-400 transition-colors" />}
            </div>
            <p className="text-2xl font-bold font-mono text-white">{s.value.toLocaleString()}</p>
            <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider mt-1">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-8">
        {/* Top Sectors */}
        <div className="bg-[#0A0A0A] border border-zinc-800 p-6 rounded-sm">
          <h3 className="font-heading text-lg font-bold text-white mb-4 tracking-tight">Top Investment Sectors</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={stats?.top_sectors?.slice(0, 8) || []} layout="vertical" margin={{ left: 80 }}>
              <XAxis type="number" stroke="#3F3F46" tick={{ fill: '#71717A', fontSize: 10, fontFamily: 'JetBrains Mono' }} />
              <YAxis type="category" dataKey="sector" stroke="#3F3F46" tick={{ fill: '#A1A1AA', fontSize: 10, fontFamily: 'JetBrains Mono' }} width={75} />
              <Tooltip contentStyle={{ background: '#111', border: '1px solid #27272A', borderRadius: 2, fontFamily: 'JetBrains Mono', fontSize: 11 }} />
              <Bar dataKey="count" fill="#3B82F6" radius={[0, 2, 2, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Type Distribution */}
        <div className="bg-[#0A0A0A] border border-zinc-800 p-6 rounded-sm">
          <h3 className="font-heading text-lg font-bold text-white mb-4 tracking-tight">Investor Type Distribution</h3>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={stats?.type_distribution || []}
                dataKey="count"
                nameKey="type"
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                strokeWidth={1}
                stroke="#0A0A0A"
              >
                {(stats?.type_distribution || []).map((_, i) => (
                  <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: '#111', border: '1px solid #27272A', borderRadius: 2, fontFamily: 'JetBrains Mono', fontSize: 11 }} />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex flex-wrap gap-3 mt-2 justify-center">
            {(stats?.type_distribution || []).map((t, i) => (
              <div key={t.type} className="flex items-center gap-1.5">
                <div className="w-2.5 h-2.5 rounded-sm" style={{ background: CHART_COLORS[i % CHART_COLORS.length] }} />
                <span className="text-[10px] font-mono text-zinc-400">{t.type} ({t.count})</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-[#0A0A0A] border border-zinc-800 p-5 rounded-sm">
          <h3 className="font-heading text-lg font-bold text-white mb-2">CRM Overview</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-xs font-mono text-zinc-500">Contacted</span>
              <span className="text-sm font-mono text-emerald-400">{stats?.contacted || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-xs font-mono text-zinc-500">Family Offices</span>
              <span className="text-sm font-mono text-yellow-400">{stats?.total_family_office || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-xs font-mono text-zinc-500">CVCs</span>
              <span className="text-sm font-mono text-purple-400">{stats?.total_cvc || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-xs font-mono text-zinc-500">Accelerators</span>
              <span className="text-sm font-mono text-cyan-400">{stats?.total_accelerator || 0}</span>
            </div>
          </div>
        </div>

        <div className="bg-[#0A0A0A] border border-zinc-800 p-5 rounded-sm">
          <h3 className="font-heading text-lg font-bold text-white mb-2">Startups Registered</h3>
          <p className="text-3xl font-mono font-bold text-blue-400">{stats?.total_startups || 0}</p>
          <p className="text-xs font-mono text-zinc-500 mt-2">Founders showcasing their products</p>
          <button
            data-testid="goto-startups-btn"
            onClick={() => navigate("/startups")}
            className="mt-4 text-xs font-mono text-blue-400 hover:text-blue-300 flex items-center gap-1"
          >
            View Portal <ArrowRight size={12} />
          </button>
        </div>

        <div className="bg-[#0A0A0A] border border-zinc-800 p-5 rounded-sm">
          <h3 className="font-heading text-lg font-bold text-white mb-2">System Status</h3>
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-emerald-500" />
              <span className="text-xs font-mono text-zinc-400">Database: Online</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-emerald-500" />
              <span className="text-xs font-mono text-zinc-400">Auto-update: Active</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-emerald-500" />
              <span className="text-xs font-mono text-zinc-400">News Feed: Live</span>
            </div>
            <p className="text-[10px] font-mono text-zinc-600 mt-2">
              Last updated: {stats?.last_updated ? new Date(stats.last_updated).toLocaleString() : "N/A"}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
