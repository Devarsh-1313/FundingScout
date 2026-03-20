import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Search, Download, ChevronLeft, ChevronRight, Filter, X } from "lucide-react";
import { toast } from "sonner";
import axios from "axios";

const API = "/api";
const INVESTOR_TYPES = ["All", "VC", "Angel", "Family Office", "Accelerator", "CVC"];
const STAGES = ["All", "Pre-seed", "Seed", "Pre-Series A", "Series A", "Series B", "Series C", "Growth", "Late Stage"];
const PRIORITIES = ["All", "High", "Medium", "Low"];

export default function InvestorDatabase() {
  const navigate = useNavigate();
  const [investors, setInvestors] = useState([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [filters, setFilters] = useState({ type: "All", stage: "All", priority: "All", geography: "" });
  const [showFilters, setShowFilters] = useState(false);

  const fetchInvestors = useCallback(async () => {
    setLoading(true);
    try {
      const params = { page, limit: 25, search };
      if (filters.type !== "All") params.investor_type = filters.type;
      if (filters.stage !== "All") params.stage = filters.stage;
      if (filters.priority !== "All") params.priority = filters.priority;
      if (filters.geography) params.geography = filters.geography;
      const r = await axios.get(`${API}/investors`, { params });
      setInvestors(r.data.investors);
      setTotal(r.data.total);
      setTotalPages(r.data.total_pages);
    } catch (e) {
      toast.error("Failed to load investors");
    } finally {
      setLoading(false);
    }
  }, [page, search, filters]);

  useEffect(() => { fetchInvestors(); }, [fetchInvestors]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchInvestors();
  };

  const handleExport = async () => {
    try {
      const params = new URLSearchParams();
      if (search) params.append("search", search);
      if (filters.type !== "All") params.append("investor_type", filters.type);
      if (filters.stage !== "All") params.append("stage", filters.stage);
      if (filters.priority !== "All") params.append("priority", filters.priority);
      if (filters.geography) params.append("geography", filters.geography);
      
      const r = await axios.get(`${API}/investors/export-csv?${params.toString()}`, { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([r.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = `investors_${new Date().toISOString().split("T")[0]}.csv`;
      a.click();
      toast.success("CSV exported successfully");
    } catch {
      toast.error("Export failed");
    }
  };

  const priorityClass = (p) => p === "High" ? "badge-high" : p === "Medium" ? "badge-medium" : "badge-low";

  const formatCheque = (min, max, currency) => {
    const fmt = (n) => {
      if (n >= 1e9) return `${(n/1e9).toFixed(1)}B`;
      if (n >= 1e6) return `${(n/1e6).toFixed(1)}M`;
      if (n >= 1e3) return `${(n/1e3).toFixed(0)}K`;
      return n.toString();
    };
    return `${currency === "USD" ? "$" : currency}${fmt(min)} - ${fmt(max)}`;
  };

  return (
    <div className="animate-fade-in max-w-[1920px]" data-testid="investor-database">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-6 gap-4">
        <div>
          <h1 className="font-heading text-4xl sm:text-5xl font-black tracking-tight uppercase text-white">
            Investor Database
          </h1>
          <p className="text-sm text-zinc-400 mt-1">
            <span className="font-mono text-blue-400">{total.toLocaleString()}</span> investors tracked
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            data-testid="toggle-filters-btn"
            variant="outline"
            onClick={() => setShowFilters(!showFilters)}
            className="bg-zinc-900 border-zinc-800 hover:bg-zinc-800 text-zinc-300 text-xs rounded-sm"
          >
            <Filter size={14} className="mr-1" /> Filters
          </Button>
          <Button
            data-testid="export-csv-btn"
            onClick={handleExport}
            className="bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-sm uppercase tracking-wider text-xs px-4"
          >
            <Download size={14} className="mr-1" /> Export CSV
          </Button>
        </div>
      </div>

      {/* Search */}
      <form onSubmit={handleSearch} className="flex gap-2 mb-4">
        <div className="relative flex-1">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-600" />
          <Input
            data-testid="investor-search-input"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search investors, funds, sectors, deals..."
            className="bg-black border-zinc-800 focus:border-blue-600 rounded-sm text-sm font-mono pl-10 h-10"
          />
        </div>
        <Button type="submit" data-testid="search-btn" className="bg-zinc-900 border border-zinc-800 hover:bg-zinc-800 text-white rounded-sm text-xs px-4">
          Search
        </Button>
      </form>

      {/* Filters */}
      {showFilters && (
        <div className="bg-[#0A0A0A] border border-zinc-800 p-4 rounded-sm mb-4 grid grid-cols-2 md:grid-cols-4 gap-3 animate-fade-in" data-testid="filters-panel">
          <div>
            <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Type</label>
            <Select value={filters.type} onValueChange={(v) => { setFilters({...filters, type: v}); setPage(1); }}>
              <SelectTrigger className="bg-black border-zinc-800 rounded-sm text-xs font-mono mt-1 h-9"><SelectValue /></SelectTrigger>
              <SelectContent className="bg-[#0A0A0A] border-zinc-800">
                {INVESTOR_TYPES.map(t => <SelectItem key={t} value={t}>{t}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Stage</label>
            <Select value={filters.stage} onValueChange={(v) => { setFilters({...filters, stage: v}); setPage(1); }}>
              <SelectTrigger className="bg-black border-zinc-800 rounded-sm text-xs font-mono mt-1 h-9"><SelectValue /></SelectTrigger>
              <SelectContent className="bg-[#0A0A0A] border-zinc-800">
                {STAGES.map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Priority</label>
            <Select value={filters.priority} onValueChange={(v) => { setFilters({...filters, priority: v}); setPage(1); }}>
              <SelectTrigger className="bg-black border-zinc-800 rounded-sm text-xs font-mono mt-1 h-9"><SelectValue /></SelectTrigger>
              <SelectContent className="bg-[#0A0A0A] border-zinc-800">
                {PRIORITIES.map(p => <SelectItem key={p} value={p}>{p}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Geography</label>
            <Input
              data-testid="geography-filter"
              value={filters.geography}
              onChange={(e) => { setFilters({...filters, geography: e.target.value}); setPage(1); }}
              placeholder="e.g., India, USA"
              className="bg-black border-zinc-800 rounded-sm text-xs font-mono mt-1 h-9"
            />
          </div>
        </div>
      )}

      {/* Table */}
      <div className="bg-[#0A0A0A] border border-zinc-800 rounded-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full inv-table" data-testid="investor-table">
            <thead>
              <tr>
                <th className="text-left">Name</th>
                <th className="text-left">Institution</th>
                <th className="text-left">Type</th>
                <th className="text-left">Cheque Size</th>
                <th className="text-left">Stage</th>
                <th className="text-left">Sectors</th>
                <th className="text-left">India</th>
                <th className="text-left">Priority</th>
                <th className="text-left">Status</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                [...Array(10)].map((_, i) => (
                  <tr key={i}><td colSpan={9}><div className="h-8 bg-zinc-900 animate-pulse rounded-sm" /></td></tr>
                ))
              ) : investors.length === 0 ? (
                <tr><td colSpan={9} className="text-center text-zinc-500 py-12">No investors found</td></tr>
              ) : (
                investors.map((inv) => (
                  <tr
                    key={inv.id}
                    data-testid={`investor-row-${inv.id}`}
                    className="cursor-pointer"
                    onClick={() => navigate(`/investors/${inv.id}`)}
                  >
                    <td className="font-medium text-white whitespace-nowrap">{inv.name}</td>
                    <td className="text-zinc-400 whitespace-nowrap max-w-[180px] truncate">{inv.institution}</td>
                    <td>
                      <Badge variant="outline" className="border-zinc-700 text-zinc-400 text-[10px] font-mono rounded-sm">
                        {inv.investor_type}
                      </Badge>
                    </td>
                    <td className="text-zinc-300 whitespace-nowrap">
                      {formatCheque(inv.cheque_size_min, inv.cheque_size_max, inv.cheque_size_currency)}
                    </td>
                    <td className="text-zinc-400 whitespace-nowrap max-w-[140px] truncate">
                      {(inv.stage || []).join(", ")}
                    </td>
                    <td className="max-w-[180px]">
                      <div className="flex flex-wrap gap-1">
                        {(inv.primary_sectors || []).slice(0, 2).map(s => (
                          <span key={s} className="text-[9px] font-mono bg-blue-500/10 text-blue-400 px-1.5 py-0.5 rounded-sm">{s}</span>
                        ))}
                        {(inv.primary_sectors || []).length > 2 && (
                          <span className="text-[9px] font-mono text-zinc-600">+{inv.primary_sectors.length - 2}</span>
                        )}
                      </div>
                    </td>
                    <td>
                      {inv.invests_in_india ? (
                        <span className="text-[10px] font-mono text-emerald-400">YES</span>
                      ) : (
                        <span className="text-[10px] font-mono text-zinc-600">NO</span>
                      )}
                    </td>
                    <td>
                      <Badge variant="outline" className={`${priorityClass(inv.priority_tag)} text-[10px] font-mono rounded-sm`}>
                        {inv.priority_tag}
                      </Badge>
                    </td>
                    <td>
                      <span className={`text-[10px] font-mono ${inv.contacted ? "text-emerald-400" : "text-zinc-600"}`}>
                        {inv.contact_status}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="flex items-center justify-between px-4 py-3 border-t border-zinc-800">
          <span className="text-[10px] font-mono text-zinc-500">
            Page {page} of {totalPages} ({total} results)
          </span>
          <div className="flex gap-1">
            <Button
              data-testid="prev-page-btn"
              variant="ghost"
              size="sm"
              disabled={page <= 1}
              onClick={() => setPage(p => p - 1)}
              className="text-zinc-400 hover:text-white h-8 w-8 p-0"
            >
              <ChevronLeft size={16} />
            </Button>
            {[...Array(Math.min(5, totalPages))].map((_, i) => {
              const p = Math.max(1, Math.min(page - 2, totalPages - 4)) + i;
              if (p > totalPages) return null;
              return (
                <Button
                  key={p}
                  variant="ghost"
                  size="sm"
                  onClick={() => setPage(p)}
                  className={`h-8 w-8 p-0 text-xs font-mono ${page === p ? "bg-blue-600/20 text-blue-400" : "text-zinc-500 hover:text-white"}`}
                >
                  {p}
                </Button>
              );
            })}
            <Button
              data-testid="next-page-btn"
              variant="ghost"
              size="sm"
              disabled={page >= totalPages}
              onClick={() => setPage(p => p + 1)}
              className="text-zinc-400 hover:text-white h-8 w-8 p-0"
            >
              <ChevronRight size={16} />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
