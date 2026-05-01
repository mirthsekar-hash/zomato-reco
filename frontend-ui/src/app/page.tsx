"use client";

import { useState, useEffect } from "react";
import PreferenceForm from "@/components/PreferenceForm";
import RecommendationList from "@/components/RecommendationList";
import { PreferenceRequest, ContractResponse, fetchRecommendations, fetchLocations } from "@/lib/api";
import { AlertCircle } from "lucide-react";

export default function Home() {
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState<ContractResponse | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [locations, setLocations] = useState<string[]>([]);

    useEffect(() => {
        const loadLocations = async () => {
            try {
                const locs = await fetchLocations();
                setLocations(locs);
            } catch (err) {
                console.error("Failed to load locations", err);
            }
        };
        loadLocations();
    }, []);

    const handleSearch = async (request: PreferenceRequest) => {
        setIsLoading(true);
        setError(null);
        try {
            const data = await fetchRecommendations(request);
            setResponse(data);
        } catch (err: any) {
            setError(err.message || "An unexpected error occurred");
        } finally {
            setIsLoading(false);
        }
    };


    return (
        <div className="relative">
            {/* Hero Section */}
            <div className="relative min-h-[700px] flex items-center justify-center pt-20 pb-40 overflow-hidden">
                {/* Background with Blur Overlay */}
                <div 
                    className="absolute inset-0 bg-cover bg-center grayscale-[0.2]"
                    style={{ backgroundImage: "url('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&q=80&w=2000')" }}
                >
                    <div className="absolute inset-0 bg-black/40 backdrop-blur-[2px]"></div>
                </div>

                {/* Content */}
                <div className="relative z-10 container mx-auto px-6 text-center text-white space-y-8">
                    <h1 className="text-6xl md:text-8xl font-black tracking-tight drop-shadow-2xl animate-in fade-in zoom-in duration-1000">
                        Tailored for You
                    </h1>
                    <p className="text-lg md:text-xl max-w-2xl mx-auto font-medium leading-relaxed opacity-90 drop-shadow-md">
                        Tell us your taste, and we'll handle the rest. Discover the finest dining experiences curated specifically for your palate.
                    </p>
                </div>
            </div>

            {/* Form Overlay Section */}
            <div className="container mx-auto px-6 -mt-32 relative z-20 pb-24">
                <PreferenceForm onSubmit={handleSearch} isLoading={isLoading} locations={locations} />
            </div>


            {/* Results Section */}
            {(response || error || isLoading) && (
                <div className="container mx-auto px-6 py-12 space-y-12 bg-white rounded-t-[3rem] shadow-2xl animate-in slide-in-from-bottom-12 duration-700">
                    {error && (
                        <div className="max-w-2xl mx-auto bg-reco-light border border-reco-red/20 text-reco-red p-6 rounded-3xl flex items-center gap-4">
                            <AlertCircle size={24} className="shrink-0" />
                            <p className="font-semibold">{error}</p>
                        </div>
                    )}

                    {response && !error && (
                        <div className="space-y-12">
                            <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
                                <div className="space-y-2">
                                    <h2 className="text-4xl font-black text-text-primary tracking-tight">
                                        Top Matches
                                    </h2>
                                    <p className="text-text-secondary font-medium">
                                        Found {response.total_results} exceptional restaurants based on your palate.
                                    </p>
                                </div>
                                <div className="bg-[#F5F5F5] px-6 py-3 rounded-2xl text-sm font-bold text-reco-red">
                                    AI-Ranked for Precision
                                </div>
                            </div>
                            
                            {response.recommendations.length > 0 ? (
                                <RecommendationList recommendations={response.recommendations} isLoading={false} />
                            ) : (
                                <div className="text-center py-24 bg-[#FAFAFA] rounded-[2.5rem] border-2 border-dashed border-gray-200">
                                    <p className="text-xl text-text-secondary font-bold">No restaurants matched your exact criteria.</p>
                                    <p className="text-text-muted mt-2">Try relaxing your budget or lowering the minimum rating.</p>
                                </div>
                            )}
                        </div>
                    )}

                    {isLoading && !response && (
                        <div className="pt-12">
                            <RecommendationList recommendations={[]} isLoading={true} />
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
