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

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchLocations(): Promise<string[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/locations`);
    if (!response.ok) throw new Error('Failed to fetch locations');
    const data = await response.json();
    return data.locations;
}

export async function fetchRecommendations(request: PreferenceRequest): Promise<ContractResponse> {
    const response = await fetch(`${API_BASE_URL}/api/v1/recommendations`, {
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
            if (errorData.detail) {
                errorMsg = typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail);
            } else if (errorData.error) {
                errorMsg = errorData.error;
            }
        } catch(e) {}
        throw new Error(errorMsg);
    }

    return response.json();
}

