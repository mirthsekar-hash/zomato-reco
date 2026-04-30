import { RestaurantRecommendation } from "@/lib/api";
import RestaurantCard from "./RestaurantCard";

interface RecommendationListProps {
    recommendations: RestaurantRecommendation[];
    isLoading: boolean;
}

export default function RecommendationList({ recommendations, isLoading }: RecommendationListProps) {
    if (isLoading) {
        return (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {[...Array(6)].map((_, i) => (
                    <div key={i} className="bg-white rounded-[2rem] h-[400px] animate-pulse border border-gray-100">
                        <div className="p-8 h-full flex flex-col space-y-6">
                            <div className="flex justify-between">
                                <div className="w-3/4 h-8 bg-gray-100 rounded-lg"></div>
                                <div className="w-12 h-8 bg-gray-100 rounded-lg"></div>
                            </div>
                            <div className="flex gap-2">
                                <div className="w-24 h-8 bg-gray-100 rounded-xl"></div>
                                <div className="w-20 h-8 bg-gray-100 rounded-xl"></div>
                            </div>
                            <div className="w-full h-4 bg-gray-100 rounded mt-4"></div>
                            <div className="mt-auto pt-8 border-t border-gray-50">
                                <div className="w-full h-20 bg-gray-50 rounded-2xl"></div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    if (recommendations.length === 0) {
        return null;
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {recommendations.map((restaurant, index) => (
                <div key={`${restaurant.restaurant_name}-${index}`} className="animate-in fade-in slide-in-from-bottom-8 duration-700" style={{ animationDelay: `${index * 150}ms`, animationFillMode: 'both' }}>
                    <RestaurantCard restaurant={restaurant} />
                </div>
            ))}
        </div>
    );
}
