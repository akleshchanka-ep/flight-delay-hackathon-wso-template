# Flight Delay Predictor - Frontend

Modern web UI for flight delay predictions, built with Astro, TypeScript, and DaisyUI 5.

## 🛠 Tech Stack

- **Astro** - Server-side rendering framework
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **DaisyUI 5** - Beautiful component library
- **HTMX** (integrated) - Dynamic HTML enhancement

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

### Installation

```bash
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

Or use the startup script:

```bash
./run_frontend.sh
```

The frontend will be available at: **http://localhost:4321**

### Build for Production

```bash
npm run build
npm run preview
```

## 📱 Features

### 🏠 Home Page (`/`)
- Landing page with overview
- Navigation to prediction modes
- Feature highlights

### ⚡ Quick Predict (`/predict`)
- Simple, streamlined interface
- Day of week selection (dropdown)
- Origin and destination airport selection
- Instant prediction results with visual indicators

### 🎛 Custom Predict (`/custom`)
- Advanced prediction interface
- Radio button day selection
- Airport search functionality
- **Batch Prediction Mode**: Predict for entire week
- Enhanced result visualization with comparison tables

## 🧞 Commands

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
| `./run_frontend.sh`       | Start frontend with automated checks             |

## 📁 Project Structure

```
frontend/
├── src/
│   ├── layouts/
│   │   └── Layout.astro          # Base layout with navbar & footer
│   ├── pages/
│   │   ├── index.astro           # Home page
│   │   ├── predict.astro         # Quick prediction
│   │   └── custom.astro          # Custom prediction
│   └── styles/
│       └── global.css            # Global styles with DaisyUI
├── public/                       # Static assets
├── astro.config.mjs             # Astro configuration
├── tailwind.config.cjs          # Tailwind + DaisyUI config
└── package.json                 # Dependencies
```

## � API Integration

The frontend connects to the backend API:

- `GET /airports` - Fetch airport list
- `POST /predict` - Get delay predictions

API base URL: `http://localhost:8000` (configurable via `PUBLIC_API_URL` env var)

## 🎨 Theming

DaisyUI themes available: corporate (default), light, dark, cupcake

Change theme in `src/layouts/Layout.astro`:
```html
<html lang="en" data-theme="corporate">
```

## 📚 Resources

- [Astro Documentation](https://docs.astro.build)
- [DaisyUI Components](https://daisyui.com/components/)
- [Tailwind CSS](https://tailwindcss.com/docs)

---

Built with ❤️ using Astro + DaisyUI
