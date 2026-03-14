import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

interface HeroProps {
  health: "checking" | "online" | "offline";
  onValidateClick: () => void;
  onHowItWorksClick: () => void;
}

function Hero({ health, onValidateClick, onHowItWorksClick }: HeroProps) {
  const [titleNumber, setTitleNumber] = useState(0);
  const titles = useMemo(
    () => ["validated", "stress-tested", "market-ready", "de-risked", "proven"],
    []
  );

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (titleNumber === titles.length - 1) {
        setTitleNumber(0);
      } else {
        setTitleNumber(titleNumber + 1);
      }
    }, 2000);
    return () => clearTimeout(timeoutId);
  }, [titleNumber, titles]);

  return (
    <div className="w-full">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex gap-8 py-20 lg:py-40 items-center justify-center flex-col">
          {/* API status badge */}
          <div className="flex items-center gap-2.5 px-4 py-1.5 rounded-full border border-indigo-500/20 bg-indigo-500/10 backdrop-blur-sm">
            <span className="relative flex h-2 w-2">
              {health === "online" && (
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-50" />
              )}
              <span
                className={`relative inline-flex rounded-full h-2 w-2 ${
                  health === "online"
                    ? "bg-emerald-400"
                    : health === "offline"
                      ? "bg-red-400"
                      : "bg-slate-500 animate-pulse"
                }`}
              />
            </span>
            <span className="text-xs font-medium text-slate-300">
              {health === "online"
                ? "API Online"
                : health === "offline"
                  ? "API Offline"
                  : "Checking…"}
            </span>
          </div>

          <div className="flex gap-4 flex-col">
            <h1 className="text-5xl md:text-7xl max-w-2xl tracking-tighter text-center font-normal">
              <span className="text-slate-100">Your startup idea,</span>
              <span className="relative flex w-full justify-center overflow-hidden text-center md:pb-4 md:pt-1">
                &nbsp;
                {titles.map((title, index) => (
                  <motion.span
                    key={index}
                    className="absolute font-semibold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent"
                    initial={{ opacity: 0, y: "-100" }}
                    transition={{ type: "spring", stiffness: 50 }}
                    animate={
                      titleNumber === index
                        ? { y: 0, opacity: 1 }
                        : {
                            y: titleNumber > index ? -150 : 150,
                            opacity: 0,
                          }
                    }
                  >
                    {title}
                  </motion.span>
                ))}
              </span>
            </h1>

            <p className="text-lg md:text-xl leading-relaxed tracking-tight text-slate-400 max-w-2xl text-center">
              Most founders waste months building the wrong thing. IdeaProof
              analyzes your idea in seconds — competitors, market size, risks,
              and a viability score. Know before you build.
            </p>
          </div>

          <div className="flex flex-row gap-3">
            <Button
              size="lg"
              variant="outline"
              onClick={onHowItWorksClick}
              className="border-white/20 bg-white/[0.04] text-slate-300 hover:bg-white/[0.08] hover:text-white hover:border-white/30"
            >
              See How It Works
            </Button>
            <Button
              size="lg"
              onClick={onValidateClick}
              className="gap-2 bg-gradient-to-r from-indigo-500 to-cyan-500 hover:shadow-lg hover:shadow-indigo-500/25"
            >
              Validate My Idea <ArrowRight className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

export { Hero };
