import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Users, Upload, Globe, ExternalLink, Plus } from "lucide-react";
import { toast } from "sonner";
import axios from "axios";

const API = "/api";
const STAGES = ["Pre-seed", "Seed", "Pre-Series A", "Series A", "Series B"];
const SECTORS = ["SaaS", "Fintech", "Consumer", "EdTech", "HealthTech", "AI/ML", "E-commerce", "DeepTech", "D2C Brands", "CleanTech", "Logistics", "FoodTech"];

export default function StartupRegistration() {
  const [startups, setStartups] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({
    founder_name: "", startup_name: "", description: "", website_url: "", app_url: "",
    stage: "Seed", sector: "SaaS", target_raise: "", video_url: "", screenshot_urls: [], file_ids: []
  });

  useEffect(() => {
    axios.get(`${API}/startups`).then(r => setStartups(r.data.startups)).catch(() => {});
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);
    try {
      const fd = new FormData();
      fd.append("file", file);
      const r = await axios.post(`${API}/upload`, fd, { headers: { "Content-Type": "multipart/form-data" } });
      setForm(prev => ({ ...prev, file_ids: [...prev.file_ids, r.data.id], screenshot_urls: [...prev.screenshot_urls, r.data.original_filename] }));
      toast.success(`Uploaded: ${file.name}`);
    } catch {
      toast.error("Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const handleSubmit = async () => {
    if (!form.founder_name || !form.startup_name || !form.description) {
      toast.error("Please fill in all required fields");
      return;
    }
    setSubmitting(true);
    try {
      const data = { ...form, target_raise: parseFloat(form.target_raise) || 0 };
      const r = await axios.post(`${API}/startups`, data);
      setStartups(prev => [r.data, ...prev]);
      setShowForm(false);
      setForm({ founder_name: "", startup_name: "", description: "", website_url: "", app_url: "", stage: "Seed", sector: "SaaS", target_raise: "", video_url: "", screenshot_urls: [], file_ids: [] });
      toast.success("Startup registered successfully!");
    } catch {
      toast.error("Registration failed");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="animate-fade-in max-w-[1400px]" data-testid="startup-registration-page">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-heading text-4xl sm:text-5xl font-black tracking-tight uppercase text-white">
            <Users className="inline mr-2 text-blue-400" size={36} />
            Startup Portal
          </h1>
          <p className="text-sm text-zinc-400 mt-2">Register your product, upload demos, and connect with investors</p>
        </div>
        <Button
          data-testid="register-startup-btn"
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-sm uppercase tracking-wider text-xs px-4"
        >
          <Plus size={14} className="mr-1" /> {showForm ? "Cancel" : "Register Startup"}
        </Button>
      </div>

      {/* Registration Form */}
      {showForm && (
        <div className="bg-[#0A0A0A] border border-zinc-800 p-6 rounded-sm mb-6 animate-fade-in" data-testid="startup-form">
          <h3 className="font-heading text-xl font-bold text-white mb-4">Register Your Product</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Founder Name *</label>
              <Input data-testid="founder-name-input" value={form.founder_name} onChange={(e) => setForm({...form, founder_name: e.target.value})}
                className="bg-black border-zinc-800 rounded-sm text-sm font-mono mt-1" placeholder="Your name" />
            </div>
            <div>
              <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Startup Name *</label>
              <Input data-testid="startup-name-input" value={form.startup_name} onChange={(e) => setForm({...form, startup_name: e.target.value})}
                className="bg-black border-zinc-800 rounded-sm text-sm font-mono mt-1" placeholder="Company name" />
            </div>
            <div className="md:col-span-2">
              <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Description *</label>
              <Textarea data-testid="startup-description-input" value={form.description} onChange={(e) => setForm({...form, description: e.target.value})}
                className="bg-black border-zinc-800 rounded-sm text-sm font-mono mt-1 min-h-[100px]" placeholder="What does your startup do?" />
            </div>
            <div>
              <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Stage</label>
              <Select value={form.stage} onValueChange={(v) => setForm({...form, stage: v})}>
                <SelectTrigger className="bg-black border-zinc-800 rounded-sm text-xs font-mono mt-1"><SelectValue /></SelectTrigger>
                <SelectContent className="bg-[#0A0A0A] border-zinc-800">
                  {STAGES.map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Sector</label>
              <Select value={form.sector} onValueChange={(v) => setForm({...form, sector: v})}>
                <SelectTrigger className="bg-black border-zinc-800 rounded-sm text-xs font-mono mt-1"><SelectValue /></SelectTrigger>
                <SelectContent className="bg-[#0A0A0A] border-zinc-800">
                  {SECTORS.map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Target Raise (USD)</label>
              <Input data-testid="target-raise-input" type="number" value={form.target_raise} onChange={(e) => setForm({...form, target_raise: e.target.value})}
                className="bg-black border-zinc-800 rounded-sm text-sm font-mono mt-1" placeholder="e.g., 500000" />
            </div>
            <div>
              <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Website URL</label>
              <Input data-testid="website-url-input" value={form.website_url} onChange={(e) => setForm({...form, website_url: e.target.value})}
                className="bg-black border-zinc-800 rounded-sm text-sm font-mono mt-1" placeholder="https://..." />
            </div>
            <div>
              <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">App URL / Demo Link</label>
              <Input value={form.app_url} onChange={(e) => setForm({...form, app_url: e.target.value})}
                className="bg-black border-zinc-800 rounded-sm text-sm font-mono mt-1" placeholder="App store or demo link" />
            </div>
            <div>
              <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Video URL (YouTube/Loom)</label>
              <Input value={form.video_url} onChange={(e) => setForm({...form, video_url: e.target.value})}
                className="bg-black border-zinc-800 rounded-sm text-sm font-mono mt-1" placeholder="Video demo link" />
            </div>
            <div className="md:col-span-2">
              <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Upload Screenshots / Files</label>
              <div className="mt-1 flex items-center gap-3">
                <label className="bg-zinc-900 border border-zinc-800 hover:bg-zinc-800 text-zinc-300 text-xs font-mono px-4 py-2.5 rounded-sm cursor-pointer flex items-center gap-2">
                  <Upload size={14} /> {uploading ? "Uploading..." : "Choose File"}
                  <input type="file" className="hidden" onChange={handleFileUpload} disabled={uploading} data-testid="file-upload-input" />
                </label>
                {form.screenshot_urls.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {form.screenshot_urls.map((f, i) => (
                      <Badge key={i} variant="outline" className="border-zinc-700 text-zinc-400 text-[10px] font-mono rounded-sm">{f}</Badge>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
          <Button
            data-testid="submit-startup-btn"
            onClick={handleSubmit}
            disabled={submitting}
            className="mt-4 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-sm uppercase tracking-wider text-xs px-8 py-2.5"
          >
            {submitting ? "Registering..." : "Register Startup"}
          </Button>
        </div>
      )}

      {/* Registered Startups */}
      <div className="space-y-3">
        <h2 className="font-heading text-2xl font-bold text-white mb-4">Registered Startups</h2>
        {startups.length === 0 ? (
          <div className="text-center py-12 text-zinc-500 font-mono text-sm">No startups registered yet. Be the first!</div>
        ) : (
          startups.map(s => (
            <div key={s.id} data-testid={`startup-${s.id}`} className="bg-[#0A0A0A] border border-zinc-800 p-5 rounded-sm hover:border-zinc-600 transition-colors">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="text-sm font-bold text-white">{s.startup_name}</h3>
                    <Badge variant="outline" className="bg-blue-500/10 text-blue-400 border-blue-500/30 text-[10px] font-mono rounded-sm">{s.sector}</Badge>
                    <Badge variant="outline" className="border-zinc-700 text-zinc-400 text-[10px] font-mono rounded-sm">{s.stage}</Badge>
                  </div>
                  <p className="text-xs text-zinc-400 mb-2">{s.description}</p>
                  <div className="flex items-center gap-3 text-[10px] font-mono text-zinc-500">
                    <span>Founder: {s.founder_name}</span>
                    {s.target_raise > 0 && <span>Target: ${s.target_raise.toLocaleString()}</span>}
                    {s.website_url && (
                      <a href={s.website_url} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 flex items-center gap-1">
                        <Globe size={10} /> Website
                      </a>
                    )}
                    {s.video_url && (
                      <a href={s.video_url} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 flex items-center gap-1">
                        <ExternalLink size={10} /> Video Demo
                      </a>
                    )}
                  </div>
                </div>
                <Badge variant="outline" className="bg-emerald-500/10 text-emerald-400 border-emerald-500/30 text-[10px] font-mono rounded-sm">
                  {s.status || "Active"}
                </Badge>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
