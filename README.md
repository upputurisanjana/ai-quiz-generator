# AI Quiz Generator — Streamlit Frontend

A precision-engineered quiz application with calibrated playfulness. Transforms PowerPoint presentations into interactive MCQ quizzes with AI-generated questions and explanations.

## Design System

**Philosophy:** "Calibrated Playfulness" — strict professional structure with playful geometric accents.

### Color Palette
- **Accent:** `#FF6B4A` Coral (distinctive, warm, energetic)
- **Light Mode:** 
  - Background: `#FAFAF8` (warm off-white)
  - Text: `#1A1A1A` (near-black)
- **Dark Mode:**
  - Background: `#1C1E26` (deep slate)
  - Text: `#E8E8E8` (soft white)
- **Success:** `#00C48C`
- **Error:** `#FF4757`

### Typography
- **Display/Heading:** Inter Bold (700)
- **Body:** Inter Regular (400)
- **Measurements:** SF Mono/Consolas with tabular-nums

### Motion Principles
- Spring easing (cubic-bezier 0.34, 1.56, 0.64, 1) for micro-interactions
- 250ms theme transitions
- 280ms screen transitions with upward slide + fade
- Respects `prefers-reduced-motion`

## Features

### 1. Upload & Parse Screen
- Drag-and-drop `.pptx` validation
- Slide count & word count preview
- Disabled continue state until ready

### 2. Configure Quiz Screen
- Question count slider (5–30)
- Difficulty selector (Simple/Medium/Complex)
- **Timed/Untimed toggle** with live time estimation
- Time calculation: Simple (35s), Medium (67s), Complex (105s) per question

### 3. Quiz Screen
- Single question display with 4 options
- Progress bar with monospace counter
- **Conditional timer** (only in timed mode)
- Selection micro-interactions with scale bounce
- **Per-answer explanations:**
  - Wrong answer: specific reason + correct answer highlight
  - Correct answer: affirmation with explanation
  - Expandable explanation panel with smooth height animation

### 4. Results Screen
- Large monospace score display
- Question-by-question review with expandable details
- Retake/Upload New actions

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set Claude API key:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

3. Run:
```bash
streamlit run app.py
```

## Implementation Notes

### Theme Toggle
Fixed in top-right corner across all screens. 250ms crossfade transition between light/dark modes.

### Timer Behavior
- Only appears in "Timed" mode
- Countdown with warning state at <10% remaining
- Uses monospace with tabular figures for smooth number transitions
- Auto-advances questions when time expires (can be disabled)

### Explanation System
- Requires explicit "Submit Answer" before revealing
- Simultaneous wrong/correct highlighting
- Expandable panel with smooth slideDown animation
- Two-part explanation: "Why wrong" + "Why correct"
- Continue button only after explanation shown

### Motion System
All transitions use spring easing except theme toggle (ease). Supports `prefers-reduced-motion` with instant/fade-only fallbacks.

## Design Decisions

1. **Accent Color Choice:** Coral `#FF6B4A` — distinctive, not generic blue/purple, warm enough to feel playful but saturated enough to work as an action color.

2. **Dual Theme Implementation:** Both themes share identical structure/spacing/hierarchy. Only bg/text/border colors change, preserving the "calibrated playfulness" balance.

3. **Monospace for Measurements:** All counters, timers, scores use tabular-nums variant to prevent layout shift during number updates.

4. **Card-Based Layout:** Rounded 16px cards with 1px hairline borders and subtle shadows maintain the "precise instrument" aesthetic.

5. **Micro-interactions:** Scale bounce (1 → 1.03 → 1) on selection, translateX on option hover — just enough spring to feel responsive without being bouncy.
