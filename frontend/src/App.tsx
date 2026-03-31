import { Fragment, useState, useEffect, useRef, useCallback } from 'react';
import { motion } from 'framer-motion';
import {
  Send,
  CheckCircle2,
  AlertTriangle,
  Users,
  TrendingUp,
  Copy,
  Check,
  ChevronUp,
  ChevronDown,
  Clock,
  Zap,
  Search,
  Brain,
  Sparkles,
  X,
  RefreshCw,
  Lightbulb,
  ArrowRight,
  FileText,
  Loader2,
  BarChart3,
  Activity,
  ShieldAlert,
  Database,
  Github,
} from 'lucide-react';
import { useShaderBackground } from '@/components/ui/animated-shader-hero';
import { Hero } from '@/components/ui/animated-hero';
import { Button } from '@/components/ui/button';

/* ═══════════════ TYPES ═══════════════ */

interface ValidationResult {
  score: number;
  summary: string;
  strengths: string[];
  risks: string[];
  competitors: string[];
  market_notes: string | null;
}

interface HistoryEntry {
  idea: string;
  score: number;
  timestamp: Date;
  fullResults: ValidationResult;
  fullIdea: string;
}

interface ToastData {
  id: number;
  message: string;
  type: 'success' | 'error' | 'info';
}

interface PipelineNode {
  key: string;
  label: string;
  Icon: React.FC<{ className?: string }>;
}

/* ═══════════════ CONSTANTS ═══════════════ */

const API = 'http://localhost:8000';

const EXAMPLE_IDEA =
  'An AI app that summarizes long PDFs for students in 3 bullet points.';

const PIPELINE_STEPS: PipelineNode[] = [
  { key: 'idea', label: 'Idea', Icon: FileText },
  { key: 'service', label: 'ValidationService', Icon: Zap },
  { key: 'agent', label: 'ValidatorAgent', Icon: Brain },
  { key: 'search', label: 'WebSearch', Icon: Search },
  { key: 'competitors', label: 'CompetitorFinder', Icon: Users },
  { key: 'market', label: 'MarketEstimator', Icon: TrendingUp },
  { key: 'llm', label: 'LLMClient', Icon: Sparkles },
  { key: 'report', label: 'Report', Icon: FileText },
];

const LOGOS = ['VENTURE.LAB', 'BUILDFAST', 'IDEX.AI', 'STACKR', 'FOUNDERKIT'];

const ARCH_NODES: { icon: React.FC<{ className?: string }>; label: string; desc: string }[] = [
  { icon: FileText, label: 'Your Idea', desc: 'Plain-text startup concept' },
  { icon: Zap, label: 'Validation Service', desc: 'FastAPI orchestration layer' },
  { icon: Brain, label: 'Validator Agent', desc: 'Core reasoning agent' },
  { icon: Search, label: 'Web Search', desc: 'Live market signals' },
  { icon: Users, label: 'Competitor Finder', desc: 'Who already exists' },
  { icon: TrendingUp, label: 'Market Estimator', desc: 'TAM & growth rate' },
  { icon: Sparkles, label: 'LLM Synthesis', desc: 'Claude/GPT reasoning layer' },
  { icon: FileText, label: 'Structured Report', desc: 'Score + insights JSON' },
];

const FEATURES: { icon: React.FC<{ className?: string }>; title: string; desc: string }[] = [
  { icon: Zap, title: 'Instant Viability Score', desc: '0–10 score with detailed reasoning, not just a number' },
  { icon: Search, title: 'Live Competitor Analysis', desc: "Real-time web search surfaces who's already in your space" },
  { icon: TrendingUp, title: 'Market Size Estimation', desc: 'TAM, growth rates, and industry signals pulled on demand' },
  { icon: ShieldAlert, title: 'Risk Mapping', desc: 'AI identifies the landmines before you step on them' },
  { icon: Brain, title: 'MCP Orchestration', desc: 'Model + Context + Tools running in a coordinated agent loop' },
  { icon: Database, title: 'Memory & Context', desc: 'Past validations stored with embeddings for similarity search' },
];

/* ═══════════════ TOAST SYSTEM ═══════════════ */

