export interface PreferenceRequest {
    location: string;
    budget: string; // 'low', 'medium', 'high'
    cuisine: string;
    minimum_rating: number;
    additional_preferences?: string;
    top_k?: number;
    llm_model?: string;
}

export interface RestaurantRecommendation {
    restaurant_name: string;
    cuisine: string;
    estimated_cost_for_two: string | number | null;
    rating: number | null;
    ai_explanation: string;
    rank?: number;
    location?: string;
}

export interface ContractResponse {
    generated_at_utc: string;
    total_results: number;
    recommendations: RestaurantRecommendation[];
    meta: Record<string, any>;
}

export async function fetchRecommendations(request: PreferenceRequest): Promise<ContractResponse> {
    const response = await fetch('/api/v1/recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
    });

    if (!response.ok) {
        let errorMsg = 'Failed to fetch recommendations';
        try {
            const errorData = await response.json();
            if (errorData.error) errorMsg = errorData.error;
        } catch(e) {}
        throw new Error(errorMsg);
    }

    return response.json();
}
