import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Rocket, ExternalLink, Shield } from "lucide-react";
import axios from "axios";

const API = "/api";

export default function Accelerators() {
  const [accelerators, setAccelerators] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API}/accelerators`)
    .then(r => { 
      console.log("API:", r.data); // DEBUG
      setAccelerators(Array.isArray(r.data) ? r.data : r.data.accelerators || []);
      setLoading(false); 
    })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="animate-fade-in max-w-[1400px]" data-testid="accelerators-page">
      <div className="mb-8">
        <h1 className="font-heading text-4xl sm:text-5xl font-black tracking-tight uppercase text-white">
          <Rocket className="inline mr-2 text-blue-400" size={36} />
          Elite Accelerators
        </h1>
        <p className="text-sm text-zinc-400 mt-2">Verified global accelerator programs - YC, Techstars, Alchemist & more</p>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[...Array(4)].map((_, i) => <div key={i} className="bg-[#0A0A0A] border border-zinc-800 h-64 animate-pulse rounded-sm" />)}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {accelerators.map(a => (
            <div key={a.id} data-testid={`accelerator-${a.id}`} className="bg-[#0A0A0A] border border-zinc-800 p-6 rounded-sm hover:border-zinc-600 transition-colors">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    {a.trust_label && (
                      <span className="flex items-center gap-1 text-[10px] font-mono bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded-sm">
                        <Shield size={10} /> {a.trust_label}
                      </span>
                    )}
                  </div>
                  <h3 className="text-lg font-bold text-white">{a.name}</h3>
                  <p className="text-xs font-mono text-zinc-500">{a.location}</p>
                </div>
                <Badge variant="outline" className={`text-[10px] font-mono rounded-sm ${
                  a.application_status?.toLowerCase().includes("open") ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30" : "bg-zinc-500/10 text-zinc-400 border-zinc-500/30"
                }`}>
                  {a.application_status}
                </Badge>
              </div>

              <div className="grid grid-cols-2 gap-3 mb-4 text-[10px] font-mono">
                <div className="bg-black/50 p-3 rounded-sm border border-zinc-900">
                  <p className="text-zinc-600 uppercase tracking-wider mb-1">Investment</p>
                  <p className="text-emerald-400 text-xs">{a.investment_amount}</p>
                </div>
                <div className="bg-black/50 p-3 rounded-sm border border-zinc-900">
                  <p className="text-zinc-600 uppercase tracking-wider mb-1">Equity</p>
                  <p className="text-yellow-400 text-xs">{a.equity_taken}</p>
                </div>
                <div className="bg-black/50 p-3 rounded-sm border border-zinc-900">
                  <p className="text-zinc-600 uppercase tracking-wider mb-1">Batch Size</p>
                  <p className="text-zinc-300 text-xs">{a.batch_size}</p>
                </div>
                <div className="bg-black/50 p-3 rounded-sm border border-zinc-900">
                  <p className="text-zinc-600 uppercase tracking-wider mb-1">Program Lead</p>
                  <p className="text-zinc-300 text-xs">{a.program_lead}</p>
                </div>
              </div>

              <div className="mb-4">
                <p className="text-[10px] font-mono text-zinc-600 uppercase tracking-wider mb-2">Focus Sectors</p>
                <div className="flex flex-wrap gap-1">
                  {(a.focus_sectors || []).map(s => (
                    <Badge key={s} variant="outline" className="bg-blue-500/10 text-blue-400 border-blue-500/30 text-[9px] font-mono rounded-sm">{s}</Badge>
                  ))}
                </div>
              </div>

              <div className="mb-4">
                <p className="text-[10px] font-mono text-zinc-600 uppercase tracking-wider mb-2">Portfolio Highlights</p>
                <div className="flex flex-wrap gap-1">
                  {(a.portfolio_highlights || []).slice(0, 6).map(p => (
                    <span key={p} className="text-[9px] font-mono bg-zinc-900 text-zinc-400 px-2 py-0.5 rounded-sm border border-zinc-800">{p}</span>
                  ))}
                </div>
              </div>

              {a.website && (
                <a
                  href={a.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-[10px] font-mono text-blue-400 hover:text-blue-300"
                  data-testid={`visit-accelerator-${a.id}`}
                >
                  Visit Website <ExternalLink size={10} />
                </a>
              )}
            </div>
          ))}
          {accelerators.length === 0 && <div className="col-span-2 text-center py-12 text-zinc-500 font-mono text-sm">No accelerators found</div>}
        </div>
      )}
    </div>
  );
}
