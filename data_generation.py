import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

np.random.seed(42)
os.makedirs("data", exist_ok=True)

def generate_influencers(n=50):
    platforms = ['Instagram', 'YouTube', 'Twitter']
    categories = ['Fitness', 'Health', 'Lifestyle']
    genders = ['Male', 'Female', 'Other']
    
    data = []
    for i in range(n):
        follower_count = np.random.randint(10000, 1000000)

        if follower_count >= 500000:
            influencer_type = 'Mega'
        elif follower_count >= 100000:
            influencer_type = 'Macro'
        elif follower_count >= 50000:
            influencer_type = 'Micro'
        else:
            influencer_type = 'Nano'

        data.append([
            i + 1,
            f"Influencer_{i+1}",
            random.choice(categories),
            random.choice(genders),
            follower_count,
            random.choice(platforms),
            influencer_type
        ])

    df = pd.DataFrame(data, columns=[
        'id', 'name', 'category', 'gender', 'follower_count', 'platform', 'influencer_type'
    ])
    df.to_csv("data/influencers.csv", index=False)
    return df

def generate_posts(influencers,n_posts=100):
    data=[]
    
    for _ in range(n_posts):
        influencer = influencers.sample(1).iloc[0]
        data.append([
            influencer['id'],
            influencer['platform'],
            datetime.today() - timedelta(days=np.random.randint(1, 90)),
            f"https://socialmedia.com/post/{np.random.randint(1000, 9999)} ",
            "Great product for health!",
            np.random.randint(1000, 50000),
            np.random.randint(100, 10000),
            np.random.randint(10, 500)
        ])
    df=pd.DataFrame(data,columns=['influencer_id', 'platform', 'date', 'url', 'caption', 'reach', 'likes', 'comments'])
    df.to_csv("data/posts.csv", index=False)
    return df

def generate_tracking_data(influencers, n_users=2500):
    data = []

    for _ in range(n_users):
        inf = influencers.sample(1).iloc[0]

        user_id = random.randint(1, 10000)
        group = random.choice([0, 1])  # 0 = control, 1 = exposed

        # Simulate revenue uplift
        if group == 1:
            revenue = round(random.uniform(300, 500), 2)  # Exposed group buys more
        else:
            revenue = round(random.uniform(20, 40), 2) 

        data.append([
            inf['platform'],
            f"Campaign_{random.randint(1, 5)}",
            inf['id'],
            user_id,
            random.choice(['MB Protein', 'HK Multivitamin', 'Gritzo Shake']),
            datetime.today() - timedelta(days=random.randint(1, 90)),
            random.randint(1, 5),
            revenue,
            group
        ])

    df = pd.DataFrame(data, columns=[
        'source', 'campaign', 'influencer_id', 'user_id',
        'product', 'date', 'orders', 'revenue', 'group'
    ])
    df.to_csv("data/tracking_data.csv", index=False, encoding='utf-8')
    return df


def generate_payouts(influencers):
    data = []
    for _, inf in influencers.iterrows():
        basis = random.choice(['post', 'order'])
        rate = round(random.uniform(100, 300), 2)
        orders = random.randint(1, 20)
        total = rate * (orders if basis == 'order' else 1)
        data.append([inf['id'], basis, rate, orders, total])
    df = pd.DataFrame(data, columns=['influencer_id', 'basis', 'rate', 'orders', 'total_payout'])
    df.to_csv("data/payouts.csv", index=False,encoding='utf-8')
    return df

if __name__ == "__main__":
    inf = generate_influencers()
    generate_posts(inf)
    generate_tracking_data(inf)
    generate_payouts(inf)
    print("Sample data generated in /data")
