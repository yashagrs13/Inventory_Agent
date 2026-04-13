# Design System: Inventory AI Dashboard Overview
**Project ID:** 3094262228024149943

## 1. Visual Theme & Atmosphere
The UI embodies a clean, utilitarian, and airy administrative dashboard atmosphere. Despite the project's 'Dark' colorMode metadata preference, the actual screen implementation utilizes a crisp, high-contrast Light theme characterized by vast light gray backgrounds juxtaposed against a deeply grounded, dark navy sidebar. The design feels structured, professional, and data-centric—ideal for inventory management without overwhelming the user with heavy borders or harsh shadows.

## 2. Color Palette & Roles

*   **Deep Slate Navy (#0f172a)** — Used as the foundational background for the sidebar navigation, providing a heavy anchor that balances the airy main content area.
*   **Lighter Slate Hover (#1e293b)** — Used for subtle, low-friction hover states on inactive navigation items.
*   **Vibrant Action Blue (#2563eb)** — The project's primary accent color. It drives primary actions (like "Create Purchase Order") and denotes the active navigational state.
*   **Soft Alert Atmosphere (#e0f2fe)** — A very pale, icy blue used uniquely as the background for the "AI Insights" banner to gently draw the eye without signaling an error.
*   **Neutral Canvas (#f3f4f6 / Tailwind `gray-100`)** — The overarching canvas color for the main application view. 
*   **Surface White (#ffffff)** — Used for elevated cards and table containers to distinctly separate structured data from the canvas background.
*   **Status Indicators**:
    *   *Positive Green* (Light: `#dcfce7`, Text: `#166534`) — Represents "In Stock" stability.
    *   *Warning Orange* (Light: `#ffedd5`, Text: `#ea580c`) — Represents "Low Stock" cautions.
    *   *Critical Red* (Light: `#fee2e2`, Text: `#dc2626`) — Represents "Out of Stock" alerts.

## 3. Typography Rules
*   **Typeface:** The system universally relies on **Inter**, a highly legible, modern sans-serif font.
*   **Hierarchy & Weight:** 
    *   **Headers & Titles:** Rendered in `font-bold` (700 weight) with dark slate text (`text-slate-900`) to create a stark contrast against body copy.
    *   **Body & Data Rows:** Rendered in `font-medium` (500 weight) for item names and regular weight (`text-gray-600`) for secondary table metadata (like SKUs).
    *   **Micro-copy:** Table headers use `text-xs uppercase font-semibold tracking-wider` to clearly demarcate column labels without competing visually with the data itself.

## 4. Component Stylings

*   **Buttons:** 
    *   Primary buttons feature "Subtly rounded corners" (`rounded-md` / 6px radius) with a solid Vibrant Action Blue background and white text. They employ `shadow-sm` and a smooth color transition on hover (`hover:bg-blue-600`).
    *   Secondary buttons are transparent with a delicate gray stroke (`border-gray-300`) and gray text, turning solid white upon hover.
*   **Cards/Containers:** 
    *   Main data containers and insight banners feature "Generously rounded corners" (`rounded-xl` / 12px radius).
    *   They employ "Whisper-soft diffused shadows" (`shadow-sm`) accompanied by a very delicate 1px border (`border-gray-200` or `border-blue-100`) to define their edges against the canvas rather than relying entirely on heavy drop shadows.
*   **Badges/Status Tags:**
    *   Status indicators strictly use "Pill-shaped" geometry (`rounded-full`) with a high-contrast pairing of a tinted background and a saturated text color from the same hue family.

## 5. Layout Principles
*   **Structural Grid:** The application follows a rigid sidebar-and-main-content architectural split. The sidebar is fixed at 256px (`w-64`) while the main content flexes to fill the remaining viewport.
*   **Whitespace Strategy:** The design leverages generous internal padding (`p-6` to `p-8`) inside the main scrollable area, creating a relaxed, breathable reading experience.
*   **Dividers:** Structural breaks between table rows or header sections heavily favor subtle 1px strokes (`border-gray-100`) over solid background color changes, maintaining the UI's lightness.
