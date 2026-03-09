import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import EmailDialog from "@/components/EmailDialog";
import { ArrowLeft, Globe, Linkedin, Twitter, ExternalLink, Save, Pencil } from "lucide-react";
import { toast } from "sonner";
import axios from "axios";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;
const COLORS = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#06B6D4"];

export default function InvestorProfile() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [investor, setInvestor] = useState(null);
  const [editing, setEditing] = useState(false);
  const [editData, setEditData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API}/investors/${id}`)
      .then(r => { setInvestor(r.data); setEditData(r.data); setLoading(false); })
      .catch(() => { toast.error("Investor not found"); navigate("/investors"); });
  }, [id, navigate]);

  const handleSave = async () => {
    try {
      const r = await axios.put(`${API}/investors/${id}`, {
        priority_tag: editData.priority_tag,
        notes: editData.notes,
        contacted: editData.contacted,
        contact_status: editData.contact_status,
        last_contact_date: editData.last_contact_date,
      });
      setInvestor(r.data);
      setEditing(false);
      toast.success("Investor updated");
    } catch {
      toast.error("Update failed");
    }
  };

  if (loading) return <div className="animate-fade-in"><div className="h-96 bg-zinc-900 animate-pulse rounded-sm" /></div>;
  if (!investor) return null;

  const patterns = Object.entries(investor.investment_patterns || {}).map(([k, v]) => ({ name: k, value: v }));

  return (
    <div className="animate-fade-in max-w-[1400px]" data-testid="investor-profile">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <Button
          data-testid="back-to-investors-btn"
          variant="ghost"
          onClick={() => navigate("/investors")}
          className="text-zinc-400 hover:text-white p-2"
        >
          <ArrowLeft size={18} />
        </Button>
        <div className="flex-1">
          <h1 className="font-heading text-3xl sm:text-4xl font-black tracking-tight text-white uppercase">
            {investor.name}
          </h1>
          <p className="text-sm text-zinc-400 font-mono">{investor.title} at {investor.institution}</p>
        </div>
        <EmailDialog investor={investor} />
        <Button
          data-testid="edit-investor-btn"
          onClick={() => setEditing(!editing)}
          className="bg-zinc-900 border border-zinc-800 hover:bg-zinc-800 text-zinc-300 text-xs rounded-sm"
        >
          <Pencil size={14} className="mr-1" /> {editing ? "Cancel" : "Edit"}
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Main Info */}
        <div className="lg:col-span-2 space-y-4">
          {/* Key Details */}
          <div className="bg-[#0A0A0A] border border-zinc-800 p-6 rounded-sm">
            <h3 className="font-heading text-lg font-bold text-white mb-4">Key Details</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div>
                <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Type</p>
                <Badge variant="outline" className="border-zinc-700 text-zinc-300 mt-1 rounded-sm">{investor.investor_type}</Badge>
              </div>
              <div>
                <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Cheque Size</p>
                <p className="text-sm font-mono text-white mt-1">
                  ${(investor.cheque_size_min || 0).toLocaleString()} - ${(investor.cheque_size_max || 0).toLocaleString()}
                </p>
              </div>
              <div>
                <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Currency</p>
                <p className="text-sm font-mono text-white mt-1">{investor.cheque_size_currency}</p>
              </div>
              <div>
                <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Shareholding</p>
                <p className="text-sm font-mono text-white mt-1">{investor.typical_shareholding || "N/A"}</p>
              </div>
              <div>
                <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Invests in India</p>
                <p className={`text-sm font-mono mt-1 ${investor.invests_in_india ? "text-emerald-400" : "text-zinc-500"}`}>
                  {investor.invests_in_india ? "YES" : "NO"}
                </p>
              </div>
              <div>
                <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Last Verified</p>
                <p className="text-sm font-mono text-white mt-1">{investor.last_verified_date || "N/A"}</p>
              </div>
            </div>
          </div>

          {/* Sectors & Stages */}
          <div className="bg-[#0A0A0A] border border-zinc-800 p-6 rounded-sm">
            <h3 className="font-heading text-lg font-bold text-white mb-4">Investment Focus</h3>
            <div className="space-y-4">
              <div>
                <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider mb-2">Primary Sectors</p>
                <div className="flex flex-wrap gap-2">
                  {(investor.primary_sectors || []).map(s => (
                    <Badge key={s} variant="outline" className="bg-blue-500/10 text-blue-400 border-blue-500/30 text-xs font-mono rounded-sm">{s}</Badge>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider mb-2">Secondary Sectors</p>
                <div className="flex flex-wrap gap-2">
                  {(investor.secondary_sectors || []).map(s => (
                    <Badge key={s} variant="outline" className="border-zinc-700 text-zinc-400 text-xs font-mono rounded-sm">{s}</Badge>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider mb-2">Stages</p>
                <div className="flex flex-wrap gap-2">
                  {(investor.stage || []).map(s => (
                    <Badge key={s} variant="outline" className="bg-emerald-500/10 text-emerald-400 border-emerald-500/30 text-xs font-mono rounded-sm">{s}</Badge>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider mb-2">Geographies</p>
                <div className="flex flex-wrap gap-2">
                  {(investor.geographies || []).map(g => (
                    <Badge key={g} variant="outline" className="border-zinc-700 text-zinc-400 text-xs font-mono rounded-sm">{g}</Badge>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Recent Deals */}
          <div className="bg-[#0A0A0A] border border-zinc-800 p-6 rounded-sm">
            <h3 className="font-heading text-lg font-bold text-white mb-4">Recent Deals / Portfolio</h3>
            <div className="space-y-3">
              {(investor.recent_deals || []).map((d, i) => (
                <div key={i} className="flex items-center justify-between bg-black/50 p-3 rounded-sm border border-zinc-900">
                  <div>
                    <p className="text-sm font-mono text-white">{d.company}</p>
                    <p className="text-[10px] font-mono text-zinc-500">{d.sector}</p>
                  </div>
                  {d.link && (
                    <a href={d.link} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">
                      <ExternalLink size={14} />
                    </a>
                  )}
                </div>
              ))}
              {(!investor.recent_deals || investor.recent_deals.length === 0) && (
                <p className="text-xs font-mono text-zinc-600">No recent deals recorded</p>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          {/* Contact Info */}
          <div className="bg-[#0A0A0A] border border-zinc-800 p-6 rounded-sm">
            <h3 className="font-heading text-lg font-bold text-white mb-4">Contact</h3>
            <div className="space-y-3">
              {investor.email && (
                <div>
                  <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Email</p>
                  <a href={`mailto:${investor.email}`} className="text-sm font-mono text-blue-400 hover:text-blue-300 break-all">{investor.email}</a>
                </div>
              )}
              <div className="flex gap-2 mt-3">
                {investor.website && (
                  <a href={investor.website} target="_blank" rel="noopener noreferrer" data-testid="website-link"
                    className="bg-zinc-900 border border-zinc-800 p-2 rounded-sm hover:bg-zinc-800 text-zinc-400 hover:text-white">
                    <Globe size={16} />
                  </a>
                )}
                {investor.linkedin_url && (
                  <a href={investor.linkedin_url} target="_blank" rel="noopener noreferrer" data-testid="linkedin-link"
                    className="bg-zinc-900 border border-zinc-800 p-2 rounded-sm hover:bg-zinc-800 text-zinc-400 hover:text-white">
                    <Linkedin size={16} />
                  </a>
                )}
                {investor.twitter_handle && (
                  <a href={`https://twitter.com/${investor.twitter_handle.replace("@", "")}`} target="_blank" rel="noopener noreferrer" data-testid="twitter-link"
                    className="bg-zinc-900 border border-zinc-800 p-2 rounded-sm hover:bg-zinc-800 text-zinc-400 hover:text-white">
                    <Twitter size={16} />
                  </a>
                )}
              </div>
            </div>
          </div>

          {/* Investment Patterns */}
          {patterns.length > 0 && (
            <div className="bg-[#0A0A0A] border border-zinc-800 p-6 rounded-sm">
              <h3 className="font-heading text-lg font-bold text-white mb-4">Investment Patterns</h3>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={patterns} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={75} strokeWidth={1} stroke="#0A0A0A">
                    {patterns.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                  </Pie>
                  <Tooltip contentStyle={{ background: '#111', border: '1px solid #27272A', borderRadius: 2, fontFamily: 'JetBrains Mono', fontSize: 11 }} />
                </PieChart>
              </ResponsiveContainer>
              <div className="space-y-1 mt-2">
                {patterns.map((p, i) => (
                  <div key={p.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-sm" style={{ background: COLORS[i % COLORS.length] }} />
                      <span className="text-[10px] font-mono text-zinc-400">{p.name}</span>
                    </div>
                    <span className="text-[10px] font-mono text-zinc-300">{p.value}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* CRM / Edit Panel */}
          <div className="bg-[#0A0A0A] border border-zinc-800 p-6 rounded-sm">
            <h3 className="font-heading text-lg font-bold text-white mb-4">CRM Status</h3>
            {editing ? (
              <div className="space-y-3">
                <div>
                  <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Priority</label>
                  <Select value={editData.priority_tag} onValueChange={(v) => setEditData({...editData, priority_tag: v})}>
                    <SelectTrigger className="bg-black border-zinc-800 rounded-sm text-xs font-mono mt-1"><SelectValue /></SelectTrigger>
                    <SelectContent className="bg-[#0A0A0A] border-zinc-800">
                      {["High", "Medium", "Low"].map(p => <SelectItem key={p} value={p}>{p}</SelectItem>)}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Contact Status</label>
                  <Select value={editData.contact_status} onValueChange={(v) => setEditData({...editData, contact_status: v, contacted: v !== "Not contacted"})}>
                    <SelectTrigger className="bg-black border-zinc-800 rounded-sm text-xs font-mono mt-1"><SelectValue /></SelectTrigger>
                    <SelectContent className="bg-[#0A0A0A] border-zinc-800">
                      {["Not contacted", "Emailed", "Meeting booked"].map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Notes</label>
                  <Textarea
                    value={editData.notes || ""}
                    onChange={(e) => setEditData({...editData, notes: e.target.value})}
                    className="bg-black border-zinc-800 rounded-sm text-xs font-mono mt-1 min-h-[80px]"
                    placeholder="Add notes about this investor..."
                  />
                </div>
                <Button
                  data-testid="save-investor-btn"
                  onClick={handleSave}
                  className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-sm uppercase tracking-wider text-xs"
                >
                  <Save size={14} className="mr-1" /> Save Changes
                </Button>
              </div>
            ) : (
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-[10px] font-mono text-zinc-500">Priority</span>
                  <Badge variant="outline" className={`${investor.priority_tag === "High" ? "badge-high" : investor.priority_tag === "Medium" ? "badge-medium" : "badge-low"} text-[10px] font-mono rounded-sm`}>
                    {investor.priority_tag}
                  </Badge>
                </div>
                <div className="flex justify-between">
                  <span className="text-[10px] font-mono text-zinc-500">Status</span>
                  <span className={`text-xs font-mono ${investor.contacted ? "text-emerald-400" : "text-zinc-500"}`}>{investor.contact_status}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[10px] font-mono text-zinc-500">Last Contact</span>
                  <span className="text-xs font-mono text-zinc-400">{investor.last_contact_date || "Never"}</span>
                </div>
                {investor.notes && (
                  <div className="mt-2 pt-2 border-t border-zinc-800">
                    <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider mb-1">Notes</p>
                    <p className="text-xs text-zinc-400">{investor.notes}</p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Source */}
          <div className="bg-[#0A0A0A] border border-zinc-800 p-4 rounded-sm">
            <p className="text-[10px] font-mono text-zinc-600 uppercase tracking-wider">Source: {investor.source || "N/A"}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
