import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Influencer ROAS tracking Dashboard", layout="wide")
@st.cache_data
def load_data():
    inf = pd.read_csv("data/influencers.csv")
    posts = pd.read_csv("data/posts.csv")
    tracking = pd.read_csv("data/tracking_data.csv")
    payouts = pd.read_csv("data/payouts.csv")
    return inf, posts, tracking, payouts

st.sidebar.header("📂 Upload Custom Data (Optional)")
uploaded_files = {
    "influencers": st.sidebar.file_uploader("Influencers CSV", type=["csv"]),
    "posts": st.sidebar.file_uploader("Posts CSV", type=["csv"]),
    "tracking": st.sidebar.file_uploader("Tracking Data CSV", type=["csv"]),
    "payouts": st.sidebar.file_uploader("Payouts CSV", type=["csv"])
}

def load_or_upload(file, fallback):
    if file:
        return pd.read_csv(file)
    return fallback

inf_generated, posts_generated, tracking_generated, payouts_generated = load_data()
influencers = load_or_upload(uploaded_files["influencers"], inf_generated)
posts = load_or_upload(uploaded_files["posts"], posts_generated)
tracking = load_or_upload(uploaded_files["tracking"], tracking_generated)
payouts = load_or_upload(uploaded_files["payouts"], payouts_generated)

# --- Filters ---
st.sidebar.header("🧮 Filters")
platforms = st.sidebar.multiselect("Platform", influencers["platform"].unique(), default=influencers["platform"].unique())
categories = st.sidebar.multiselect("Category", influencers["category"].unique(), default=influencers["category"].unique())
products = st.sidebar.multiselect("Product", tracking["product"].unique(), default=tracking["product"].unique())
types = st.sidebar.multiselect("Influencer Type", influencers["influencer_type"].unique(), default=influencers["influencer_type"].unique())

influencers_filtered = influencers[
    influencers['platform'].isin(platforms) &
    influencers['category'].isin(categories) &
    influencers['influencer_type'].isin(types)
]
posts_filtered = posts[posts['influencer_id'].isin(influencers_filtered['id'])]
tracking_filtered = tracking[
    (tracking['influencer_id'].isin(influencers_filtered['id'])) &
    (tracking['product'].isin(products))
].copy()
payouts_filtered = payouts[payouts['influencer_id'].isin(influencers_filtered['id'])]

st.title("📊 HealthKart Influencer Campaign Dashboard")
st.subheader("📈 Key Metrics")
total_revenue = tracking_filtered['revenue'].sum()
total_payout = payouts_filtered['total_payout'].sum()
roas = round(total_revenue / total_payout, 2) if total_payout else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
col2.metric("Total Payout", f"₹{total_payout:,.2f}")
col3.metric("ROAS", f"{roas}x")

exposed = tracking[tracking['group'] == 1]
merged = exposed.merge(influencers_filtered, left_on='influencer_id', right_on='id')
merged = merged.merge(payouts_filtered, left_on='influencer_id', right_on='influencer_id')

# Group by influencer to compute incremental revenue and ROAS
influencer_roas_df = merged.groupby('influencer_id').agg({
    'revenue': 'sum',
    'total_payout': 'first',
    'category': 'first',
    'gender': 'first'
}).reset_index()

# Calculate ROAS
influencer_roas_df['roas'] = influencer_roas_df['revenue'] / influencer_roas_df['total_payout']
influencer_roas_df.rename(columns={'revenue': 'incremental_revenue'}, inplace=True)

st.subheader("📊 Incremental ROAS (Simulated)")

# Simulate control/exposed groups
control = tracking_filtered[tracking_filtered['group'] == 0]
exposed = tracking_filtered[tracking_filtered['group'] == 1]

ctrl_avg = control.groupby('user_id')['revenue'].sum().mean()
exp_avg = exposed.groupby('user_id')['revenue'].sum().mean()
incremental_roas = round((exp_avg - ctrl_avg) / total_payout, 2) if total_payout else 0

st.write(f"**Control Revenue/User**: ₹{ctrl_avg:.2f}")
st.write(f"**Exposed Revenue/User**: ₹{exp_avg:.2f}")
st.metric("Incremental ROAS", f"{incremental_roas:.4f}x")

# --- Top Influencers ---
st.subheader("🏆 Top Influencers by ROAS")

