import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Clock, Download } from "lucide-react";
import { toast } from "sonner";
import axios from "axios";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function NewUpdated() {
  const navigate = useNavigate();
  const [investors, setInvestors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API}/investors/new-updated`)
      .then(r => { setInvestors(r.data.investors); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const handleExport = async () => {
    try {
      const r = await axios.get(`${API}/investors/export-csv`, { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([r.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = `new_updated_${new Date().toISOString().split("T")[0]}.csv`;
      a.click();
      toast.success("CSV exported");
    } catch {
      toast.error("Export failed");
    }
  };

  const formatTime = (d) => {
    if (!d) return "N/A";
    const diff = (Date.now() - new Date(d).getTime()) / 1000;
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return new Date(d).toLocaleDateString();
  };

  return (
    <div className="animate-fade-in max-w-[1400px]" data-testid="new-updated-page">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-heading text-4xl sm:text-5xl font-black tracking-tight uppercase text-white">
            <Clock className="inline mr-2 text-blue-400" size={36} />
            New & Updated
          </h1>
          <p className="text-sm text-zinc-400 mt-2">
            Investors added or changed in the last 24 hours
            <span className="font-mono text-blue-400 ml-2">({investors.length})</span>
          </p>
        </div>
        <Button
          data-testid="export-new-updated-btn"
          onClick={handleExport}
          className="bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-sm uppercase tracking-wider text-xs px-4"
        >
          <Download size={14} className="mr-1" /> Export CSV
        </Button>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => <div key={i} className="bg-[#0A0A0A] border border-zinc-800 h-20 animate-pulse rounded-sm" />)}
        </div>
      ) : investors.length === 0 ? (
        <div className="bg-[#0A0A0A] border border-zinc-800 p-12 rounded-sm text-center">
          <Clock size={48} className="mx-auto text-zinc-700 mb-4" />
          <p className="text-zinc-500 font-mono text-sm">No new or updated investors in the last 24 hours</p>
          <p className="text-zinc-600 font-mono text-xs mt-2">The auto-updater runs daily to check for new data</p>
        </div>
      ) : (
        <div className="space-y-2">
          {investors.map(inv => (
            <div
              key={inv.id}
              data-testid={`new-updated-row-${inv.id}`}
              className="bg-[#0A0A0A] border border-zinc-800 p-4 rounded-sm hover:border-zinc-600 transition-colors cursor-pointer flex items-center gap-4"
              onClick={() => navigate(`/investors/${inv.id}`)}
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-mono font-bold text-white truncate">{inv.name}</h3>
                  <span className="text-xs font-mono text-zinc-500 truncate">{inv.institution}</span>
                </div>
                <div className="flex gap-2 mt-1">
                  <Badge variant="outline" className="border-zinc-700 text-zinc-400 text-[10px] font-mono rounded-sm">{inv.investor_type}</Badge>
                  {(inv.primary_sectors || []).slice(0, 2).map(s => (
                    <span key={s} className="text-[9px] font-mono bg-blue-500/10 text-blue-400 px-1.5 py-0.5 rounded-sm">{s}</span>
                  ))}
                </div>
              </div>
              <div className="text-right flex-shrink-0">
                <p className="text-[10px] font-mono text-zinc-500">Updated</p>
                <p className="text-xs font-mono text-zinc-300">{formatTime(inv.updated_at)}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
