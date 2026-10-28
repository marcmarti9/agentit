---
name: vibe-coded-seo
description: |
  Full technical SEO checklist and remediation for vibe-coded or client-rendered sites so Google can actually see and rank them.
  Use when a site built with AI or a modern SPA is not ranking, when the user pastes the classic SEO prompt, or before launch of a marketing site.
license: Apache-2.0
---

# Vibe-Coded SEO

Google cannot rank what it cannot see. This skill turns the common "rank #1 by Friday" checklist into a concrete, evidence-based procedure for sites that were generated or heavily client-rendered.

## When to use

- A new site or landing page built with AI / Next.js / Remix / pure client SPA is not showing in Google.
- The user pastes or references the classic SEO checklist (SSR, sitemap, WebP, schema, Lighthouse, etc.).
- Before the first serious marketing push on a vibe-coded property.

Do not use for:
- Pure content strategy or link-building campaigns (those belong in growth/marketing skills).
- Sites that are already server-rendered, indexed and ranking; use a lighter audit instead.

## Procedure

1. **Render reality check**
   - Fetch the page as Googlebot would (or use the browser with JS disabled / Lighthouse).
   - Confirm the main content, H1 and key links are present in the initial HTML.
   - If the page is a blank shell, fix rendering first (SSR, SSG, ISR or a proper pre-render).

2. **Crawlability**
   - `robots.txt` does not block Googlebot.
   - No accidental `noindex`.
   - Canonical tags point to the preferred URL.
   - Sitemap exists, is valid and is submitted in Search Console.
   - No redirect chains or soft-404s.
   - Orphan pages are linked from somewhere crawlable.

3. **On-page basics**
   - One H1 per page that matches intent.
   - Unique meta description per important page.
   - FAQ schema where there are real FAQs.
   - Breadcrumbs on deep pages.
   - Alt text on every meaningful image.

4. **Performance & assets**
   - Images converted to WebP or AVIF and sized to the display size.
   - Below-the-fold images lazy-loaded.
   - Fonts loaded the framework way; limited to 1–2 families.
   - Layout shifts fixed (explicit dimensions, font-display).
   - Lighthouse mobile median ≥ 90 on the key pages (or a documented reason why not).

5. **Content signals**
   - Remove obvious AI slop (repetitive phrases, "in conclusion", unsupported superlatives).
   - Real author bio or company identity where it matters.
   - Internal links that make sense.

6. **Verification**
   - Run Lighthouse three times in mobile mode on the homepage and the two or three slowest pages; record the median.
   - Confirm in Search Console that the pages are indexed (or at least not excluded for the reasons you just fixed).
   - Report before/after numbers.

## Output

- A checklist table with pass/fail and the exact file or config that was changed.
- Lighthouse medians before and after.
- Remaining items that need the user (Search Console property, backlinks, etc.).

## Relationship to other skills

- This skill owns the technical SEO remediation for newly built or poorly indexed sites.
- Compose with `pre-ship-audit` when the same site also needs security and design checks.
- Content strategy, keyword research and link acquisition stay in the growth / marketing skills.
