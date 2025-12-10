# ResumeAI - Resume Evaluator Application

A modern, accessible React application that evaluates resumes against job descriptions using AI-powered analysis.

## Features

- **PDF Resume Upload**: Drag-and-drop or click-to-upload functionality for PDF resumes (max 10MB)
- **Job Description Input**: Text area for pasting job descriptions
- **AI Evaluation**: Submit for instant analysis (currently using mock data - connect to your backend API)
- **Score Display**: Circular progress indicator showing match percentage
- **Verdict Badge**: Visual indicator for shortlisted/review/rejected status
- **Missing Skills**: List of skills mentioned in job description but not found in resume
- **Pro Tips**: AI-generated suggestions to improve your resume
- **Improvements List**: Categorized list of actionable improvements
- **PDF Preview**: View your uploaded resume alongside the evaluation results

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling with custom design system
- **shadcn/ui** for accessible UI components
- **React Router** for navigation
- **React Query** for data fetching (prepared for API integration)

## Project Structure

```
src/
├── components/
│   ├── ui/              # shadcn/ui components (Button, Card, etc.)
│   ├── CircularProgress.tsx    # Animated score indicator
│   ├── FileUpload.tsx          # PDF upload component
│   ├── Header.tsx              # App header with logo
│   ├── ImprovementsList.tsx    # Grouped improvement suggestions
│   ├── PDFViewer.tsx           # Resume preview component
│   ├── SkillsList.tsx          # Missing skills display
│   ├── TipCard.tsx             # Pro tip display card
│   └── VerdictBadge.tsx        # Verdict status badge
├── context/
│   └── EvaluationContext.tsx   # Global state for evaluation results
├── pages/
│   ├── Index.tsx               # Home page with upload form
│   ├── ScorePage.tsx           # Results page
│   └── NotFound.tsx            # 404 page
├── types/
│   └── evaluation.ts           # TypeScript interfaces
└── hooks/
    └── use-toast.ts            # Toast notifications
```

## API Integration

The application is designed to connect to a backend API. To integrate:

1. Open `src/pages/Index.tsx`
2. Locate the `handleSubmit` function
3. Replace the mock response with an actual API call:

```typescript
// Current mock implementation:
await new Promise((resolve) => setTimeout(resolve, 2000));
const mockResponse = { ... };

// Replace with:
const response = await fetch('/api/evaluate', {
  method: 'POST',
  body: formData,
});

if (!response.ok) {
  throw new Error('Evaluation failed');
}

const data = await response.json();
```

### Expected API Response Format

```typescript
interface EvaluationResult {
  verdict: string;           // "Shortlisted" | "Review" | "Rejected"
  matchScore: number;        // 0-100
  missingSkills: string[];   // ["Skill1", "Skill2"]
  tip: string;               // "Your professional tip here"
  improvements: Array<{
    area: string;            // "Skills" | "Experience" | "Format"
    suggestion: string;      // "Specific improvement suggestion"
  }>;
}
```

## Running the Application

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Accessibility Features

- Semantic HTML structure with proper headings
- ARIA labels and roles for all interactive elements
- Keyboard navigation support
- Screen reader compatible
- Color contrast compliant
- Focus indicators for all interactive elements

## Design System

The application uses a custom design system defined in:
- `src/index.css` - CSS variables and utility classes
- `tailwind.config.ts` - Tailwind configuration with custom colors

### Key Colors
- **Primary**: Teal/Cyan (`hsl(199, 89%, 48%)`)
- **Accent**: Mint (`hsl(172, 66%, 50%)`)
- **Success**: Green for positive scores
- **Warning**: Amber for missing skills
- **Destructive**: Red for errors

### Typography
- **Display**: Space Grotesk (headings)
- **Body**: DM Sans (content)

## Customization

### Changing Colors
Edit the CSS variables in `src/index.css`:

```css
:root {
  --primary: 199 89% 48%;  /* Your primary color in HSL */
  --accent: 172 66% 50%;   /* Your accent color in HSL */
}
```

### Modifying Score Thresholds
Edit `src/components/CircularProgress.tsx` to change score color thresholds:

```typescript
const getScoreColor = () => {
  if (value >= 80) return 'text-success';  // Green
  if (value >= 60) return 'text-primary';  // Blue
  if (value >= 40) return 'text-warning';  // Amber
  return 'text-destructive';               // Red
};
```

## License

MIT License
