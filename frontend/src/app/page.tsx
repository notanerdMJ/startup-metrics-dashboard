import Hero from "@/components/landing/Hero";
import Features from "@/components/landing/Features";
import HowItWorks from "@/components/landing/HowItWorks";
import CTA from "@/components/landing/CTA";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-dashboard-bg">
      <Hero />
      <Features />
      <HowItWorks />
      <CTA />
    </div>
  );
}