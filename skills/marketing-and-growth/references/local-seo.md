# Local SEO + AI visibility — evidence-first playbook

Use this reference for local businesses: storefronts, service-area businesses (SABs), hybrid businesses, restaurants, clinics, professional services, retail and other location-dependent businesses.

This is a specialization of the main SEO workflow, not a separate SEO doctrine. Load seo-growth-loop.md as well when the task includes broad technical SEO, search opportunity discovery or ongoing measurement.

## Source hierarchy

Prefer current first-party guidance over creator heuristics.

Reviewed 2026-09-18:

- Google Business Profile representation guidelines: https://support.google.com/business/answer/3038177
- Google local ranking guidance: https://support.google.com/business/answer/7091
- Google Maps fake-engagement/review policy: https://support.google.com/contributionpolicy/answer/7400114
- Google Search spam policies: https://developers.google.com/search/docs/essentials/spam-policies
- Google LocalBusiness structured data: https://developers.google.com/search/docs/appearance/structured-data/local-business
- Google generative-AI search optimization guide: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- OpenAI publisher/search crawler guidance: https://help.openai.com/en/articles/12627856
- Bing Webmaster Tools (authenticated reports must be inspected live): https://www.bing.com/webmasters/
- Bing IndexNow: https://www.bing.com/indexnow/getstarted

Creator posts, agency case studies and SEO-tool studies may generate hypotheses, but never turn their thresholds or correlations into universal rules without current evidence.

## 1. Define the business reality first

Record the business model, real staffed locations, service areas actually served, primary services/products, target locations, the qualified conversion (call, booking, order, form, visit or revenue), current GBP ownership/verification state, website/domain and tracking quality.

A local SEO plan must represent the real business. Do not design a profile or page architecture around a ranking tactic that the company cannot truthfully support.

## 2. Eligibility and policy guardrails

Google Business Profile is an identity/product surface, not a sandbox for keyword experiments.

- Use the real-world business name. Do not add keywords that are not part of the represented business name.
- Use one profile per eligible business/location unless Google's documented exceptions apply.
- A virtual office is not eligible merely because an address can be rented.
- A coworking location is eligible only when the business meets Google's current requirements, including real presence, signage and staff/customer service as applicable.
- A SAB that does not serve customers at its address should hide that address and configure a service area.
- Multiple profiles require genuinely distinct eligible locations/operations, not duplicate pins for coverage.
- Keep categories minimal, accurate and specific to what the business actually does.

Before changing name, address, category, ownership or location structure, check current GBP policy and the actual business evidence.

## 3. Baseline the local market

Inspect current evidence before prescribing tactics:

- GBP completeness, eligibility and verification;
- target query + location combinations;
- current local pack / Maps / organic results from relevant geographies;
- real competitor profiles and landing pages;
- primary categories and service/product coverage;
- review count, rating, themes and recent velocity;
- website crawlability/indexation and local landing pages;
- citations/entity consistency on material directories;
- backlinks/mentions/local PR;
- GSC, analytics, GBP performance and call/booking/order data where available.

Google describes the main local ranking dimensions as relevance, distance and prominence. Treat that as the primary model. Competitive observations are evidence about the market, not proof of a secret ranking formula.

## 4. Google Business Profile optimization

Prioritize completeness and accuracy:

- correct name, address/service area, phone, website and hours;
- the smallest truthful set of categories that describes the business;
- applicable services/products/menu/booking attributes;
- high-quality real photos and videos;
- current opening/special hours;
- useful owner responses to reviews;
- booking/order links where supported;
- correct destination page for the user's intent.

Do not claim that keyword stuffing descriptions/posts, exact-match naming or a particular posting frequency is a guaranteed ranking lever. Test only policy-compliant hypotheses and measure them.

## 5. Reviews

Reviews can contribute to prominence and conversion, but the system must stay authentic.

Operating model: real customer interaction -> neutral review request -> no incentive, rating pressure or review gating -> customer writes their own experience -> useful business response -> monitor themes and service issues.

Do not:

- buy or incentivize reviews;
- ask only happy customers while suppressing negative feedback;
- require a specific star rating or wording;
- ask staff/friends/affiliates to manufacture reviews;
- manufacture unusual bursts to imitate demand.

Track rating, volume, response coverage, customer themes and conversion impact. Competitor review counts can be a benchmark, not a universal target.

## 6. Local website / on-page SEO

Use the general technical SEO workflow first.

For local pages:

- create a page when there is a real user/business reason for that service/location combination;
- make location/service pages materially useful and differentiated;
- avoid city-swap templates and doorway pages;
- use descriptive titles, headings and URLs without rigid exact-match formulas;
- make contact, booking/order and location information easy to find;
- link important local pages from a coherent browseable architecture;
- keep canonical URLs correct;
- expose critical content to crawlers and users.

