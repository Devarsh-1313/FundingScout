import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ExternalLink, Newspaper } from "lucide-react";
import axios from "axios";

const API = "/api";
const CATEGORIES = ["All", "Funding", "Product Launch", "M&A", "Partnership", "Analysis", "Accelerator", "Industry"];

export default function NewsAggregator() {
  const [articles, setArticles] = useState([]);
  const [category, setCategory] = useState("All");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const params = {};
    if (category !== "All") params.category = category;
    axios.get(`${API}/news`, { params })
      .then(r => { setArticles(r.data.articles); setLoading(false); })
      .catch(() => setLoading(false));
  }, [category]);

  const formatTime = (d) => {
    const diff = (Date.now() - new Date(d).getTime()) / 1000;
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return `${Math.floor(diff / 86400)}d ago`;
  };

  const catColor = (c) => {
    const map = { "Funding": "text-emerald-400 bg-emerald-500/10", "Product Launch": "text-blue-400 bg-blue-500/10", "M&A": "text-purple-400 bg-purple-500/10", "Partnership": "text-cyan-400 bg-cyan-500/10", "Analysis": "text-yellow-400 bg-yellow-500/10", "Accelerator": "text-pink-400 bg-pink-500/10" };
    return map[c] || "text-zinc-400 bg-zinc-500/10";
  };

  return (
    <div className="animate-fade-in max-w-[1400px]" data-testid="news-page">
      <div className="mb-8">
        <h1 className="font-heading text-4xl sm:text-5xl font-black tracking-tight uppercase text-white">
          <Newspaper className="inline mr-2 text-blue-400" size={36} />
          News Aggregator
        </h1>
        <p className="text-sm text-zinc-400 mt-2">AI-summarized startup and venture capital news</p>
      </div>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        {CATEGORIES.map(c => (
          <Button
            key={c}
            data-testid={`news-cat-${c.toLowerCase().replace(/[^a-z]/g, "")}`}
            onClick={() => setCategory(c)}
            className={`text-xs font-mono rounded-sm px-3 py-1.5 h-auto ${
              category === c
                ? "bg-blue-600 text-white"
                : "bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-white hover:bg-zinc-800"
            }`}
          >
            {c}
          </Button>
        ))}
      </div>

      {/* News Feed */}
      {loading ? (
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => <div key={i} className="bg-[#0A0A0A] border border-zinc-800 h-32 animate-pulse rounded-sm" />)}
        </div>
      ) : (
        <div className="space-y-3">
          {articles.map((a) => (
            <div key={a.id} data-testid={`news-article-${a.id}`} className="bg-[#0A0A0A] border border-zinc-800 p-5 rounded-sm hover:border-zinc-600 transition-colors group">
              <div className="flex gap-4">
                {a.thumbnail && (
                  <img src={a.thumbnail} alt="" className="w-24 h-24 object-cover rounded-sm flex-shrink-0 border border-zinc-800" />
                )}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded-sm ${catColor(a.category)}`}>{a.category}</span>
                    <span className="text-[10px] font-mono text-zinc-600">{a.source}</span>
                    <span className="text-[10px] font-mono text-zinc-700">{formatTime(a.published_at)}</span>
                  </div>
                  <h3 className="text-sm font-medium text-white mb-2 group-hover:text-blue-400 transition-colors">{a.title}</h3>
                  <p className="text-xs text-zinc-400 leading-relaxed line-clamp-3">{a.summary}</p>
                  <a
                    href={a.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-[10px] font-mono text-blue-400 hover:text-blue-300 mt-2"
                  >
                    Read full article <ExternalLink size={10} />
                  </a>
                </div>
              </div>
            </div>
          ))}
          {articles.length === 0 && (
            <div className="text-center py-12 text-zinc-500 font-mono text-sm">No articles found</div>
          )}
        </div>
      )}
    </div>
  );
}
