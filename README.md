
# Cover Letter Writer Project

**From URL to first-draft cover letter in 42 seconds.**

This project helps automate job applications by using a structured candidate profile and a configurable workflow to populate application fields and generate tailored materials.

The automation produces a strong first-draft cover letter quickly, but treat it as a starting point. Review the generated letter for accuracy, tone, and specificity; then improve wording, add personal touches, and correct any factual errors. This tool is a time-saver, not a replacement for human insight.

## Overview

- **Inputs:** put your `Candidate Profile.txt`, `Workflow.json` and template_cover_letter.docx in the `inputs/` folder.
- **Output:** application artifacts and logs are written to the `output/` folder.
- **Runner:** `main.py` in the project root executes the automation pipeline.

## Quick Start

1. (Optional) Create and activate a virtual environment.
2. Copy the provided `.envexample` to `.env` in the project root and set the required environment variables. Keep secrets out of version control and never commit your `.env` file.
3. Place your `Candidate Profile.txt` into `inputs/`.
4. Configure or verify `inputs/Workflow.json` for the automation steps.
5. Run:

```
uv run main.py
```

Generated files will appear in `output/`.

## Candidate Profile Guidelines

A good `Candidate Profile.txt` is clear, consistent, and structured so the automation can reliably parse and use the information. Prefer plain text with clearly labeled sections. Use short lines and consistent separators.

Using AI to create a Candidate Profile:

- If you don't already have a tidy profile, use an AI assistant to generate one by feeding it the information below, your resume, an existing cover letter, and any contextual information (preferred roles, locations, priorities). Review and edit the AI output for accuracy and tone before saving as `Candidate Profile.txt`.

Recommended sections (order not strict):

- Name: Full name as you want it to appear on applications
- Contact: email, phone, location, LinkedIn, portfolio, resume path (optional)
- Title / Headline: short target title, e.g., "Senior Backend Engineer"
- Summary: 1–3 sentence professional summary
- Skills: comma- or newline-separated list of core skills and technologies
- Experience: repeated blocks with Company, Role, Dates, and bullet achievements
- Education: degree, school, year
- Certifications: name and year
- Preferences: preferred roles, locations, remote/in-office, salary range (optional)
- Keywords: domain-specific keywords to help match job descriptions
- Cover Letter Template: optional templated text with placeholders

Tips for a strong profile:

- Use measurable achievements (percentages, scale, dollars) in Experience.
- Include role-specific keywords recruiters and ATS look for.
- Keep Skills concise; separate primary skills from secondary tools.
- For multiple role targets, create alternate profiles or include a `Preferences` section describing targets.


## Workflow.json

`inputs/Workflow.json` configures the steps your automation will take (mapping profile fields to application fields, applying templates, etc.). Keep it in JSON and document any custom keys used by your local automation logic.

## Project Structure

- `main.py` — entry point
- `src/functions.py` — core helpers
- `inputs/` — `Candidate Profile.txt`, `Workflow.json`
- `output/` — generated application files

## Notes

- This README describes how to prepare a `Candidate Profile.txt` so automation can produce higher-quality, targeted applications. If you want, maintain multiple candidate profiles for different role types.
