import { RestaurantRecommendation } from "@/lib/api";
import { Star, MapPin, IndianRupee, Sparkles, TrendingUp } from "lucide-react";

export default function RestaurantCard({ restaurant }: { restaurant: RestaurantRecommendation }) {
    return (
        <div className="bg-white rounded-[2rem] overflow-hidden border border-gray-100 hover:border-reco-red/30 transition-all duration-500 shadow-sm hover:shadow-2xl group flex flex-col h-full relative">
            {/* Rank Badge */}
            {restaurant.rank && (
                <div className="absolute top-4 left-4 z-10 bg-reco-red text-white text-xs font-black w-8 h-8 rounded-full flex items-center justify-center shadow-lg shadow-reco-red/20">
                    #{restaurant.rank}
                </div>
            )}

            {/* Top Info */}
            <div className="p-8 flex-grow space-y-6">
                <div className="flex justify-between items-start gap-4">
                    <h3 className="text-2xl font-black text-text-primary group-hover:text-reco-red transition-colors leading-tight">
                        {restaurant.restaurant_name}
                    </h3>
                    <div className="bg-[#F5F5F5] px-3 py-1.5 rounded-xl flex items-center gap-1.5 font-black text-sm text-text-primary shrink-0 border border-gray-100">
                        <span className="text-reco-red">{restaurant.rating ? Number(restaurant.rating).toFixed(1) : "N/A"}</span>
                        <Star size={14} className="fill-reco-red text-reco-red" />
                    </div>
                </div>
                
                <div className="flex flex-wrap gap-3">
                    {restaurant.location && (
                        <div className="flex items-center gap-2 bg-[#FAFAFA] px-4 py-2 rounded-xl text-xs font-bold text-text-secondary border border-gray-50">
                            <MapPin size={14} className="text-reco-red" />
                            {restaurant.location}
                        </div>
                    )}
                    <div className="flex items-center gap-2 bg-[#FAFAFA] px-4 py-2 rounded-xl text-xs font-bold text-text-secondary border border-gray-50">
                        <IndianRupee size={14} className="text-reco-red" />
                        {restaurant.estimated_cost_for_two || "N/A"}
                    </div>
                </div>

                <div className="space-y-2">
                    <div className="flex items-center gap-2 text-[0.7rem] font-black uppercase tracking-wider text-text-muted">
                        <TrendingUp size={12} />
                        Cuisine Palette
                    </div>
                    <p className="text-sm font-bold text-text-secondary leading-relaxed capitalize">
                        {restaurant.cuisine}
                    </p>
                </div>
            </div>

            {/* AI Insight Section */}
            <div className="p-8 bg-[#FDFDFD] border-t border-gray-50 mt-auto relative overflow-hidden group-hover:bg-white transition-colors">
                <div className="absolute top-0 left-0 w-full h-[3px] bg-gradient-to-r from-reco-red/0 via-reco-red/40 to-reco-red/0 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                <div className="flex items-start gap-3">
                    <div className="p-2 bg-reco-light rounded-lg shrink-0">
                        <Sparkles size={18} className="text-reco-red" />
                    </div>
                    <div className="space-y-1">
                        <span className="text-[0.7rem] font-black text-reco-red uppercase tracking-[0.1em] block">AI Analysis</span>
                        <p className="text-sm text-text-secondary font-medium leading-relaxed italic">
                            "{restaurant.ai_explanation}"
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
