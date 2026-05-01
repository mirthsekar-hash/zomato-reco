"use client";

import { useState } from "react";
import { 
    MapPin, 
    ArrowRight, 
    Users, 
    Heart, 
    Briefcase, 
    Music, 
    Target,
    Compass
} from "lucide-react";
import { PreferenceRequest } from "@/lib/api";

interface PreferenceFormProps {
    onSubmit: (request: PreferenceRequest) => void;
    isLoading: boolean;
    locations: string[];
}

export default function PreferenceForm({ onSubmit, isLoading, locations }: PreferenceFormProps) {
    const [location, setLocation] = useState("");
    const [budget, setBudget] = useState("low");
    const [selectedCuisines, setSelectedCuisines] = useState<string[]>(["Italian", "Chinese"]);
    const [minRating, setMinRating] = useState(3.5);
    const [vibe, setVibe] = useState("Family-friendly");

    const cuisines = ["Italian", "North Indian", "Chinese", "Japanese", "Mediterranean", "French", "Mexican"];
    const vibes = [
        { id: "Family-friendly", icon: Users, label: "Family-friendly" },
        { id: "Romantic", icon: Heart, label: "Romantic" },
        { id: "Business", icon: Briefcase, label: "Business" },
        { id: "Nightlife", icon: Music, label: "Nightlife" },
    ];

    const toggleCuisine = (c: string) => {
        setSelectedCuisines(prev => 
            prev.includes(c) ? prev.filter(x => x !== c) : [...prev, c]
        );
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit({
            location,
            budget,
            cuisine: selectedCuisines.join(", "),
            minimum_rating: minRating,
            additional_preferences: vibe,
        });
    };

    return (
        <form onSubmit={handleSubmit} className="bg-white p-8 md:p-12 rounded-[2.5rem] shadow-premium max-w-5xl mx-auto space-y-12 animate-in fade-in slide-in-from-bottom-8 duration-700">
            {/* Top Row: Location and Budget */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                <div className="space-y-4">
                    <label className="text-[0.8rem] font-bold uppercase tracking-[0.1em] text-text-secondary flex items-center gap-2">
                        <MapPin size={16} /> Your Location
                    </label>
                    <div className="relative">
                        <select
                            required
                            value={location}
                            onChange={(e) => setLocation(e.target.value)}
                            className="w-full bg-[#F5F5F5] border-none rounded-2xl px-6 py-5 text-text-primary placeholder:text-text-muted focus:ring-2 focus:ring-reco-red transition-all appearance-none cursor-pointer"
                        >
                            <option value="" disabled>Select a location</option>
                            {locations.map((loc) => (
                                <option key={loc} value={loc}>{loc}</option>
                            ))}

                        </select>
                        <Compass className="absolute right-6 top-1/2 -translate-y-1/2 text-reco-red pointer-events-none" size={20} />
                    </div>
                </div>

                <div className="space-y-4">
                    <label className="text-[0.8rem] font-bold uppercase tracking-[0.1em] text-text-secondary flex items-center gap-2">
                        <Target size={16} /> Budget Range
                    </label>
                    <div className="flex bg-[#F5F5F5] rounded-2xl p-1.5 h-[64px]">
                        {['low', 'medium', 'high'].map((b) => (
                            <button
                                key={b}
                                type="button"
                                onClick={() => setBudget(b)}
                                className={`flex-1 rounded-xl text-sm font-bold capitalize transition-all ${budget === b ? 'bg-white text-text-primary shadow-sm' : 'text-text-muted hover:text-text-secondary'}`}
                            >
                                {b}
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            {/* Middle: Rating */}
            <div className="space-y-6">
                <div className="flex justify-between items-center">
                    <label className="text-[0.8rem] font-bold uppercase tracking-[0.1em] text-text-secondary">
                        Minimum Rating
                    </label>
                    <span className="text-2xl font-black text-reco-red">{minRating.toFixed(1)}+</span>
                </div>
                <input 
                    type="range" 
                    min="0" max="5" step="0.1" 
                    value={minRating}
                    onChange={(e) => setMinRating(parseFloat(e.target.value))}
                    className="w-full"
                />
            </div>

            {/* Favorite Cuisines */}
            <div className="space-y-6">
                <label className="text-[0.8rem] font-bold uppercase tracking-[0.1em] text-text-secondary flex items-center gap-2">
                    Favorite Cuisines
                </label>
                <div className="flex flex-wrap gap-3">
                    {cuisines.map((c) => (
                        <button
                            key={c}
                            type="button"
                            onClick={() => toggleCuisine(c)}
                            className={`px-8 py-3 rounded-full text-sm font-bold transition-all border-none ${selectedCuisines.includes(c) ? 'bg-reco-red text-white shadow-lg shadow-reco-red/20' : 'bg-[#F5F5F5] text-text-secondary hover:bg-gray-200'}`}
                        >
                            {c}
                        </button>
                    ))}
                </div>
            </div>

            {/* Vibe & Occasion */}
            <div className="space-y-6">
                <label className="text-[0.8rem] font-bold uppercase tracking-[0.1em] text-text-secondary">
                    Vibe & Occasion
                </label>
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                    {vibes.map((v) => {
                        const Icon = v.icon;
                        const isSelected = vibe === v.id;
                        return (
                            <button
                                key={v.id}
                                type="button"
                                onClick={() => setVibe(v.id)}
                                className={`flex flex-col items-center justify-center p-8 rounded-3xl transition-all border-2 h-[160px] space-y-4 ${isSelected ? 'border-reco-red bg-white shadow-xl shadow-reco-red/5' : 'border-[#F5F5F5] bg-white hover:border-gray-200'}`}
                            >
                                <div className={`p-4 rounded-full transition-colors ${isSelected ? 'text-reco-red' : 'text-text-primary'}`}>
                                    <Icon size={28} />
                                </div>
                                <span className={`text-sm font-bold ${isSelected ? 'text-text-primary' : 'text-text-secondary'}`}>{v.label}</span>
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* Submit */}
            <div className="pt-6">
                <button 
                    type="submit" 
                    disabled={isLoading}
                    className="w-full md:w-auto md:min-w-[300px] mx-auto block bg-reco-red hover:bg-reco-red-hover text-white font-black py-6 px-12 rounded-2xl transition-all duration-300 shadow-2xl shadow-reco-red/30 disabled:opacity-70 group"
                >
                    {isLoading ? (
                        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mx-auto"></div>
                    ) : (
                        <div className="flex items-center justify-center gap-3">
                            <span>Find Best Matches</span>
                            <ArrowRight size={22} className="group-hover:translate-x-1 transition-transform" />
                        </div>
                    )}
                </button>
            </div>
        </form>
    );
}
