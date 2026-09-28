import { Button } from "@/components/ui/button";
import {
  User,
  Search,
  Eye,
  Send,
  BarChart3,
  ArrowRight,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Target,
  Edit,
  Bookmark,
  FileCheck,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

// REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
const handleGoogleLogin = () => {
  const redirectUrl = window.location.origin + "/dashboard";
  window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
};

export default function HowItWorks() {
  const navigate = useNavigate();

  const steps = [
    {
      number: "01",
      icon: User,
      title: "Build Your Profile",
      subtitle: "Tell us what good looks like for you.",
      description: "Upload your resume and set your preferences so we understand:",
      points: [
        "Your target roles and experience level",
        "Preferred locations (Toronto, GTA, Ontario, Remote, etc.)",
        "Industries you want to focus on",
        "Work authorization and work arrangement preferences",
      ],
      highlight: "Your profile guides every recommendation — nothing is guessed.",
    },
    {
      number: "02",
      icon: Search,
      title: "Job Matching (With Explanations)",
      subtitle: "We don't apply everywhere. We match carefully.",
      description: "Our system scans supported job boards (starting with Greenhouse) and evaluates roles based on:",
      points: [
        "Role relevance",
        "Experience fit",
        "Location alignment",
        "Industry match",
        "Your application intensity (conservative → ambitious)",
      ],
      extras: [
        { icon: CheckCircle, text: "Jobs we recommend" },
        { icon: XCircle, text: "Jobs we skip — and why" },
        { icon: Target, text: "Clear reasoning behind every match" },
      ],
      extrasLabel: "You'll see:",
      highlight: "Skipping is intentional. It protects your long-term chances.",
    },
    {
      number: "03",
      icon: Eye,
      title: "Review Before Applying",
      subtitle: "Nothing is submitted without your approval.",
      description: "For each recommended role, we prepare:",
      points: [
        "A tailored resume version",
        "A role-specific cover letter",
        "A preview of the application flow",
      ],
      extras: [
        { icon: CheckCircle, text: "Approve" },
        { icon: Edit, text: "Edit" },
        { icon: XCircle, text: "Skip" },
        { icon: Bookmark, text: "Save for later" },
      ],
      extrasLabel: "You choose what to:",
      highlight: "This keeps quality high and avoids résumé spam.",
    },
    {
      number: "04",
      icon: Send,
      title: "Apply With Confidence",
      subtitle: "When you approve, we handle the technical steps — not the decisions.",
      description: "We assist with:",
      points: [
        "Form filling on supported platforms",
        "Uploading the correct documents",
        "Ensuring applications are submitted correctly",
      ],
      extras: [
        { icon: FileCheck, text: "Where you applied" },
        { icon: FileCheck, text: "What was sent" },
        { icon: FileCheck, text: "When it was submitted" },
      ],
      extrasLabel: "You always know:",
      highlight: "Everything is tracked in your dashboard.",
    },
    {
      number: "05",
      icon: BarChart3,
      title: "Track & Prepare",
      subtitle: "Applying is just the start.",
      description: "From your dashboard, you can:",
      points: [
        "Track application statuses",
        "See which roles are gaining traction",
        "Prepare for interviews with role-specific insights",
      ],
      highlight: "The goal isn't more applications — it's more interviews.",
    },
  ];

  const autoApplyProblems = [
    "Get you rejected faster",
    "Lock you out of companies",
    "Flood ATS systems with low-signal applications",
  ];

  return (
    <div className="min-h-screen bg-background" data-testid="how-it-works-page">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-background border-b border-border">
        <nav className="max-w-6xl mx-auto flex items-center justify-between px-6 h-20">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => navigate("/")}>
            <div className="w-9 h-9 bg-foreground flex items-center justify-center">
              <span className="font-mono font-bold text-background text-lg">J</span>
            </div>
            <span className="text-2xl font-serif font-bold text-foreground">JobMatch AI</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              data-testid="home-btn"
              onClick={() => navigate("/")}
              className="hidden sm:inline-flex font-mono text-xs uppercase tracking-widest text-muted-foreground hover:text-foreground px-4 py-2 transition-colors"
            >
              ← Back to Home
            </button>
            <Button
              data-testid="header-signin-btn"
              onClick={handleGoogleLogin}
              className="rounded-none bg-primary text-primary-foreground hover:bg-foreground hover:text-background font-mono text-xs uppercase tracking-widest px-6"
            >
              Get Started
            </Button>
          </div>
        </nav>
      </header>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 pt-20 pb-16 border-b border-border">
        <p className="micro-label text-muted-foreground mb-6">// How It Works</p>
        <h1 className="text-5xl md:text-7xl font-serif font-bold leading-[0.95] tracking-tight text-foreground max-w-4xl">
          A smarter way to apply —{" "}
          <span className="italic">without burning opportunities</span>
        </h1>
        <p className="mt-8 text-base md:text-lg text-muted-foreground max-w-2xl leading-relaxed">
          Our platform helps you find the right jobs, prepare high-quality applications, and apply
          with confidence — all with you in control.
        </p>
      </section>

      {/* Steps — editorial two-column */}
      <section className="max-w-6xl mx-auto px-6 py-16">
        <div className="space-y-0 border-t border-border">
          {steps.map((step, i) => (
            <div
              key={i}
              data-testid={`step-${i + 1}`}
              className="grid lg:grid-cols-[220px_1fr] gap-8 lg:gap-12 py-14 border-b border-border"
            >
              {/* Index column */}
              <div className="lg:sticky lg:top-28 self-start">
                <p className="text-6xl font-serif font-bold text-foreground/15">{step.number}</p>
                <div className="w-12 h-12 border border-foreground flex items-center justify-center text-foreground mt-4">
                  <step.icon className="w-6 h-6" />
                </div>
              </div>

              {/* Content column */}
              <div className="max-w-2xl">
                <h2 className="text-3xl md:text-4xl font-serif font-semibold text-foreground">{step.title}</h2>
                <p className="mt-2 text-lg text-muted-foreground">{step.subtitle}</p>
                <p className="mt-6 text-foreground">{step.description}</p>
                <ul className="mt-4 space-y-3">
                  {step.points.map((point, j) => (
                    <li key={j} className="flex items-start gap-3">
                      <span className="w-1.5 h-1.5 bg-primary mt-2.5 shrink-0" />
                      <span className="text-muted-foreground">{point}</span>
                    </li>
                  ))}
                </ul>

                {step.extras && (
                  <div className="mt-8 pt-6 border-t border-border">
                    <p className="micro-label text-muted-foreground mb-4">{step.extrasLabel}</p>
                    <div className="grid sm:grid-cols-3 border-t border-l border-border">
                      {step.extras.map((extra, j) => (
                        <div key={j} className="flex items-center gap-2 p-4 border-b border-r border-border">
                          <extra.icon className="w-4 h-4 text-foreground shrink-0" />
                          <span className="text-sm text-foreground">{extra.text}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <p className="mt-8 font-mono text-xs uppercase tracking-widest text-foreground border-l-2 border-primary pl-4 py-1">
                  {step.highlight}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Not auto-apply */}
      <section className="max-w-6xl mx-auto px-6 py-12">
        <div className="border border-foreground bg-foreground text-background p-10 md:p-14">
          <div className="flex items-start gap-5 mb-8">
            <div className="w-12 h-12 border border-primary flex items-center justify-center text-primary shrink-0">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-3xl md:text-4xl font-serif font-semibold text-background leading-tight">
                Why we&apos;re not &ldquo;auto-apply&rdquo;
              </h2>
              <p className="mt-3 text-sidebar-muted">
                Many tools optimize for volume.{" "}
                <span className="text-background font-semibold">We optimize for outcomes.</span>
              </p>
            </div>
          </div>
          <p className="font-mono text-xs uppercase tracking-widest text-primary mb-4">Auto-applying everywhere can:</p>
          <div className="space-y-px bg-sidebar-border border border-sidebar-border mb-8">
            {autoApplyProblems.map((problem, i) => (
              <div key={i} className="flex items-center gap-3 p-5 bg-foreground">
                <XCircle className="w-5 h-5 text-destructive shrink-0" />
                <span className="text-background">{problem}</span>
              </div>
            ))}
          </div>
          <p className="text-2xl font-serif text-background text-center pt-6 border-t border-sidebar-border">
            That&apos;s why every application here is <span className="text-primary italic">intentional</span>.
          </p>
        </div>
      </section>

      {/* Final CTA */}
      <section className="max-w-6xl mx-auto px-6 pb-24">
        <div className="border border-foreground p-12 md:p-16 text-center">
          <h2 className="text-4xl md:text-6xl font-serif font-bold text-foreground leading-[0.95]">
            Ready to apply smarter?
          </h2>
          <p className="mt-6 text-base md:text-lg text-muted-foreground max-w-xl mx-auto">
            Join thousands of candidates who care about quality over quantity.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-10">
            <Button
              data-testid="cta-get-started-btn"
              onClick={handleGoogleLogin}
              className="rounded-none bg-primary text-primary-foreground hover:bg-foreground hover:text-background font-mono text-xs uppercase tracking-widest h-14 px-10"
            >
              Find jobs that actually fit me
              <ArrowRight className="w-4 h-4 ml-3" />
            </Button>
            <Button
              variant="outline"
              onClick={() => navigate("/")}
              className="rounded-none border-foreground text-foreground hover:bg-foreground hover:text-background font-mono text-xs uppercase tracking-widest h-14 px-8"
            >
              Back to Home
            </Button>
          </div>
        </div>
      </section>

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