function ToastContainer({
  toasts,
  onDismiss,
  onRetry,
}: {
  toasts: ToastData[];
  onDismiss: (id: number) => void;
  onRetry?: () => void;
}) {
  return (
    <div className="fixed top-4 right-4 z-[100] flex flex-col gap-2 w-full max-w-sm pointer-events-none">
      {toasts.map((t) => (
        <ToastItem key={t.id} toast={t} onDismiss={onDismiss} onRetry={onRetry} />
      ))}
    </div>
  );
}

function ToastItem({
  toast,
  onDismiss,
  onRetry,
}: {
  toast: ToastData;
  onDismiss: (id: number) => void;
  onRetry?: () => void;
}) {
  const bg =
    toast.type === 'success'
      ? 'border-emerald-500/30 bg-emerald-500/10'
      : toast.type === 'error'
        ? 'border-red-500/30 bg-red-500/10'
        : 'border-indigo-500/30 bg-indigo-500/10';
  const IconEl =
    toast.type === 'success' ? CheckCircle2 : toast.type === 'error' ? AlertTriangle : Zap;
  const iconColor =
    toast.type === 'success' ? 'text-emerald-400' : toast.type === 'error' ? 'text-red-400' : 'text-indigo-400';

  return (
    <div className={`pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-xl border backdrop-blur-2xl animate-slide-in-right ${bg}`}>
      <IconEl className={`w-4 h-4 shrink-0 ${iconColor}`} />
      <span className="text-sm text-slate-200 flex-1">{toast.message}</span>
      {toast.type === 'error' && onRetry && (
        <button onClick={onRetry} className="text-[11px] text-red-400 hover:text-red-300 flex items-center gap-1 shrink-0">
          <RefreshCw className="w-3 h-3" /> Retry
        </button>
      )}
      <button onClick={() => onDismiss(toast.id)} className="text-slate-500 hover:text-slate-300 shrink-0">
        <X className="w-3.5 h-3.5" />
      </button>
    </div>
  );
}

/* ═══════════════ SKELETON LOADERS ═══════════════ */

function Skeleton({ className = '' }: { className?: string }) {
  return <div className={`skeleton rounded-lg ${className}`} />;
}

function ResultsSkeleton() {
  return (
    <div className="space-y-6">
      <div className="glass-card p-10 flex justify-center"><Skeleton className="w-52 h-52 !rounded-full" /></div>
      <div className="glass-card p-6 space-y-3"><Skeleton className="w-40 h-4" /><Skeleton className="w-full h-4" /><Skeleton className="w-4/5 h-4" /></div>
      <div className="grid md:grid-cols-2 gap-4">
        {[0, 1].map((i) => (
          <div key={i} className="glass-card p-6 space-y-3"><Skeleton className="w-28 h-4" /><Skeleton className="w-full h-9" /><Skeleton className="w-full h-9" /><Skeleton className="w-3/4 h-9" /></div>
        ))}
      </div>
    </div>
  );
}

/* ═══════════════ SCORE GAUGE ═══════════════ */

