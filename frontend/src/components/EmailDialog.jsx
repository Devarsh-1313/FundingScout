import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Mail } from "lucide-react";
import { toast } from "sonner";
import axios from "axios";

const API = "/api";

export default function EmailDialog({ investor }) {
  const [open, setOpen] = useState(false);
  const [sending, setSending] = useState(false);
  const [form, setForm] = useState({
    subject: "",
    content: "",
    template: "custom",
    senderName: "",
  });

  const handleSend = async () => {
    if (!investor?.email) {
      toast.error("No email address available");
      return;
    }
    setSending(true);
    try {
      await axios.post(`${API}/send-email`, {
        recipient_email: investor.email,
        subject: form.subject || `Intro from ${form.senderName}`,
        html_content: form.content,
        template_type: form.template === "custom" ? null : form.template,
        investor_name: investor.name,
        sender_name: form.senderName,
      });
      toast.success(`Email sent to ${investor.name}`);
      setOpen(false);
      setForm({ subject: "", content: "", template: "custom", senderName: "" });
    } catch (e) {
      toast.error("Failed to send email");
    } finally {
      setSending(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button
          data-testid="email-investor-btn"
          className="bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-sm uppercase tracking-wider text-xs px-4 py-2 shadow-[0_0_15px_rgba(59,130,246,0.3)] hover:shadow-[0_0_25px_rgba(59,130,246,0.5)]"
        >
          <Mail size={14} className="mr-2" /> Contact
        </Button>
      </DialogTrigger>
      <DialogContent className="bg-[#0A0A0A] border-zinc-800 rounded-sm max-w-lg" data-testid="email-dialog">
        <DialogHeader>
          <DialogTitle className="font-heading text-xl text-white tracking-tight">
            Contact {investor?.name}
          </DialogTitle>
        </DialogHeader>
        <div className="space-y-4 mt-4">
          <div>
            <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Template</label>
            <Select value={form.template} onValueChange={(v) => setForm({ ...form, template: v })}>
              <SelectTrigger className="bg-black border-zinc-800 rounded-sm text-sm font-mono mt-1">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-[#0A0A0A] border-zinc-800">
                <SelectItem value="custom">Custom Email</SelectItem>
                <SelectItem value="pitch_deck">Pitch Deck Sharing</SelectItem>
                <SelectItem value="meeting_request">Meeting Request</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Your Name</label>
            <Input
              data-testid="sender-name-input"
              value={form.senderName}
              onChange={(e) => setForm({ ...form, senderName: e.target.value })}
              className="bg-black border-zinc-800 rounded-sm text-sm font-mono mt-1"
              placeholder="Your name"
            />
          </div>
          <div>
            <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Subject</label>
            <Input
              data-testid="email-subject-input"
              value={form.subject}
              onChange={(e) => setForm({ ...form, subject: e.target.value })}
              className="bg-black border-zinc-800 rounded-sm text-sm font-mono mt-1"
              placeholder="Email subject"
            />
          </div>
          <div>
            <label className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">Message</label>
            <Textarea
              data-testid="email-content-input"
              value={form.content}
              onChange={(e) => setForm({ ...form, content: e.target.value })}
              className="bg-black border-zinc-800 rounded-sm text-sm font-mono mt-1 min-h-[120px]"
              placeholder="Write your message..."
            />
          </div>
          <div className="flex justify-between items-center pt-2">
            <span className="text-xs font-mono text-zinc-600">To: {investor?.email || "N/A"}</span>
            <Button
              data-testid="send-email-btn"
              onClick={handleSend}
              disabled={sending || !form.content}
              className="bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-sm uppercase tracking-wider text-xs px-6 py-2.5"
            >
              {sending ? "Sending..." : "Send Email"}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
