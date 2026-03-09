import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Sparkles, Target, ArrowRight, Loader2 } from "lucide-react";
import { toast } from "sonner";
import axios from "axios";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;
const STAGES = ["Pre-seed", "Seed", "Pre-Series A", "Series A", "Series B", "Series C"];

export default function IdeaMatch() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ description: "", stage: "Seed", target_raise: "", geography: "India" });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleMatch = async () => {
    if (!form.description.trim()) { toast.error("Please describe your startup"); return; }
    setLoading(true);
    try {
      const r = await axios.post(`${API}/idea-match`, {
        description: form.description,
        stage: form.stage,
        target_raise: parseFloat(form.target_raise) || 0,
        geography: form.geography,
      });
      setResults(r.data);
      toast.success(`Found ${r.data.total_matches} matching investors`);
    } catch {
      toast.error("Matching failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade-in max-w-[1400px]" data-testid="idea-match-page">
      <div className="mb-8">
        <h1 className="font-heading text-4xl sm:text-5xl font-black tracking-tight uppercase text-white">
          <Sparkles className="inline mr-2 text-blue-400" size={36} />
          Idea Match
        </h1>
        <p className="text-sm text-zinc-400 mt-2">AI-powered investor matching based on your startup profile</p>
      </div>

      {/* Input Form */}
      <div className="bg-[#0A0A0A] border border-zinc-800 p-6 rounded-sm mb-6">
        <div className="space-y-4">
          <div>
            <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Describe Your Startup</label>
            <Textarea
              data-testid="idea-description-input"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              className="bg-black border-zinc-800 focus:border-blue-600 rounded-sm text-sm font-mono mt-1 min-h-[120px]"
              placeholder="We're building an AI-powered SaaS platform for supply chain optimization in India. Our product helps D2C brands reduce logistics costs by 30% using real-time route optimization and demand forecasting..."
            />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Stage</label>
              <Select value={form.stage} onValueChange={(v) => setForm({ ...form, stage: v })}>
                <SelectTrigger className="bg-black border-zinc-800 rounded-sm text-xs font-mono mt-1"><SelectValue /></SelectTrigger>
                <SelectContent className="bg-[#0A0A0A] border-zinc-800">
                  {STAGES.map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Target Raise (USD)</label>
              <Input
                data-testid="target-raise-input"
                type="number"
                value={form.target_raise}
                onChange={(e) => setForm({ ...form, target_raise: e.target.value })}
                className="bg-black border-zinc-800 rounded-sm text-xs font-mono mt-1"
                placeholder="e.g., 500000"
              />
            </div>
            <div>
              <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Target Geography</label>
              <Input
                data-testid="target-geography-input"
                value={form.geography}
                onChange={(e) => setForm({ ...form, geography: e.target.value })}
                className="bg-black border-zinc-800 rounded-sm text-xs font-mono mt-1"
                placeholder="e.g., India"
              />
            </div>
          </div>
          <Button
            data-testid="find-matches-btn"
            onClick={handleMatch}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-sm uppercase tracking-wider text-xs px-8 py-3 shadow-[0_0_15px_rgba(59,130,246,0.3)] hover:shadow-[0_0_25px_rgba(59,130,246,0.5)]"
          >
            {loading ? <><Loader2 className="animate-spin mr-2" size={14} /> Matching...</> : <><Target size={14} className="mr-2" /> Find Matching Investors</>}
          </Button>
        </div>
      </div>

      {/* Results */}
      {results && (
        <div className="space-y-4" data-testid="match-results">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-heading text-2xl font-bold text-white">{results.total_matches} Matches Found</h2>
              <div className="flex gap-2 mt-2">
                {results.extracted_sectors?.map(s => (
                  <Badge key={s} variant="outline" className="bg-blue-500/10 text-blue-400 border-blue-500/30 text-[10px] font-mono rounded-sm">{s}</Badge>
                ))}
              </div>
            </div>
          </div>

          <div className="space-y-3">
            {results.matches?.map((inv, i) => (
              <div
                key={inv.id}
                data-testid={`match-result-${i}`}
                className="bg-[#0A0A0A] border border-zinc-800 p-5 rounded-sm hover:border-zinc-600 transition-colors cursor-pointer"
                onClick={() => navigate(`/investors/${inv.id}`)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-sm font-mono font-bold text-white">{inv.name}</h3>
                      <span className="text-xs font-mono text-zinc-500">{inv.institution}</span>
                      <Badge variant="outline" className="border-zinc-700 text-zinc-400 text-[10px] font-mono rounded-sm">{inv.investor_type}</Badge>
                    </div>
                    <div className="flex flex-wrap gap-2 mb-2">
                      {inv.match_reasons?.map((r, j) => (
                        <span key={j} className="text-[10px] font-mono bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded-sm">{r}</span>
                      ))}
                    </div>
                    <div className="flex gap-4 text-[10px] font-mono text-zinc-500">
                      <span>Cheque: ${(inv.cheque_size_min || 0).toLocaleString()} - ${(inv.cheque_size_max || 0).toLocaleString()}</span>
                      <span>Stages: {(inv.stage || []).join(", ")}</span>
                    </div>
                  </div>
                  <div className="text-right ml-4">
                    <div className={`text-2xl font-mono font-bold ${inv.match_score >= 70 ? "text-emerald-400" : inv.match_score >= 40 ? "text-yellow-400" : "text-zinc-500"}`}>
                      {inv.match_score}%
                    </div>
                    <p className="text-[10px] font-mono text-zinc-600">match</p>
                    <ArrowRight size={14} className="text-zinc-600 mt-2 ml-auto" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