function ScoreGauge({ score }: { score: number }) {
  const [display, setDisplay] = useState(0);
  const R = 80;
  const C = 2 * Math.PI * R;
  const ARC = C * 0.75;

  useEffect(() => {
    if (score == null) return;
    setDisplay(0);
    let raf: number;
    const dur = 1500;
    const t0 = performance.now();
    const tick = (now: number) => {
      const p = Math.min((now - t0) / dur, 1);
      const ease = 1 - Math.pow(1 - p, 3);
      setDisplay(score * ease);
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [score]);

  const offset = ARC * (1 - display / 10);
  const color = display >= 7 ? '#22c55e' : display >= 4 ? '#f59e0b' : '#ef4444';
  const textCls = display >= 7 ? 'text-emerald-400' : display >= 4 ? 'text-amber-400' : 'text-red-400';

  return (
    <div className="flex flex-col items-center">
      <div className="relative">
        <svg width="220" height="220" viewBox="0 0 220 220">
          <defs>
            <filter id="arcGlow"><feGaussianBlur stdDeviation="5" result="b" /><feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge></filter>
          </defs>
          <circle cx="110" cy="110" r={R} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="14" strokeDasharray={`${ARC} ${C}`} strokeLinecap="round" transform="rotate(135 110 110)" />
          <circle cx="110" cy="110" r={R} fill="none" stroke={color} strokeWidth="14" strokeDasharray={`${ARC} ${C}`} strokeDashoffset={offset} strokeLinecap="round" transform="rotate(135 110 110)" filter="url(#arcGlow)" />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-5xl font-bold font-mono tabular-nums ${textCls}`}>{display.toFixed(1)}</span>
          <span className="text-[11px] text-slate-500 uppercase tracking-[0.2em] mt-1">out of 10</span>
        </div>
      </div>
      <span className="text-sm font-semibold text-slate-400 uppercase tracking-[0.15em] mt-3">Viability Score</span>
    </div>
  );
}

/* ═══════════════ MCP LOADING PIPELINE ═══════════════ */

function MCPLoadingPipeline({ step }: { step: number }) {
  return (
    <div className="flex items-center justify-center gap-1 md:gap-1.5 overflow-x-auto pb-2 px-2">
      {PIPELINE_STEPS.map((node, i) => {
        const active = step >= i;
        const { Icon } = node;
        return (
          <div key={node.key} className="flex items-center shrink-0">
            <div className={`flex flex-col items-center gap-1.5 px-2 md:px-3 py-2 rounded-lg border transition-all duration-500 ${active ? 'pipeline-active' : 'border-white/[0.06] bg-white/[0.02]'}`}>
              <Icon className={`w-3.5 h-3.5 md:w-4 md:h-4 transition-colors duration-500 ${active ? 'text-indigo-400' : 'text-slate-700'}`} />
              <span className={`text-[9px] md:text-[10px] font-medium whitespace-nowrap transition-colors duration-500 ${active ? 'text-indigo-300' : 'text-slate-700'}`}>{node.label}</span>
            </div>
            {i < PIPELINE_STEPS.length - 1 && (
              <ArrowRight className={`w-3 h-3 md:w-3.5 md:h-3.5 mx-0.5 shrink-0 transition-colors duration-500 ${step > i ? 'text-indigo-500' : 'text-slate-800'}`} />
            )}
          </div>
        );
      })}
    </div>
  );
}

/* ═══════════════ COMPETITOR CARD ═══════════════ */

const AVATAR_GRADIENTS = [
  'from-indigo-500 to-cyan-500',
  'from-violet-500 to-fuchsia-500',
  'from-cyan-500 to-emerald-500',
  'from-amber-500 to-orange-500',
  'from-rose-500 to-pink-500',
  'from-teal-500 to-lime-500',
];

function CompetitorCard({ name, index }: { name: string; index: number }) {
  const grad = AVATAR_GRADIENTS[index % AVATAR_GRADIENTS.length];
  return (
    <div className="glass-card p-4 min-w-[152px] flex flex-col items-center gap-3 cursor-default hover:border-indigo-500/40 hover:shadow-lg hover:shadow-indigo-500/10 hover:-translate-y-1 transition-all duration-300 shrink-0">
      <div className={`w-11 h-11 rounded-full bg-gradient-to-br ${grad} flex items-center justify-center text-white font-bold text-lg select-none`}>
        {name.charAt(0).toUpperCase()}
      </div>
      <span className="text-sm font-medium text-slate-200 text-center leading-tight">{name}</span>
      <span className="text-[10px] uppercase tracking-[0.15em] text-slate-600 font-medium">competitor</span>
    </div>
  );
}

/* ═══════════════ DIVIDER ═══════════════ */

function GradientDivider() {
  return <div className="h-px w-full bg-gradient-to-r from-transparent via-indigo-500/20 to-transparent" />;
}

/* ═══════════════ SOCIAL PROOF ═══════════════ */

function SocialProofBar() {
  return (
    <div className="py-10 relative">
      <div className="absolute inset-0 bg-[#080810]/80" />
      <div className="relative z-10">
        <p className="text-center text-[11px] uppercase tracking-[0.3em] text-slate-600 mb-6 font-medium">
          Trusted by founders, students &amp; innovation teams
        </p>
        <div className="flex items-center justify-center gap-8 md:gap-16 flex-wrap px-4">
          {LOGOS.map((logo) => (
            <span key={logo} className="text-sm md:text-base font-mono text-white/[0.12] tracking-[0.15em] font-semibold select-none">
              {logo}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ═══════════════ HOW IT WORKS — PIPELINE VIZ ═══════════════ */

function PipelinePill({ icon: Icon, label, desc }: { icon: React.FC<{ className?: string }>; label: string; desc: string }) {
  return (
    <div className="flex flex-col items-center gap-2 shrink-0">
      <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl border border-indigo-500/20 bg-white/[0.04] backdrop-blur-sm hover:bg-white/[0.07] hover:border-indigo-500/35 transition-all">
        <Icon className="w-4 h-4 text-indigo-400" />
        <span className="text-xs font-medium text-slate-200 whitespace-nowrap">{label}</span>
      </div>
      <span className="text-[10px] text-slate-500 text-center max-w-[110px] leading-tight">{desc}</span>
    </div>
  );
}

function PipelinePillCompact({ icon: Icon, label, desc }: { icon: React.FC<{ className?: string }>; label: string; desc: string }) {
  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-indigo-500/15 bg-white/[0.03] hover:bg-white/[0.06] transition-all">
      <Icon className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
      <span className="text-[11px] font-medium text-slate-300 whitespace-nowrap">{label}</span>
      <span className="text-[9px] text-slate-600 hidden xl:inline">— {desc}</span>
    </div>
  );
}

function PipelineConnector({ delay = 0 }: { delay?: number }) {
  return (
    <div className="flex items-center px-0.5 self-start mt-3">
      <div className="relative w-6 lg:w-10 h-5 flex items-center">
        <div className="w-full h-px bg-gradient-to-r from-indigo-500/40 to-indigo-500/15" />
        <div
          className="absolute top-1/2 -translate-y-1/2 w-1.5 h-1.5 rounded-full bg-cyan-400 shadow-[0_0_6px_#22d3ee] animate-travel-dot"
          style={{ animationDelay: `${delay}s` }}
        />
      </div>
      <ArrowRight className="w-3 h-3 text-indigo-500/30 -ml-0.5 shrink-0" />
    </div>
  );
}

function HowItWorksSection() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      viewport={{ once: true }}
      className="max-w-7xl mx-auto px-4 sm:px-6 py-24"
    >
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-4">Under the Hood</h2>
        <p className="text-lg text-slate-400 max-w-xl mx-auto">A production-grade AI pipeline, not a toy chatbot</p>
      </div>

      {/* Desktop pipeline */}
      <div className="hidden lg:flex items-start justify-center gap-0.5 overflow-x-auto pb-4 px-2">
        <PipelinePill icon={FileText} label="Your Idea" desc="Plain-text startup concept" />
        <PipelineConnector delay={0} />
        <PipelinePill icon={Zap} label="Validation Service" desc="FastAPI orchestration" />
        <PipelineConnector delay={0.5} />
        <PipelinePill icon={Brain} label="Validator Agent" desc="Core reasoning agent" />
        <PipelineConnector delay={1.0} />
        <div className="flex flex-col gap-1.5 rounded-2xl border border-dashed border-indigo-500/20 p-3 bg-white/[0.02] shrink-0">
          <span className="text-[8px] uppercase tracking-[0.2em] text-indigo-400/50 text-center font-medium">Parallel Tools</span>
          <PipelinePillCompact icon={Search} label="Web Search" desc="Live market signals" />
          <PipelinePillCompact icon={Users} label="Competitor Finder" desc="Who already exists" />
          <PipelinePillCompact icon={TrendingUp} label="Market Estimator" desc="TAM & growth rate" />
        </div>
        <PipelineConnector delay={1.5} />
        <PipelinePill icon={Sparkles} label="LLM Synthesis" desc="Claude/GPT reasoning" />
        <PipelineConnector delay={2.0} />
        <PipelinePill icon={FileText} label="Structured Report" desc="Score + insights JSON" />
      </div>

      {/* Mobile pipeline */}
      <div className="flex lg:hidden flex-col items-center gap-2 max-w-sm mx-auto">
        {ARCH_NODES.map((node, i) => (
          <Fragment key={node.label}>
            <div className="flex items-center gap-3 w-full px-4 py-2.5 rounded-xl border border-indigo-500/15 bg-white/[0.03]">
              <node.icon className="w-4 h-4 text-indigo-400 shrink-0" />
              <div className="flex flex-col min-w-0">
                <span className="text-sm font-medium text-slate-200">{node.label}</span>
                <span className="text-[10px] text-slate-500">{node.desc}</span>
              </div>
            </div>
            {i < ARCH_NODES.length - 1 && <ChevronDown className="w-4 h-4 text-indigo-500/30" />}
          </Fragment>
        ))}
      </div>
    </motion.div>
  );
}

/* ═══════════════ FEATURES GRID ═══════════════ */

function FeaturesSection() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      viewport={{ once: true }}
      className="max-w-6xl mx-auto px-4 sm:px-6 py-24"
    >
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-4">Everything You Need</h2>
        <p className="text-lg text-slate-400 max-w-xl mx-auto">
          A full-stack validation engine, not another ChatGPT wrapper
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {FEATURES.map((f) => (
          <div
            key={f.title}
            className="glass-card feature-glow p-6 group hover:border-indigo-500/40 transition-all duration-300"
          >
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 flex items-center justify-center mb-4 group-hover:bg-indigo-500/20 transition-colors">
              <f.icon className="w-5 h-5 text-indigo-400" />
            </div>
            <h3 className="text-base font-semibold text-slate-100 mb-2">{f.title}</h3>
            <p className="text-sm text-slate-400 leading-relaxed">{f.desc}</p>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

/* ═══════════════ CTA FOOTER ═══════════════ */

function CTAFooter({ onValidateClick }: { onValidateClick: () => void }) {
  return (
    <footer className="relative py-24 px-4">
      <div className="absolute inset-0 bg-gradient-to-t from-[#050510] to-transparent pointer-events-none" />
      <div className="relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="max-w-3xl mx-auto text-center space-y-8"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white">
            Stop guessing. Start validating.
          </h2>
          <p className="text-lg text-slate-400">
            Built on a production MCP architecture. Powered by the world&apos;s best LLMs.
          </p>
          <Button
            size="lg"
            onClick={onValidateClick}
            className="gap-2 text-base px-10 h-14 bg-gradient-to-r from-indigo-500 to-cyan-500 hover:shadow-xl hover:shadow-indigo-500/25"
          >
            Validate Your First Idea — It&apos;s Free <ArrowRight className="w-5 h-5" />
          </Button>
        </motion.div>

        <div className="mt-24 pt-8 border-t border-white/[0.06] max-w-4xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-center md:text-left">
          <span className="text-lg font-bold gradient-text select-none">IdeaProof</span>
          <span className="text-xs text-slate-600">Built with FastAPI + Claude + Vector DB</span>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-slate-600 hover:text-slate-400 transition-colors"
          >
            <Github className="w-5 h-5" />
          </a>
        </div>
      </div>
    </footer>
  );
}

/* ═══════════════════════════════════════════════════
   MAIN APP
   ═══════════════════════════════════════════════════ */

export default function App() {
  const [idea, setIdea] = useState('');
  const [results, setResults] = useState<ValidationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [health, setHealth] = useState<'checking' | 'online' | 'offline'>('checking');
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [historyOpen, setHistoryOpen] = useState(false);
  const [toasts, setToasts] = useState<ToastData[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [pipelineStep, setPipelineStep] = useState(-1);
  const [copied, setCopied] = useState(false);

  const resultsRef = useRef<HTMLDivElement>(null);
  const validatorRef = useRef<HTMLElement>(null);
  const pipelineRef = useRef<HTMLElement>(null);
  const pipelineInterval = useRef<ReturnType<typeof setInterval> | null>(null);
  const shaderCanvasRef = useShaderBackground();

  /* ── Scroll helpers ── */
  const scrollToValidator = useCallback(() => {
    validatorRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  const scrollToPipeline = useCallback(() => {
    pipelineRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  /* ── Toast helpers ── */
  const addToast = useCallback((message: string, type: ToastData['type'] = 'info') => {
    const id = Date.now() + Math.random();
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => setToasts((prev) => prev.filter((t) => t.id !== id)), 5000);
  }, []);

  const dismissToast = useCallback((id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  /* ── Health check ── */
  useEffect(() => {
    const check = () =>
      fetch(`${API}/health`)
        .then((r) => r.json())
        .then((d: { status: string }) => setHealth(d.status === 'ok' ? 'online' : 'offline'))
        .catch(() => setHealth('offline'));
    check();
    const iv = setInterval(check, 30000);
    return () => clearInterval(iv);
  }, []);

  /* ── Keyboard shortcut: Ctrl/Cmd + Enter ── */
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('submit-btn')?.click();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  /* ── Submit ── */
  const handleSubmit = async () => {
    const trimmed = idea.trim();
    if (!trimmed || loading) return;

    setLoading(true);
    setResults(null);
    setShowResults(false);
    setPipelineStep(0);

    pipelineInterval.current = setInterval(() => {
      setPipelineStep((p) => (p < PIPELINE_STEPS.length - 1 ? p + 1 : p));
    }, 450);

    try {
      const res = await fetch(`${API}/validate-idea`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idea: trimmed }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error((body as { detail?: string }).detail || `Request failed (${res.status})`);
      }

      const data: ValidationResult = await res.json();
      setResults(data);
      setShowResults(true);

      setHistory((prev) =>
        [{ idea: trimmed.substring(0, 60), score: data.score, timestamp: new Date(), fullResults: data, fullIdea: trimmed }, ...prev].slice(0, 5),
      );

      addToast('Validation complete!', 'success');
      setTimeout(() => resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 150);
    } catch (err) {
      addToast(err instanceof Error ? err.message : 'Unknown error', 'error');
    } finally {
      if (pipelineInterval.current) clearInterval(pipelineInterval.current);
      setPipelineStep(-1);
      setLoading(false);
    }
  };

  const handleRetry = () => { if (idea.trim()) handleSubmit(); };
  const fillExample = () => setIdea(EXAMPLE_IDEA);

  const handleCopy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      addToast('Copied to clipboard', 'success');
      setTimeout(() => setCopied(false), 2000);
    } catch { addToast('Failed to copy', 'error'); }
  };

  const handleHistorySelect = (entry: HistoryEntry) => {
    setResults(entry.fullResults);
    setShowResults(true);
    setIdea(entry.fullIdea);
    setHistoryOpen(false);
    setTimeout(() => resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
  };

  const scoreColor = (s: number) =>
    s >= 7 ? 'bg-emerald-500/20 text-emerald-400' : s >= 4 ? 'bg-amber-500/20 text-amber-400' : 'bg-red-500/20 text-red-400';

  /* ════════════════ RENDER ════════════════ */

  return (
    <div className="min-h-screen bg-[#080810] text-slate-100 relative overflow-x-hidden font-sans">
      {/* ── Fixed shader background ── */}
      <canvas ref={shaderCanvasRef} className="fixed inset-0 w-full h-full z-0 touch-none" style={{ background: 'black' }} />
      <div className="dot-grid fixed inset-0 pointer-events-none z-[1] opacity-30" />

      {/* ── Toasts ── */}
      <ToastContainer toasts={toasts} onDismiss={dismissToast} onRetry={loading ? undefined : handleRetry} />

      {/* ── Main content ── */}
      <div className="relative z-10">

        {/* ═══════════ S1: HERO ═══════════ */}
        <section className="relative min-h-screen flex items-center justify-center">
          <Hero health={health} onValidateClick={scrollToValidator} onHowItWorksClick={scrollToPipeline} />
        </section>

        <GradientDivider />

        {/* ═══════════ S2: SOCIAL PROOF ═══════════ */}
        <SocialProofBar />

        <GradientDivider />

        {/* ═══════════ S3: HOW IT WORKS ═══════════ */}
        <section id="how-it-works" ref={pipelineRef} className="relative">
          <div className="absolute inset-0 bg-[#080810]/70 pointer-events-none" />
          <div className="relative z-10">
            <HowItWorksSection />
          </div>
        </section>

        <GradientDivider />

        {/* ═══════════ S4: FEATURES ═══════════ */}
        <section className="relative">
          <FeaturesSection />
        </section>

        <GradientDivider />

        {/* ═══════════ S5: LIVE VALIDATOR ═══════════ */}
        <section id="validator" ref={validatorRef} className="relative py-20 md:py-28 px-4 sm:px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-14"
          >
            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-4">Try It Now</h2>
            <p className="text-lg text-slate-400 max-w-lg mx-auto">
              Paste your idea below. Results in under 30 seconds.
            </p>
          </motion.div>

          {/* ── Form ── */}
          <div className="max-w-2xl mx-auto space-y-5">
            <div className="relative">
              <textarea
                value={idea}
                onChange={(e) => setIdea(e.target.value)}
                placeholder="Describe your startup idea in plain English… e.g. An AI app that summarizes long PDFs for students in 3 bullet points"
                rows={5}
                className="w-full bg-[#0a1024]/85 backdrop-blur-md border border-indigo-300/35 rounded-2xl p-5 pr-16 text-slate-100 placeholder-slate-400 resize-none focus:outline-none focus:border-indigo-300/60 focus:ring-1 focus:ring-indigo-300/30 transition-all text-[15px] leading-relaxed shadow-[inset_0_0_0_1px_rgba(255,255,255,0.03)]"
              />
              <div className="absolute bottom-3.5 right-4 text-xs font-mono tabular-nums select-none">
                <span className={idea.length > 500 ? 'text-amber-300' : 'text-slate-300'}>{idea.length}</span>
                <span className="text-slate-400">/500</span>
              </div>
            </div>

            <div className="flex flex-wrap items-center justify-center gap-3">
              <button
                id="submit-btn"
                onClick={handleSubmit}
                disabled={loading || !idea.trim()}
                className="btn-shimmer inline-flex items-center gap-2.5 px-7 py-3 rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-500 text-white font-semibold text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-indigo-500/25 active:scale-[0.98] transition-all"
              >
                {loading ? (
                  <><Loader2 className="w-4 h-4 animate-spin" /> Validating…</>
                ) : (
                  <><Send className="w-4 h-4" /> Validate Idea <ArrowRight className="w-4 h-4" /></>
                )}
              </button>
              <button
                onClick={fillExample}
                className="inline-flex items-center gap-2 px-5 py-3 rounded-xl border border-white/15 bg-white/[0.04] text-slate-300 text-sm font-medium hover:bg-white/[0.08] hover:text-white hover:border-white/25 transition-all"
              >
                <Lightbulb className="w-4 h-4" /> Try an Example
              </button>
            </div>

            <p className="text-[11px] text-slate-500 text-center flex items-center justify-center gap-1.5">
              Press <kbd>⌘</kbd><span className="text-slate-600">/</span><kbd>Ctrl</kbd> + <kbd>Enter</kbd> to submit
            </p>

            {loading && (
              <div className="mt-6 w-full animate-fade-in">
                <p className="text-[11px] uppercase tracking-[0.25em] text-slate-500 text-center mb-4 font-medium">MCP Orchestration Pipeline</p>
                <MCPLoadingPipeline step={pipelineStep} />
              </div>
            )}
          </div>

          {/* ── Results ── */}
          {(loading || showResults) && (
            <div ref={resultsRef} className="max-w-5xl mx-auto mt-16">
              {loading && !results ? (
                <ResultsSkeleton />
              ) : (
                results && (
                  <div className="space-y-6">
                    <div className="glass-card p-8 sm:p-10 flex justify-center stagger-reveal" style={{ animationDelay: '0ms' }}>
                      <ScoreGauge score={results.score} />
                    </div>

                    <div className="glass-card p-6 sm:p-8 border-l-2 border-l-cyan-500/50 stagger-reveal" style={{ animationDelay: '100ms' }}>
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="text-xs uppercase tracking-[0.2em] text-cyan-400 font-semibold">Executive Summary</h3>
                        <button onClick={() => handleCopy(results.summary)} className="flex items-center gap-1.5 text-[11px] text-slate-500 hover:text-slate-300 transition-colors">
                          {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                          {copied ? 'Copied' : 'Copy'}
                        </button>
                      </div>
                      <p className="text-slate-300 leading-relaxed text-[15px]">{results.summary}</p>
                    </div>

                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="glass-card p-6 stagger-reveal" style={{ animationDelay: '200ms' }}>
                        <h3 className="text-xs uppercase tracking-[0.2em] text-emerald-400 font-semibold mb-4 flex items-center gap-2">
                          <CheckCircle2 className="w-4 h-4" /> Strengths
                        </h3>
                        <div className="flex flex-wrap gap-2">
                          {results.strengths.length > 0 ? results.strengths.map((s, i) => (
                            <span key={i} className="stagger-reveal inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-sm" style={{ animationDelay: `${300 + i * 80}ms` }}>
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500/70" />{s}
                            </span>
                          )) : <span className="text-sm text-slate-600 italic">None identified</span>}
                        </div>
                      </div>
                      <div className="glass-card p-6 stagger-reveal" style={{ animationDelay: '300ms' }}>
                        <h3 className="text-xs uppercase tracking-[0.2em] text-amber-400 font-semibold mb-4 flex items-center gap-2">
                          <AlertTriangle className="w-4 h-4" /> Risks
                        </h3>
                        <div className="flex flex-wrap gap-2">
                          {results.risks.length > 0 ? results.risks.map((r, i) => (
                            <span key={i} className="stagger-reveal inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300 text-sm" style={{ animationDelay: `${400 + i * 80}ms` }}>
                              <AlertTriangle className="w-3.5 h-3.5 text-amber-500/70" />{r}
                            </span>
                          )) : <span className="text-sm text-slate-600 italic">None identified</span>}
                        </div>
                      </div>
                    </div>

                    {results.competitors.length > 0 && (
                      <div className="glass-card p-6 stagger-reveal" style={{ animationDelay: '400ms' }}>
                        <h3 className="text-xs uppercase tracking-[0.2em] text-indigo-400 font-semibold mb-4 flex items-center gap-2">
                          <Users className="w-4 h-4" /> Competitors
                        </h3>
                        <div className="flex gap-3 overflow-x-auto pb-2">
                          {results.competitors.map((c, i) => <CompetitorCard key={i} name={c} index={i} />)}
                        </div>
                      </div>
                    )}

                    {results.market_notes && (
                      <div className="glass-card p-6 stagger-reveal" style={{ animationDelay: '500ms' }}>
                        <h3 className="text-xs uppercase tracking-[0.2em] text-indigo-400 font-semibold mb-3 flex items-center gap-2">
                          <BarChart3 className="w-4 h-4" /> Market Intelligence
                        </h3>
                        <div className="bg-[#080810]/60 rounded-xl p-5 border border-white/[0.06]">
                          <p className="text-sm text-slate-300 font-mono leading-relaxed">{results.market_notes}</p>
                        </div>
                      </div>
                    )}

                    <div className="glass-card p-6 stagger-reveal" style={{ animationDelay: '600ms' }}>
                      <h3 className="text-xs uppercase tracking-[0.2em] text-slate-500 font-semibold mb-4 flex items-center gap-2">
                        <Activity className="w-4 h-4" /> MCP Orchestration Flow
                      </h3>
                      <MCPLoadingPipeline step={PIPELINE_STEPS.length} />
                    </div>
                  </div>
                )
              )}
            </div>
          )}
        </section>

        {/* ═══════════ S6: VALIDATION HISTORY ═══════════ */}
        {history.length > 0 && (
          <section className="max-w-5xl mx-auto px-4 sm:px-6 pb-12">
            <GradientDivider />
            <div className="py-8 flex flex-col items-center">
              <button
                onClick={() => setHistoryOpen((v) => !v)}
                className="flex items-center gap-2.5 px-5 py-2.5 rounded-xl bg-surface/60 backdrop-blur-sm border border-indigo-500/15 text-xs text-slate-400 hover:text-slate-200 transition-colors"
              >
                <Clock className="w-3.5 h-3.5" />
                Recent Validations ({history.length})
                {historyOpen ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
              </button>
              {historyOpen && (
                <div className="mt-4 flex gap-3 overflow-x-auto pb-2 w-full justify-center">
                  {history.map((h, i) => (
                    <button
                      key={i}
                      onClick={() => handleHistorySelect(h)}
                      className="shrink-0 flex items-center gap-3 px-4 py-2.5 rounded-lg border border-white/[0.06] bg-white/[0.02] hover:bg-white/[0.05] hover:border-indigo-500/30 transition-all text-left"
                    >
                      <div className="flex flex-col gap-1 min-w-0">
                        <span className="text-xs text-slate-300 truncate max-w-[200px]">{h.idea}{h.fullIdea.length > 60 ? '…' : ''}</span>
                        <span className="text-[10px] text-slate-600">{h.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                      </div>
                      <span className={`text-xs font-mono font-bold px-2 py-0.5 rounded-md shrink-0 ${scoreColor(h.score)}`}>{h.score.toFixed(1)}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </section>
        )}

        <GradientDivider />

        {/* ═══════════ S7: CTA FOOTER ═══════════ */}
        <CTAFooter onValidateClick={scrollToValidator} />
      </div>
    </div>
  );
}
