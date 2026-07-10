# Y Combinator Application Draft: Radar Comercial

Este documento contiene las preguntas clave del formulario oficial de **Y Combinator (YC)** con respuestas redactadas en el estilo directo, conciso y basado en hechos que buscan los evaluadores de YC.

---

## 1. Company Info

### What is your company going to make?
We are building a private, client-side relational intelligence wallet that helps B2B sales representatives mine and leverage their existing first-degree professional networks to close deals, without ceding ownership of their contacts to the company CRM.

#### Why did you choose this idea? What do you know about this problem that others don't?
As former sales executives at leading fintechs (Clip, Fiserv), we know that cold outreach (emails/messages) is dead, yielding response rates under 1%. However, we also know that sales representatives collectively sit on thousands of warm, first-degree LinkedIn connections that are completely abandoned. 

We discovered a critical structural secret of the LinkedIn algorithm: **LinkedIn limits organic reach by testing posts on a small initial cohort (5-10% of your network)**. If you have 4,000 "dead-weight" connections (inactive, irrelevant profiles), the test cohort gets diluted, nobody interacts, and the algorithm kills the post's reach. By providing a "LinkedIn Purger" tool, sales reps prune their network down to their active 150-connection Dunbar Limit. This instantly triggers the LinkedIn algorithm to boost their organic content reach. 

Additionally, sales reps hide their networks from Salesforce/HubSpot because they view their contacts as personal professional equity. By building a "Zero-Knowledge" client-side wallet where contacts are processed locally, reps will willingly upload their data to find warm paths to target accounts, while companies will happily pay to unlock those introductions.

---

## 2. Market & Competition

### Who are your competitors?
*   **LeadDelta:** Focuses on the individual B2C user managing their LinkedIn inbox. They lack team collaboration, CRM integration matching, and semantic matching for complex B2B pipelines.
*   **Clay / Folk:** Modern relational databases. They act as alternative CRMs rather than lightweight add-ons, requiring high implementation friction, custom engineering, and expensive licenses.
*   **Apollo / Lusha:** Databases for cold, bulk contact scraping. They do not map trust paths or existing relationships.
*   **Crossbeam / Cabal:** Enterprise partner ecosystems matching account lists between two companies, not mapping the internal sales team's networks.

### What is your unique differentiator? (Why you?)
We are the only platform implementing a **"Private Wallet" (Zero-Knowledge) architecture** for relationship data. 
*   **For the Sales Rep:** Their network remains encrypted and private. They only expose a specific contact when a match is found and they decide to make an introduction. If they leave the company, they disconnect their wallet and their contacts disappear from the company CRM.
*   **For the Company:** They do not own the rep's contacts but pay a subscription to run matching algorithms (semantic search and embeddings) that alert the rep when a warm intro can shorten a sales cycle.

---

## 3. Product & Technical Detail

### How does it work technically?
1.  **Bring Your Own Data (BYOD):** The sales rep uploads their LinkedIn data export (ZIP) to the browser.
2.  **Client-Side Encryption:** The Chrome Extension parses the data locally and encrypts it using AES-256. Only anonimized hashes (SHA-256) of company and title strings are sent to our servers.
3.  **Semantic Matching Engine:** Our backend compares the anonymized hashes against the company's active target accounts (leads/deals) in HubSpot/Salesforce using vector embeddings.
4.  **The "Warm Connection" Alert:** If a match is found, a local widget in HubSpot alerts the rep: *"You are connected to the Head of Finance at this account. Habilitar introducción."*
5.  **Referral Bounty:** If the intro leads to a closed deal, the rep gets a $150 USD bounty and a 2% commission paid by the company, automated through the platform.

---

## 4. Growth & Monetization

### How do you make money?
We operate a hybrid business model:
1.  **B2C Prosumer ($10 USD/month):** For individual freelancers and job seekers using their personal dashboard to filter and find warm connection routes.
2.  **B2B Team Subscription ($30 - $50 USD/user/month):** For companies linking their CRM to run the matching engine on their sales team's collective networks.
3.  **Referral Commission Splits:** A fee on internal co-selling bounties paid to reps.

### How will you acquire customers?
*   **Bottom-Up Adoption (B2C2B):** We distribute the tool to individual sales reps looking to hit quota. Once multiple reps in a company use it, the VP of Sales buys the B2B team tier to coordinate matches and integrate with the corporate CRM.
*   **CRM Marketplaces:** Listing our plugin on HubSpot and Pipedrive app stores as an adoption tool. HubSpot wants us because we solve the "Empty CRM" problem by giving reps an incentive to use it.
*   **Communities:** Growth loops via sales training programs and Slack channels.

---

## 5. Team & Execution

### Who is in the team?
We have a balanced, high-execution team:
*   **Founder (Antonio):** Strong commercial background in B2B sales, adquirencia, and payments (Clip, Fiserv, LATAM Commerce). Liderando estrategia de negocio y GTM.
*   **Data Engineer & Data Scientist (José & team):** Building the parsing pipelines, vector embeddings, and geographic inference models.

### What is the immediate validation plan (next 2 weeks)?
We will not build the automated platform yet. We are launching a **Private Client-Side MVP**:
1.  Deliver a single-file interactive HTML dashboard (`index.html`) to 15 friendly sales reps.
2.  The reps drag and drop their own LinkedIn `Connections.csv` locally.
3.  The dashboard cleans the data, infers countries, and generates warm pitches for their target accounts *completely locally on their own screen* (0% data sharing, overcoming the trust barrier).
4.  Offer a paid upgrade ($10 USD/month) to run the weekly update, filter by country/hierarchy, and access custom Toku/Netpay pitch templates.
If 3-5 reps pay, the B2C demand is validated, and we begin coding the Chrome Extension.
