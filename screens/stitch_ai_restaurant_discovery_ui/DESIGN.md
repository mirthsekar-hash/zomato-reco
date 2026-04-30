---
name: GourmetAI Design System
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#5b403e'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#8f6f6d'
  outline-variant: '#e4beba'
  surface-tint: '#ba1724'
  primary: '#b71422'
  on-primary: '#ffffff'
  primary-container: '#db3237'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb3ae'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e2dfde'
  on-secondary-container: '#636262'
  tertiary: '#705d00'
  on-tertiary: '#ffffff'
  tertiary-container: '#c8a900'
  on-tertiary-container: '#4b3e00'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad7'
  primary-fixed-dim: '#ffb3ae'
  on-primary-fixed: '#410004'
  on-primary-fixed-variant: '#930014'
  secondary-fixed: '#e5e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1c1b1b'
  on-secondary-fixed-variant: '#474746'
  tertiary-fixed: '#ffe16d'
  tertiary-fixed-dim: '#e9c400'
  on-tertiary-fixed: '#221b00'
  on-tertiary-fixed-variant: '#544600'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  title-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
  stack-sm: 8px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style
The design system is built to evoke a sense of effortless epicurean discovery. It targets a sophisticated audience that values both culinary excellence and technological ease. The aesthetic is a fusion of **Modern Minimalism** and **Glassmorphism**, prioritizing high-resolution food photography as the primary visual driver. 

By utilizing generous whitespace and a "content-first" hierarchy, the system feels like a premium digital magazine. The emotional response should be one of hunger and excitement, balanced by a calm, professional interface that recedes to let the vibrant colors of the cuisine take center stage.

## Colors
The palette is anchored by **Vivid Coral (#FF4D4D)**, a high-energy primary color chosen to stimulate appetite and denote action. This is balanced by a deep Obsidian secondary color for high-contrast typography and premium branding elements. 

In Light Mode, backgrounds utilize a pristine white with subtle "Cool Gray" washes to define sections without harsh borders. In Dark Mode, the system transitions to a deep charcoal-to-black gradient, preserving the vibrancy of the Primary Coral. A Tertiary Gold is reserved exclusively for ratings and "Editor’s Choice" accolades to maintain a sense of prestige.

## Typography
This design system utilizes **Inter** for all typographic needs to ensure maximum legibility across dense data sets like menus and reviews. The hierarchy is strictly enforced through weight variance rather than excessive size changes. 

Display styles use tight tracking and heavy weights to create a "bold editorial" feel, while body text maintains a generous line height for comfortable reading of long-form restaurant descriptions. Labels use all-caps with increased letter spacing to provide a clear distinction for metadata such as price points and distance.

## Layout & Spacing
The layout follows a **12-column fluid grid** for desktop and a single-column stack for mobile. It employs a strict 8px rhythmic scale. Elements are grouped using a "Stack & Cluster" philosophy: related metadata (distance, price, rating) is clustered with 8px gaps, while major content blocks are separated by 48px to allow the layout to breathe. High-quality imagery should always span at least 4 columns to maintain the premium, photography-forward intent.

## Elevation & Depth
Depth is communicated through **Ambient Shadows** and **Backdrop Blurs**. Shadows are extremely diffused (e.g., 20px-40px blur) with very low opacity (5-10%) to avoid a "heavy" feel. 

When an element, such as a reservation modal or a navigation bar, appears over photography, it must use a **Glassmorphic effect** (20px blur) to maintain a sense of spatial context while ensuring text legibility. This creates a "layered" effect that mimics high-end physical menus or glass tabletops.

## Shapes
The shape language is defined by **Softness and Modernity**. A base radius of 16px (1rem) is applied to all primary containers and image cards, creating a friendly and approachable interface. 

Buttons and input fields follow this 16px standard to maintain consistency. Smaller utility elements like tags or "chips" use a full pill-shape (radius: 999px) to distinguish them from actionable containers. Interactive elements should subtly scale (e.g., 1.02x) on hover to provide tactile feedback.

## Components
- **Buttons:** Primary buttons use the Vivid Coral background with white text. Secondary buttons use a glass-style translucent background with a subtle border in light mode, or a dark-tinted fill in dark mode.
- **Cards:** Restaurant cards are the hero component. They must feature a 16:9 aspect ratio image with the 16px border radius. Information is overlayed on the bottom using a subtle scrim or glassmorphic footer.
- **Chips:** Used for cuisine types (e.g., "Japanese," "Vegan"). These are pill-shaped with a light gray fill in light mode and a deep gray fill in dark mode.
- **Inputs:** Search bars and reservation forms use a 16px radius and a subtle 1px border. Focus states highlight the border in Vivid Coral.
- **Progressive Disclosure:** Use accordion-style lists for menus to keep the initial view clean, emphasizing high-quality food photography icons next to dish names.
- **Micro-interactions:** When a user "hearts" a restaurant, the icon should perform a soft "pop" animation, changing from an outline to a solid Vivid Coral fill.