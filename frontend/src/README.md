# frontend/src

**Purpose:** React + TypeScript source code for the IdeaProof web application — the optional UI layer that calls the FastAPI backend.

**Weeks:** 6 (optional stretch goal — build a frontend for the validation API).

## Structure

| Path | Description |
|------|-------------|
| `main.tsx` | React entry point — mounts `<App />` into the DOM |
| `App.tsx` | Main application component — full landing page with 7 sections |
| `index.css` | Global styles, Tailwind CSS v4 theme tokens, custom animations |
| `components/ui/` | Reusable UI components following the shadcn/ui pattern |
| `lib/utils.ts` | Utility functions — `cn()` for Tailwind class merging |

## Key Dependencies

- **React 19** + **TypeScript** — type-safe component development
- **Tailwind CSS v4** — utility-first styling via `@tailwindcss/vite` plugin
- **Framer Motion** — scroll and entrance animations
- **Lucide React** — icon library
- **shadcn/ui pattern** — `Button`, `Hero` components in `components/ui/`

## API Contract

The frontend calls two backend endpoints:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/health` | Check if the API is online (polled every 30 s) |
| `POST` | `/validate-idea` | Submit `{ "idea": "..." }`, receive `ValidationResponse` |

Field names and types match `app/schemas/idea_schema.py` and `app/schemas/response_schema.py` exactly.
