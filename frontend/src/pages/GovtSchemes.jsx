import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Landmark, ExternalLink, Filter } from "lucide-react";
import axios from "axios";

const API = "/api";
const CATEGORY_FILTERS = ["All", "Grant", "Equity-free funding", "Tax Exemptions"];

export default function GovtSchemes() {
  const [schemes, setSchemes] = useState([]);
  const [tier, setTier] = useState("all");
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const params = {};
    if (tier !== "all") params.tier = tier === "central" ? "Central" : "State";
    if (categoryFilter !== "All") params.category = categoryFilter;
    axios.get(`${API}/govt-schemes`, { params })
      .then(r => { setSchemes(r.data.schemes); setLoading(false); })
      .catch(() => setLoading(false));
  }, [tier, categoryFilter]);

  const catColor = (c) => {
    if (c === "Grant") return "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";
    if (c === "Equity-free funding") return "bg-blue-500/10 text-blue-400 border-blue-500/30";
    return "bg-yellow-500/10 text-yellow-400 border-yellow-500/30";
  };

  return (
    <div className="animate-fade-in max-w-[1400px]" data-testid="govt-schemes-page">
      <div className="mb-8">
        <h1 className="font-heading text-4xl sm:text-5xl font-black tracking-tight uppercase text-white">
          <Landmark className="inline mr-2 text-blue-400" size={36} />
          Govt Funding & Schemes
        </h1>
        <p className="text-sm text-zinc-400 mt-2">Government grants, equity-free funding, and tax exemptions for startups</p>
      </div>

      <Tabs value={tier} onValueChange={setTier} className="mb-6">
        <TabsList className="bg-zinc-900 border border-zinc-800 rounded-sm p-0.5">
          <TabsTrigger value="all" className="text-xs font-mono rounded-sm data-[state=active]:bg-blue-600 data-[state=active]:text-white">All</TabsTrigger>
          <TabsTrigger value="central" className="text-xs font-mono rounded-sm data-[state=active]:bg-blue-600 data-[state=active]:text-white">Central Govt</TabsTrigger>
          <TabsTrigger value="state" className="text-xs font-mono rounded-sm data-[state=active]:bg-blue-600 data-[state=active]:text-white">State Govt</TabsTrigger>
        </TabsList>
      </Tabs>

      <div className="flex flex-wrap gap-2 mb-6">
        {CATEGORY_FILTERS.map(c => (
          <Button
            key={c}
            data-testid={`scheme-cat-${c.toLowerCase().replace(/[^a-z]/g, "")}`}
            onClick={() => setCategoryFilter(c)}
            className={`text-xs font-mono rounded-sm px-3 py-1.5 h-auto ${
              categoryFilter === c ? "bg-blue-600 text-white" : "bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-white hover:bg-zinc-800"
            }`}
          >
            {c}
          </Button>
        ))}
      </div>

      {loading ? (
        <div className="space-y-4">
          {[...Array(4)].map((_, i) => <div key={i} className="bg-[#0A0A0A] border border-zinc-800 h-40 animate-pulse rounded-sm" />)}
        </div>
      ) : (
        <div className="space-y-4">
          {schemes.map(s => (
            <div key={s.id} data-testid={`scheme-${s.id}`} className="bg-[#0A0A0A] border border-zinc-800 p-6 rounded-sm hover:border-zinc-600 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <Badge variant="outline" className={`${catColor(s.category)} text-[10px] font-mono rounded-sm`}>{s.category}</Badge>
                    <Badge variant="outline" className="border-zinc-700 text-zinc-500 text-[10px] font-mono rounded-sm">{s.tier}</Badge>
                  </div>
                  <h3 className="text-base font-medium text-white mb-2">{s.name}</h3>
                  <p className="text-xs text-zinc-400 leading-relaxed mb-3">{s.description}</p>
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-[10px] font-mono">
                <div className="bg-black/50 p-3 rounded-sm border border-zinc-900">
                  <p className="text-zinc-600 uppercase tracking-wider mb-1">Amount</p>
                  <p className="text-emerald-400 text-xs">{s.amount}</p>
                </div>
                <div className="bg-black/50 p-3 rounded-sm border border-zinc-900">
                  <p className="text-zinc-600 uppercase tracking-wider mb-1">Eligibility</p>
                  <p className="text-zinc-300 text-xs">{s.eligibility}</p>
                </div>
                <div className="bg-black/50 p-3 rounded-sm border border-zinc-900">
                  <p className="text-zinc-600 uppercase tracking-wider mb-1">Deadline</p>
                  <p className="text-yellow-400 text-xs">{s.deadline || "Rolling"}</p>
                </div>
              </div>
              {s.apply_link && (
                <a
                  href={s.apply_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-4 inline-flex items-center gap-1 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold px-4 py-2 rounded-sm uppercase tracking-wider"
                  data-testid={`apply-scheme-${s.id}`}
                >
                  Direct Apply <ExternalLink size={12} />
                </a>
              )}
            </div>
          ))}
          {schemes.length === 0 && <div className="text-center py-12 text-zinc-500 font-mono text-sm">No schemes found</div>}
        </div>
      )}
    </div>
  );
}
