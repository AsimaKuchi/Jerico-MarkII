import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  FileText,
  ArrowRight,
  CheckCircle,
  Shield,
  Brain,
  Clock,
  Lock,
  Users,
  XCircle,
  AlertTriangle,
  MapPin,
} from "lucide-react";

// REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
const handleGoogleLogin = () => {
  const redirectUrl = window.location.origin + "/dashboard";
  window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
};

const HERO_IMG = "https://images.unsplash.com/photo-1531591022136-eb8b0da1e6d0?auto=format&fit=crop&w=1200&q=80";

export default function LandingPage() {
  const navigate = useNavigate();

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Matching (With Explanations)",
      description:
        "We scan real job boards and evaluate roles based on your target role, experience level, location preferences, industry fit, and application intensity.",
      highlight: "If a job is skipped, we tell you why.",
    },
    {
      icon: FileText,
      title: "Tailored Applications — Before You Apply",
      description:
        "Every application is customized: job-specific résumé, role-aligned cover letter, and clear match reasoning. You review everything before submission.",
      highlight: "No surprises. No generic filler.",
    },
    {
      icon: Clock,
      title: "Automation Where It Helps — Control Where It Matters",
      description:
        "We handle job discovery, form prep, and document tailoring. You handle final review, approval, and submission decision.",
      highlight: "This saves time without sacrificing quality.",
    },
    {
      icon: Lock,
      title: "Privacy-First by Design",
      description:
        "Nothing is submitted without your approval. No résumé spraying. No impersonation. No black-box automation.",
      highlight: "Your profile represents you — not a bot.",
    },
  ];

  const trustBadges = [
    { icon: Shield, label: "256-bit SSL Encryption" },
    { icon: MapPin, label: "PIPEDA-Compliant" },
    { icon: Users, label: "Human-in-the-Loop System" },
    { icon: XCircle, label: "No Blind Auto-Apply" },
  ];

  const skipReasons = [
    "Skip low-fit roles",
    "Flag stretch opportunities",
    "Explain risk vs reward",
    "Let you decide when to proceed",
  ];

  const reviews = [
    {
      id: "review-1",
      quote:
        "I went from spending 3 hours daily on applications to just 15 minutes. Landed 4 interviews in my first week!",
      name: "Sarah Chen",
      role: "Software Developer • Toronto, ON",
    },
    {
      id: "review-2",
      quote:
        "The AI matching is incredible. Every job suggestion was spot-on for my experience level and career goals.",
      name: "Marcus Miller",
      role: "Marketing Manager • Ottawa, ON",
    },
    {
      id: "review-3",
      quote:
        "As a new immigrant, this tool was a lifesaver. It understood the Canadian job market perfectly.",
      name: "Priya Sharma",
      role: "Data Analyst • Mississauga, ON",
    },
  ];

  return (
    <div className="min-h-screen bg-background" data-testid="landing-page">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-background border-b border-border">
        <nav className="max-w-6xl mx-auto flex items-center justify-between px-6 h-20">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-foreground flex items-center justify-center">
              <span className="font-mono font-bold text-background text-lg">J</span>
            </div>
            <span className="text-2xl font-serif font-bold text-foreground">JobMatch AI</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => navigate("/how-it-works")}
              className="hidden sm:inline-flex font-mono text-xs uppercase tracking-widest text-muted-foreground hover:text-foreground px-4 py-2 transition-colors"
            >
              How It Works
            </button>
            <Button
              data-testid="header-signin-btn"
              onClick={handleGoogleLogin}
              className="rounded-none bg-primary text-primary-foreground hover:bg-foreground hover:text-background font-mono text-xs uppercase tracking-widest px-6"
            >
              Sign In
            </Button>
          </div>
        </nav>
      </header>

      {/* Hero — asymmetric */}
      <main>
        <section className="max-w-6xl mx-auto px-6 grid lg:grid-cols-[1.1fr_0.9fr] gap-12 lg:gap-8 items-center pt-16 lg:pt-24 pb-20">
          <div className="animate-fade-in">
            <p className="micro-label text-muted-foreground mb-6">// Quality-First Job Applications</p>
            <h1 className="text-5xl md:text-7xl font-serif font-bold leading-[0.95] tracking-tight text-foreground">
              Apply to the right jobs —{" "}
              <span className="italic text-foreground relative">
                not every job
                <span className="absolute left-0 -bottom-2 w-full h-1 bg-primary" />
              </span>
            </h1>
            <p className="mt-8 text-base md:text-lg text-muted-foreground max-w-xl leading-relaxed">
              A quality-first job application platform that finds strong matches, explains why they fit,
              and lets you approve every application before it&apos;s sent.
            </p>
            <p className="mt-4 font-mono text-sm text-foreground">
              No resume spam. No blind auto-apply. No burned opportunities.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center pt-10">
              <Button
                data-testid="get-started-btn"
                onClick={handleGoogleLogin}
                className="group rounded-none bg-primary text-primary-foreground hover:bg-foreground hover:text-background font-mono text-xs uppercase tracking-widest h-14 px-8"
              >
                Find jobs that actually fit me
                <ArrowRight className="w-4 h-4 ml-3 group-hover:translate-x-1 transition-transform" />
              </Button>
              <button
                data-testid="learn-more-btn"
                onClick={() => navigate("/how-it-works")}
                className="font-mono text-xs uppercase tracking-widest text-foreground underline underline-offset-8 decoration-1 hover:decoration-primary h-14"
              >
                See how it works →
              </button>
            </div>
          </div>

          {/* Right visual: layered image + stat card */}
          <div className="relative hidden lg:block animate-fade-in-delay-1">
            <div className="border border-foreground overflow-hidden">
              <img
                src={HERO_IMG}
                alt="Editorial abstract architecture"
                className="w-full h-[440px] object-cover grayscale contrast-110"
              />
            </div>
            <div className="absolute -bottom-6 -left-6 bg-background border border-foreground p-6 w-52 editorial-offset-lime">
              <p className="text-5xl font-serif font-bold text-foreground leading-none">87%</p>
              <p className="micro-label text-muted-foreground mt-3">Match precision on approved roles</p>
            </div>
          </div>
        </section>

        {/* Credibility metrics — asymmetric strip */}
        <section className="border-y border-border bg-muted/40">
          <div className="max-w-6xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 divide-x divide-border">
            {[
              { n: "2,800+", l: "users reviewing applications before applying" },
              { n: "45,000+", l: "applications reviewed — not blindly sent" },
              { n: "100%", l: "human-approved applications only" },
              { n: "CA", l: "Ontario + Canada-focused job discovery" },
            ].map((m, i) => (
              <div key={i} className="px-6 py-10">
                <p className="text-4xl font-serif font-bold text-foreground">{m.n}</p>
                <p className="text-sm text-muted-foreground mt-2 leading-snug">{m.l}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Why quality-first */}
        <section id="how-it-works" className="max-w-6xl mx-auto px-6 py-24">
          <div className="max-w-2xl mb-16">
            <p className="micro-label text-muted-foreground mb-4">// The approach</p>
            <h2 className="text-4xl md:text-5xl font-serif font-semibold text-foreground leading-tight">
              Why choose a quality-first approach?
            </h2>
            <p className="mt-5 text-base md:text-lg text-muted-foreground">
              Most job tools optimize for volume.{" "}
              <span className="text-foreground font-semibold">We optimize for interviews.</span>
            </p>
          </div>

          <div className="grid md:grid-cols-2 border-t border-l border-border">
            {features.map((feature, i) => (
              <div
                key={i}
                data-testid={`feature-card-${i}`}
                className="group border-b border-r border-border p-8 md:p-10 hover:bg-muted/40 transition-colors"
              >
                <div className="flex items-center justify-between mb-8">
                  <div className="w-12 h-12 border border-foreground flex items-center justify-center text-foreground group-hover:bg-primary group-hover:border-primary transition-colors">
                    <feature.icon className="w-6 h-6" />
                  </div>
                  <span className="font-mono text-xs text-muted-foreground">0{i + 1}</span>
                </div>
                <h3 className="text-2xl font-serif font-semibold text-foreground">{feature.title}</h3>
                <p className="mt-4 text-muted-foreground leading-relaxed">{feature.description}</p>
                <p className="mt-6 pt-4 border-t border-border font-mono text-xs uppercase tracking-wider text-foreground">
                  {feature.highlight}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Testimonials */}
        <section className="max-w-6xl mx-auto px-6 py-24 border-t border-border">
          <div className="max-w-2xl mb-16">
            <p className="micro-label text-muted-foreground mb-4">// Field notes</p>
            <h2 className="text-4xl md:text-5xl font-serif font-semibold text-foreground leading-tight">
              What our users are saying
            </h2>
            <p className="mt-5 text-base md:text-lg text-muted-foreground">
              Real results from real job seekers across Canada
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {reviews.map((r) => (
              <div key={r.id} data-testid={r.id} className="border border-border p-8 hover:border-foreground transition-colors">
                <p className="font-mono text-primary-foreground bg-foreground inline-block px-2 py-1 text-xs">★★★★★</p>
                <p className="mt-6 text-lg font-serif italic text-foreground leading-relaxed">
                  &ldquo;{r.quote}&rdquo;
                </p>
                <div className="pt-6 mt-6 border-t border-border">
                  <p className="font-semibold text-foreground">{r.name}</p>
                  <p className="text-sm text-muted-foreground font-mono mt-1">{r.role}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Why we skip jobs */}
        <section className="max-w-6xl mx-auto px-6 py-12">
          <div className="border border-foreground bg-foreground text-background p-10 md:p-14">
            <div className="flex items-start gap-5 mb-8">
              <div className="w-12 h-12 border border-primary flex items-center justify-center text-primary shrink-0">
                <AlertTriangle className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-3xl md:text-4xl font-serif font-semibold text-background leading-tight">
                  Why we skip jobs on purpose
                </h2>
                <p className="mt-3 text-sidebar-muted">
                  Applying to the wrong job can hurt your chances at a company forever.
                </p>
              </div>
            </div>
            <p className="font-mono text-xs uppercase tracking-widest text-primary mb-6">That&apos;s why we:</p>
            <div className="grid sm:grid-cols-2 gap-px bg-sidebar-border border border-sidebar-border mb-10">
              {skipReasons.map((reason, i) => (
                <div key={i} className="flex items-center gap-3 p-5 bg-foreground">
                  <CheckCircle className="w-5 h-5 text-primary shrink-0" />
                  <span className="text-background">{reason}</span>
                </div>
              ))}
            </div>
            <p className="text-2xl font-serif text-background text-center">
              Skipping is not failure — it&apos;s strategy.
            </p>
          </div>
        </section>

        {/* Trust badges */}
        <section className="max-w-6xl mx-auto px-6 py-20">
          <div className="grid grid-cols-2 md:grid-cols-4 border-t border-l border-border">
            {trustBadges.map((badge, i) => (
              <div key={i} className="flex flex-col items-start gap-3 p-8 border-b border-r border-border">
                <badge.icon className="w-6 h-6 text-foreground" />
                <p className="text-sm font-medium text-foreground">{badge.label}</p>
              </div>
            ))}
          </div>
          <p className="text-sm text-muted-foreground mt-6 font-mono">
            Built for candidates who care about long-term career outcomes.
          </p>
        </section>

        {/* Final CTA */}
        <section className="max-w-6xl mx-auto px-6 pb-24">
          <div className="border border-foreground p-12 md:p-16 grid lg:grid-cols-[1fr_auto] gap-10 items-center">
            <div>
              <h2 className="text-4xl md:text-6xl font-serif font-bold text-foreground leading-[0.95]">
                Stop applying blindly.
                <br />
                <span className="italic">Start applying intentionally.</span>
              </h2>
              <p className="mt-6 text-base md:text-lg text-muted-foreground max-w-xl">
                Review fewer jobs. Send better applications. Get more interviews.
              </p>
            </div>
            <Button
              data-testid="cta-get-started-btn"
              onClick={handleGoogleLogin}
              className="rounded-none bg-primary text-primary-foreground hover:bg-foreground hover:text-background font-mono text-xs uppercase tracking-widest h-16 px-10"
            >
              Find jobs that fit me
              <ArrowRight className="w-4 h-4 ml-3" />
            </Button>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border">
        <div className="max-w-6xl mx-auto px-6 py-10 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-foreground flex items-center justify-center">
              <span className="font-mono font-bold text-background text-sm">J</span>
            </div>
            <span className="text-sm text-muted-foreground font-mono">© 2025 JobMatch AI</span>
          </div>
          <div className="flex items-center gap-8">
            <a href="#" className="font-mono text-xs uppercase tracking-widest text-muted-foreground hover:text-foreground transition-colors">Privacy</a>
            <a href="#" className="font-mono text-xs uppercase tracking-widest text-muted-foreground hover:text-foreground transition-colors">Terms</a>
            <a href="#" className="font-mono text-xs uppercase tracking-widest text-muted-foreground hover:text-foreground transition-colors">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
