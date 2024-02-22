import pandas as pd

data = pd.read_csv('./data/[Reddit] polestar_posts_comments by praw.csv')

keywords = [
    "seat", "Leather ", "chair", "Driver's seat", "Passenger seat", "Rear seat", "Headliner", "Roof lining", "overhead interior", "interior", "Footwells",
    "pillar", "A pillar", "B Pillar", "C Pillar", "Frunk", "Trunk", "Lighting",
    "Steering wheel", "Dashboard (instrument panel)", "Airbags", "HMI screen",
    "Centre arm rest", "holder", "Cup holder", "Phone holder", "Door panel", "door",
    "Door arm rest", "Door bin",
]

def check_keywords(text, keywords):
    text = text if pd.notna(text) else ""
    return any(keyword in text for keyword in keywords)

data['keywords_present'] = data['comment_body'].apply(lambda text: check_keywords(text, keywords))

entries_to_drop = data[~data['keywords_present']].index
filtered_data = data.drop(entries_to_drop).reset_index(drop=True)
original_shape = data.shape
filtered_shape = filtered_data.shape
original_shape, filtered_shape