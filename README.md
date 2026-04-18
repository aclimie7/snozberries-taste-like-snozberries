# SmartCart — Shopping Price Comparison

Compare Kroger and Walmart prices with all savings layers applied: **sale/member pricing → store loyalty rewards → credit card rewards** (cashback or points), then get a recommendation for the optimal store — or an optimal split between both.

---

## What It Does

1. Type your grocery list (e.g. "milk", "eggs", "chicken breast")
2. Enter your ZIP code to find local stores
3. Optionally add your credit cards and reward rates
4. Optionally toggle Kroger Plus / Walmart+ enrollment
5. Click **Compare Prices** to see a side-by-side breakdown with your true final cost

### Savings layers applied, in order:
- **Sale / member pricing** (Kroger Plus unlocks promo prices; shown when API key is present)
- **Store loyalty cashback** (Walmart+ 1% Walmart Cash on eligible items)
- **Credit card rewards** (best card automatically chosen per item category; supports cashback % and points×cpp)
- **Split recommendation** — suggests buying specific items at each store when savings exceed $2

---

## Setup

### Prerequisites
- [Node.js 18+](https://nodejs.org) (for the frontend)
- [Python 3.11+](https://python.org) (for the backend)

### 1. Clone and configure
```bash
git clone <repo-url>
cd snozberries-taste-like-snozberries
cp .env.example .env
# Edit .env to add your API keys (optional — app works in Demo Mode without them)
```

### 2. Get API keys (optional — Demo Mode works without them)

**Kroger API (free):**
1. Go to https://developer.kroger.com → Sign Up
2. Create an app with scope `product.compact`
3. Copy **Client ID** and **Client Secret** into `.env`

**Walmart Affiliate API (free):**
1. Go to https://developer.walmart.com → Sign up for Open API
2. Copy your **API Key** into `.env`

> Leave the keys blank to use **Demo Mode** — realistic sample data for ~15 common grocery items.

### 3. Start the backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
# Runs on http://localhost:8000
```

### 4. Start the frontend
```bash
cd frontend
npm install
npm run dev
# Opens http://localhost:5173
```

### 5. Open the app
Visit **http://localhost:5173** in your browser.

---

## Using the App

### Shopping List (left sidebar)
- Enter a 5-digit ZIP code
- Type an item name and quantity, click **Add**
- Click **Compare Prices** to run the comparison

### Store Rewards (left sidebar)
- Toggle **Kroger Plus** if you have a Kroger loyalty card (unlocks member pricing; earns fuel points)
- Toggle **Walmart+** if you're a Walmart+ subscriber (earns 1% Walmart Cash on eligible items)

### Credit Cards (left sidebar)
- Click a quick-add button to add a popular card preset (Amex Gold, Chase Sapphire Preferred, etc.)
- Or click **+ Add custom card** to enter any card:
  - Choose **Cashback %** or **Points (×/dollar)**
  - For points cards, enter your **cents per point** value (e.g. Chase UR ≈ 1.5, Amex MR ≈ 1.0–2.0)
  - Enter earn rates per category: Grocery / General Merchandise / All Other
- Toggle cards on/off with the checkbox

### Results
- **Summary card**: Kroger total vs Walmart total (after all rewards), best store highlighted
- **Split recommendation**: if buying certain items at the other store saves > $2, shows which items to buy where
- **Per-item cards**: side-by-side Kroger vs Walmart, with sale badges, rewards breakdown, and up to 3 product options per store
- Click **details** on any product to see the exact savings breakdown (store reward + credit card reward)

---

## Architecture

```
frontend/   React + TypeScript + Vite + Tailwind + Zustand (localStorage-persisted)
backend/    Python FastAPI — stateless, no database
```

**Backend services:**
- `services/kroger/` — OAuth2 token cache, product search, price normalizer
- `services/walmart/` — API key auth, product search, price normalizer
- `services/rewards.py` — pure-function rewards optimizer (cashback + points unified)
- `services/comparison.py` — async orchestrator, split recommendation

**Demo mode** activates automatically when API keys are absent. All 25 unit tests pass with `pytest` in the `backend/` directory.

---

## Notes

- **Kroger digital coupons** are not surfaced by the public `product.compact` API scope (requires Kroger partner approval). The `has_digital_coupon` field is reserved for a future scope.
- **Walmart store locations** are inferred from ZIP code in demo mode; the Walmart affiliate API doesn't have a standalone locations endpoint.
- Shopping list and credit card settings are saved in your browser (localStorage) — no account needed.