Client-side JavaScript is not automatically non-indexable. Google can process JavaScript, but JS-heavy sites create extra SEO complexity. Verify the rendered result with current search tooling instead of enforcing "SSR or nothing".

### Structured data

Use LocalBusiness or a more specific supported subtype only when it truthfully matches visible page/business data.

- map real name/address/telephone/hours/entity data;
- follow current Google structured-data requirements;
- validate with Rich Results Test / URL Inspection as applicable;
- never fabricate ratings, reviews, prices or business facts;
- do not treat schema as a guaranteed ranking boost.

## 7. Citations and entity consistency

The goal is accurate, corroborated business identity across surfaces that matter.

Prioritize:

1. Google Business Profile;
2. the company's own site;
3. major map/search ecosystems relevant to the market;
4. high-value local/niche directories actually used by customers or search systems;
5. authoritative local organizations, media and industry associations.

Keep core identity facts consistent and correct. Do not chase hundreds of low-quality citations or treat exact character-for-character NAP matching as a substitute for business legitimacy.

## 8. Links, mentions and local authority

Prefer editorially defensible authority: local press, chambers/associations, real sponsorships/community participation, partners/suppliers, industry publications, useful local resources and original research/data worth citing.

Do not encode fixed DR thresholds or anchor-text percentages as universal rules. Evaluate relevance, editorial quality, traffic/audience, indexability, placement, risk and business legitimacy.

Avoid link schemes, PBNs and mass low-quality placements.

## 9. AI search / generative visibility

Do not build a separate mythology around GEO.

For Google, current official guidance says generative AI search still relies on core Search ranking/quality systems. The durable work is therefore:

- crawlable/indexable pages;
- unique, non-commodity, people-first content;
- clear entity/business facts;
- first-hand expertise/evidence;
- useful structure and descriptive headings;
- high-quality supporting images/video where relevant;
- accurate structured data where supported;
- real mentions and authority.

Avoid mass pages targeting every possible prompt/fan-out query, fake mentions, manufactured community posts, unnecessary "AI SEO" files/hacks as a substitute for normal SEO, and claims that a particular passage length or FAQ pattern guarantees citations.

### ChatGPT Search

If the business wants public pages discoverable in ChatGPT Search, verify that OAI-SearchBot is not unintentionally blocked. This improves eligibility for discovery; it does not guarantee inclusion or citation.

### Bing / Copilot

Use Bing Webmaster Tools when relevant. IndexNow can notify supported engines of changed URLs, and inspect any AI Performance/citation report actually available in the authenticated account. Do not claim this audit verified that report's fields or availability from its public JavaScript shell.

### Other answer engines

Inspect live evidence. Search the real buyer questions, record which sources are cited, classify those sources (owned, review/directory, editorial, community, video, marketplace or other), and decide whether the business can legitimately earn presence there.

Never assume a fixed list such as Yelp/Reddit/YouTube is mandatory in every market.

## 10. Conversion and lead handling

SEO success is not traffic in isolation. Choose the business KPI: qualified calls, reservations/bookings, orders, store visits where measurable, qualified forms, or revenue/margin.

Make conversion friction visible: phone/booking/order CTAs, mobile usability, response time, missed calls and lead routing may erase SEO gains even when rankings improve.

## 11. Expansion / additional locations

Do not create or rent locations only to manufacture map coverage.

A new profile/location should follow from a real expansion: eligible operation + staff/customer service as required + durable location evidence + viable economics + policy-compliant profile + useful location page.

If the business cannot support a legitimate location, improve relevance, prominence, content and conversion for the existing operation instead.

## 12. Local SEO audit output

For each finding record: source/evidence, policy status (compliant, uncertain or non-compliant), affected profile/URL/location, business impact, confidence, recommended action, owner/permission required, verification step and metric/review window.

Recommended order:

eligibility/policy -> tracking/baseline -> GBP accuracy/completeness -> crawl/index/technical blockers -> local landing pages/internal linking -> reviews -> citations/entities -> links/mentions -> AI-search visibility -> conversion/lead handling -> legitimate expansion.

## 13. Rules against false precision

Do not promote any of these into canonical rules without current, project-specific evidence:

- "GBP produces X% of local leads";
- "reviews are X% of map-pack ranking";
- "DR N guarantees position #1";
- "200 reviews is enough";
- "exact-match name/domain beats 5x authority";
- fixed backlink anchor percentages;
- "80-90% of links must go to the homepage";
- "one city + one service always requires one page";
- "CSR cannot rank";
- "Yelp/Reddit/listicles are mandatory for LLM visibility".

These may be hypotheses or observations in a particular dataset. Label them as such and validate them before acting.
