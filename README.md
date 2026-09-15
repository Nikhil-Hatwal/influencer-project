# 📊 Influencer Campaign ROAS Dashboard

A Streamlit dashboard to analyze the performance of influencer marketing campaigns. It supports campaign-level and influencer-level filtering, calculates ROAS (Return on Ad Spend), simulates incremental ROAS (A/B testing style), and provides insights via charts and persona breakdowns.

## 📦 Installation & Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/Ansh-Malik1/Influencer-Campaign-ROI-calc.git
   cd Influencer-Campaign-ROI-calc
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample data**
   ```bash
   python data_generation.py
   ```

4. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

---

## 📁 Directory Structure

```
Influencer-Campaign-ROI-calc/
│
├── app.py                    # Streamlit dashboard app
├── data_generation.py       # Synthetic data generator
├── requirements.txt         # Dependencies
├── README.md                # You're here!
└── data/
    ├── influencers.csv
    ├── posts.csv
    ├── tracking_data.csv
    └── payouts.csv
```

---

## 📊 Dashboard Overview

### 🔎 Filters (Sidebar)
- **Platform**
- **Category**
- **Product**
- **Influencer Type**
- **Optional file upload for custom data**

---

### 📈 Key Visuals & Metrics

| Section             | Description                                      |
|---------------------|--------------------------------------------------|
| **Key Metrics**     | Total revenue, payout, ROAS                      |
| **Incremental ROAS**| Simulated A/B test (control vs. exposed)         |
| **Top Influencers** | Based on ROAS                                    |
| **Poor ROI Alerts** | Influencers with ROAS < 1x                       |
| **Best Personas**   | Category × Gender breakdown                      |
| **Scatterplot**     | Revenue vs. Payout                               |
| **Engagement Graph**| Engagement by platform                           |
| **Persona Heatmap** | ROAS grid for personas                           |

---

## 🧪 Incremental ROAS Simulation

This metric estimates the ROI generated from users exposed to influencer campaigns (`group = 1`) compared to a synthetic control group (`group = 0`), using simulated revenue behavior.

---

## 📂 Custom Data Upload (Optional)

You can replace the sample data via the **sidebar file uploader**:

- `influencers.csv`
- `posts.csv`
- `tracking_data.csv`
- `payouts.csv`

⚠️ Ensure the uploaded files follow the required schema below.

---

## 🛠 Data Schema

### `influencers.csv`

| Column           | Description                  |
|------------------|------------------------------|
| `id`             | Unique influencer ID         |
| `name`           | Influencer name              |
| `platform`       | Instagram, YouTube, etc.     |
| `category`       | e.g., Fitness, Beauty        |
| `gender`         | Male, Female, Other          |
| `influencer_type`| Macro, Micro, etc.           |
| `follower_count` | Total followers count        |

---

### `posts.csv`

| Column         | Description              |
|----------------|--------------------------|
| `influencer_id`| FK to influencer         |
| `likes`        | Total likes              |
| `comments`     | Total comments           |
| `reach`        | Total reach              |
| `platform`     | Platform of the post     |
| `url`          | URL of the post          |
| `date    `     | Date of posting          |


---

### `tracking_data.csv`

| Column         | Description                           |
|----------------|---------------------------------------|
| `influencer_id`| FK to influencer                      |
| `product`      | Promoted product                      |
| `revenue`      | Revenue generated                     |
| `user_id`      | Simulated customer ID                 |
| `group`        | 0 = control group, 1 = exposed group  |
| `source  `     | Source of the order                   |
| `date    `     | Date at which order was placed        |
| `orders`       | Total number of orders                |
| `campaign`     | Simulated campaign id                 |


---

### `payouts.csv`

| Column         | Description                  |
|----------------|------------------------------|
| `influencer_id`| FK to influencer             |
| `total_payout` | Total payment to influencer  |
| `basis`        | Order based or post based payout|
| `orders`       | Number of orders generated     |
| `rate`         | Basic rate for payout calculation     |



---

## ⚠️ Known Issues

- Seaborn palette warnings appear on older versions — assign `hue` to suppress.
- Some charts may appear squished on smaller screens. Use **wide layout** in Streamlit for optimal spacing.
- Ensure **Streamlit version ≥ 1.20** for full compatibility.

---

## 🧠 Key Insights

- Identify top revenue-generating influencers.
- Filter by category, platform, or influencer type to refine analysis.
- Quantify marketing uplift through **Incremental ROAS**.
- Track ROI efficiency across different **personas and demographics**.
- Compare platform-level **engagement rates**.

---


