---
page: dashboard
---
A pure Dashboard layout for the Inventory AI platform that highlights high-level insights above a separate stock table.

**DESIGN SYSTEM (REQUIRED):**
# Design System: Inventory AI Dashboard Overview
**Project ID:** 3094262228024149943

## 1. Visual Theme & Atmosphere
The UI embodies a clean, utilitarian, and airy administrative dashboard atmosphere. Utilize a crisp, high-contrast Light theme characterized by vast light gray backgrounds (Tailwind `bg-gray-100`) juxtaposed against a deeply grounded, dark navy sidebar (`bg-[#0f172a]`).

## 2. Color Palette & Roles
*   **Deep Slate Navy (#0f172a)** — Sidebar navigation background.
*   **Vibrant Action Blue (#2563eb)** — Primary actions and active nav state.
*   **Neutral Canvas (#f3f4f6 / Tailwind gray-100)** — Main container background.
*   **Surface White (#ffffff)** — Elevated cards and settings forms.

## 3. Typography Rules
*   **Typeface:** Inter (`font-sans`).
*   **Headers & Titles:** Rendered in `font-bold` with dark slate text (`text-slate-900`).

## 4. Component Stylings
*   **Buttons:** Subtly rounded corners (`rounded-md`), vibrant blue background.
*   **Cards/Containers:** Generously rounded corners (`rounded-xl`), whisper-soft diffused shadows (`shadow-sm`), delicate 1px border (`border-gray-200`).
*   **Forms/Inputs:** Clean borders, slightly rounded.

**Page Structure:**
1. Global dark sidebar on the left.
2. Top header with user profile image and search bar.
3. Top row: Three metric cards (Total Items, Low Stock Count, Pending Orders).
4. Middle section: AI Insights banner using light blue warning background.
5. Bottom section: A clean table of the Top 5 Critical Items.
