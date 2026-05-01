# Vercel Frontend Deployment

Vercel is used to host the Next.js frontend.

## Step-by-Step Instructions

1. **Import Project**:
   - Go to your Vercel Dashboard and click **Add New > Project**.
   - Import your GitHub repository.

2. **Configure Project Settings**:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `frontend-ui`
   - **Build Command**: `npm run build`
   - **Install Command**: `npm install`

3. **Environment Variables**:
   In the **Environment Variables** section, add:
   - `NEXT_PUBLIC_API_URL`: The URL of your deployed Railway backend (e.g., `https://reco-partner-backend.up.railway.app`).
     - *Note*: Ensure there is **no trailing slash** at the end of the URL.


4. **Deploy**:
   Click **Deploy**. Vercel will build your app and provide a production URL.

## Features

- **Automatic Previews**: Vercel will create a preview deployment for every Pull Request.
- **Production Branch**: Pushing to `main` will trigger a production deployment.
- **Edge Runtime**: Next.js is optimized for Vercel's edge network for fast loading.
