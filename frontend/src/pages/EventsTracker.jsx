import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Calendar, MapPin, ExternalLink, Clock } from "lucide-react";
import axios from "axios";

const API = "/api";
const CATEGORIES = ["All", "Conference", "Demo Day", "Hackathon", "Accelerator"];

export default function EventsTracker() {
  const [events, setEvents] = useState([]);
  const [category, setCategory] = useState("All");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const params = {};
    if (category !== "All") params.category = category;
    axios.get(`${API}/events`, { params })
      .then(r => { setEvents(r.data.events); setLoading(false); })
      .catch(() => setLoading(false));
  }, [category]);

  const daysUntil = (d) => {
    const diff = (new Date(d) - Date.now()) / (1000 * 60 * 60 * 24);
    if (diff < 0) return "Past";
    if (diff < 1) return "Today";
    return `${Math.ceil(diff)} days`;
  };

  return (
    <div className="animate-fade-in max-w-[1400px]" data-testid="events-page">
      <div className="mb-8">
        <h1 className="font-heading text-4xl sm:text-5xl font-black tracking-tight uppercase text-white">
          <Calendar className="inline mr-2 text-blue-400" size={36} />
          Events & Incubation
        </h1>
        <p className="text-sm text-zinc-400 mt-2">Track incubation cohorts, hackathons, demo days & conferences</p>
      </div>

      <div className="flex flex-wrap gap-2 mb-6">
        {CATEGORIES.map(c => (
          <Button
            key={c}
            data-testid={`event-cat-${c.toLowerCase().replace(/[^a-z]/g, "")}`}
            onClick={() => setCategory(c)}
            className={`text-xs font-mono rounded-sm px-3 py-1.5 h-auto ${
              category === c ? "bg-blue-600 text-white" : "bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-white hover:bg-zinc-800"
            }`}
          >
            {c}
          </Button>
        ))}
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[...Array(4)].map((_, i) => <div key={i} className="bg-[#0A0A0A] border border-zinc-800 h-48 animate-pulse rounded-sm" />)}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {events.map(e => (
            <div key={e.id} data-testid={`event-${e.id}`} className="bg-[#0A0A0A] border border-zinc-800 p-6 rounded-sm hover:border-zinc-600 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <Badge variant="outline" className="text-[10px] font-mono border-zinc-700 text-zinc-400 mb-2 rounded-sm">{e.category}</Badge>
                  <h3 className="text-base font-medium text-white">{e.name}</h3>
                </div>
                <div className="text-right">
                  <span className={`text-xs font-mono px-2 py-1 rounded-sm ${
                    daysUntil(e.date) === "Past" ? "bg-zinc-800 text-zinc-500" :
                    parseInt(daysUntil(e.date)) <= 7 ? "bg-red-500/10 text-red-400" : "bg-emerald-500/10 text-emerald-400"
                  }`}>
                    {daysUntil(e.date)}
                  </span>
                </div>
              </div>
              <p className="text-xs text-zinc-400 mb-4 leading-relaxed">{e.description}</p>
              <div className="space-y-2 text-[10px] font-mono text-zinc-500">
                <div className="flex items-center gap-2">
                  <Calendar size={12} /> <span>{e.date}</span>
                  <span className="text-zinc-700">|</span>
                  <MapPin size={12} /> <span>{e.location}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`px-1.5 py-0.5 rounded-sm ${e.type === "Virtual" ? "bg-blue-500/10 text-blue-400" : "bg-purple-500/10 text-purple-400"}`}>
                    {e.type}
                  </span>
                </div>
                {e.eligibility && <p className="text-zinc-600">Eligibility: {e.eligibility}</p>}
                {e.deadline && e.deadline !== "N/A" && (
                  <div className="flex items-center gap-1 text-yellow-500">
                    <Clock size={10} /> Deadline: {e.deadline}
                  </div>
                )}
              </div>
              {e.link && (
                <a
                  href={e.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-4 inline-flex items-center gap-1 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold px-4 py-2 rounded-sm uppercase tracking-wider"
                  data-testid={`register-event-${e.id}`}
                >
                  Register <ExternalLink size={12} />
                </a>
              )}
            </div>
          ))}
          {events.length === 0 && <div className="col-span-2 text-center py-12 text-zinc-500 font-mono text-sm">No events found</div>}
        </div>
      )}
    </div>
  );
}