roas_df = tracking_filtered.groupby("influencer_id")['revenue'].sum().reset_index()
roas_df = pd.merge(roas_df, payouts_filtered[['influencer_id', 'total_payout']], on="influencer_id")
roas_df['roas'] = roas_df['revenue'] / roas_df['total_payout']
top_inf = pd.merge(roas_df, influencers, left_on='influencer_id', right_on='id')
top_inf = top_inf.sort_values('roas', ascending=False)
st.dataframe(top_inf[['name', 'platform', 'category', 'follower_count', 'roas']].head(5), use_container_width=True)

# Poor ROIs
st.markdown("### ⚠️ Influencers with Poor ROAS (<1x)")
poor_roas_df = top_inf[top_inf['roas'] < 1].sort_values('roas')
if not poor_roas_df.empty:
    st.dataframe(poor_roas_df[['name', 'platform', 'category', 'roas']], use_container_width=True)
else:
    st.success("All influencers are performing above 1x ROAS 🚀")
    
st.markdown("### 💡 Best Personas by Average ROAS")

persona_df = pd.merge(roas_df, influencers, left_on="influencer_id", right_on="id")
persona_group = persona_df.groupby(["category", "gender"]).agg({
    "revenue": "sum",
    "total_payout": "sum"
}).reset_index()
persona_group["roas"] = persona_group["revenue"] / persona_group["total_payout"]
persona_group = persona_group.sort_values("roas", ascending=False)

st.dataframe(persona_group[['category', 'gender', 'roas']], use_container_width=True)

st.subheader("💸 Revenue vs. Payout")

fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=influencer_roas_df, x='total_payout', y='incremental_revenue', hue='roas', palette='coolwarm', ax=ax)
ax.set_title("Incremental Revenue vs. Payout")
ax.set_xlabel("Payout")
ax.set_ylabel("Incremental Revenue")
st.pyplot(fig)

st.subheader("Best personas by ROAS graph")
fig, ax = plt.subplots(figsize=(12, 6))  # larger and explicit
sns.barplot(data=persona_group, x="category", y="roas", hue="gender", ax=ax)

ax.set_ylabel("Average ROAS", fontsize=12)
ax.set_title("Best Personas by ROAS", fontsize=14)
ax.set_xlabel("Category", fontsize=12)
ax.legend(title="Gender")

fig.tight_layout()
st.pyplot(fig) 

st.subheader("Engagement Rate by Platform")

required_cols = ['likes', 'comments', 'reach', 'platform']
if all(col in posts_filtered.columns for col in required_cols):
    
    posts_filtered = posts_filtered.dropna(subset=['likes', 'comments', 'reach'])
    posts_filtered = posts_filtered[posts_filtered['reach'] > 0]

    posts_filtered['engagement_rate'] = (
        posts_filtered['likes'] + posts_filtered['comments']
    ) / posts_filtered['reach']

    # Compute average engagement per platform
    platform_grouped = posts_filtered.groupby('platform')['engagement_rate'].mean().reset_index()

    # Sort platforms by engagement
    platform_grouped = platform_grouped.sort_values('engagement_rate', ascending=False)

    # Plot
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.barplot(data=platform_grouped, x='platform', y='engagement_rate', hue='platform', palette='Set2', ax=ax, legend=False)

    ax.set_title("Average Engagement Rate per Platform", fontsize=16)
    ax.set_ylabel("Engagement Rate", fontsize=12)
    ax.set_xlabel("Platform", fontsize=12)
    ax.tick_params(axis='x', labelrotation=15)

    fig.tight_layout()
    st.pyplot(fig)

else:
    st.error("Missing required columns to compute engagement rate.")
    
st.subheader("🧬 ROAS by Persona (Category × Gender)")
heat_df = influencer_roas_df.groupby(['category', 'gender'])['roas'].mean().unstack()

fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(heat_df, annot=True, cmap="YlGnBu", fmt=".2f", ax=ax)
ax.set_title("Average ROAS by Persona")
st.pyplot(fig)

# --- Download Buttons ---
st.subheader("📥 Export Filtered Data")

def convert_df(df):
     return df.to_csv(index=False, encoding='utf-8').encode("utf-8")

col1, col2 = st.columns(2)
col1.download_button("Download Influencers", convert_df(influencers_filtered), "influencers.csv", "text/csv")
col2.download_button("Download Tracking", convert_df(tracking_filtered), "tracking.csv", "text/csv")