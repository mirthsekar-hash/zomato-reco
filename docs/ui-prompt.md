# Google Stitch UI Generation Prompt

*Copy and paste the prompt below into Google Stitch to generate the Next.js frontend for the AI-Powered Restaurant Recommendation System.*

---

**Prompt:**

Build a modern, responsive, and aesthetically pleasing frontend UI for an AI-powered restaurant recommendation service (inspired by Zomato) using Next.js. The application should have a premium feel, utilizing smooth animations, a clean color palette (e.g., vibrant primary color with a sleek dark or light mode), and modern typography.

The UI should consist of two main sections/phases, which can be presented as a seamless flow (e.g., a landing page that transitions into a results page, or a conversational/form interface that reveals recommendations).

**1. User Preference Capture (Input Interface):**
Design an engaging and intuitive form or chat-like interface to collect the following user constraints:
- **Location:** (e.g., Delhi, Bangalore - text input or searchable dropdown)
- **Budget:** (Low, Medium, High - toggle buttons or slider)
- **Cuisine:** (e.g., Italian, Chinese, North Indian - multi-select pills or dropdown)
- **Minimum Rating:** (Slider or star rating selector, e.g., 3.5+)
- **Additional Preferences/Tags:** (e.g., Family-friendly, Quick service, Romantic - tags or checkboxes)
- A prominent, stylish "Find Restaurants" or "Get Recommendations" submit button with a clear loading state/animation.

**2. Recommendation Display (Results Interface):**
Design a stunning results view to display the AI's top restaurant picks.
- Present the recommendations as visually appealing "Restaurant Cards" or a structured modern list.
- Each card must include:
  - **Restaurant Name** (prominent heading)
  - **Cuisine** (tags or badges)
  - **Rating** (star rating component with the exact number)
  - **Estimated Cost** (e.g., ₹₹, "Medium", or exact amount)
  - **AI Explanation:** A dedicated section or beautifully styled callout box within the card that displays a human-like explanation of *why* this restaurant is a good fit based on the user's specific inputs (e.g., "AI Pick: This matches your romantic vibe and Italian craving perfectly...").
- Include a "Refine Search" or "Back" button to allow users to adjust their preferences easily.

**Technical Requirements:**
- Use **Next.js** (App Router preferred).
- Use **Tailwind CSS** for styling, ensuring best practices for responsive design across mobile and desktop.
- Include micro-interactions (e.g., hover effects on cards, smooth transitions when the form is submitted).
- Use placeholder data/images where necessary to demonstrate the design, but structure the components so they can easily accept real data from an API via props later.
- Ensure semantic HTML, proper component isolation, and accessibility best practices.

Please generate the complete, working Next.js code for this UI, including the main page layout and any necessary reusable components (like `RestaurantCard`, `PreferenceForm`, etc.).
