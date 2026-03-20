from atproto import Client
from credentialsbsky import *
from datetime import datetime, timezone, timedelta

# -----------------------------------------------
# EDIT THIS before running each week
RECAP_INTRO = "the most popular random mgs posts in the past 7 days are..."
DRY_RUN = False
# -----------------------------------------------

client = Client()
client.login('randommetalgear.bsky.social', app_password)

cutoff = datetime.now(timezone.utc) - timedelta(days=7)

print(f"Fetching posts since {cutoff.strftime('%Y-%m-%d')}...")
all_posts = []
cursor = None
done = False

while not done:
    resp = client.get_author_feed(actor='randommetalgear.bsky.social', limit=100, cursor=cursor)
    posts = resp.feed
    if not posts:
        break
    for item in posts:
        post = item.post
        created = datetime.fromisoformat(post.record.created_at.replace('Z', '+00:00'))
        if created < cutoff:
            done = True
            break
        all_posts.append({
            'uri': post.uri,
            'cid': post.cid,
            'likes': post.like_count,
            'reposts': post.repost_count,
            'date': post.record.created_at,
        })
    cursor = resp.cursor
    if not cursor:
        break

print(f"Total posts this week: {len(all_posts)}")

now = datetime.now(timezone.utc)
min_age = timedelta(hours=6)
eligible = [p for p in all_posts if (now - datetime.fromisoformat(p['date'].replace('Z', '+00:00'))) >= min_age]

for p in eligible:
    age_hours = (now - datetime.fromisoformat(p['date'].replace('Z', '+00:00'))).total_seconds() / 3600
    p['likes_per_hour'] = p['likes'] / age_hours

by_likes = sorted(eligible, key=lambda p: p['likes'], reverse=True)
by_lph   = sorted(eligible, key=lambda p: p['likes_per_hour'], reverse=True)
likes_rank = {p['uri']: i for i, p in enumerate(by_likes, 1)}
lph_rank   = {p['uri']: i for i, p in enumerate(by_lph, 1)}
for p in eligible:
    p['avg_rank'] = (likes_rank[p['uri']] + lph_rank[p['uri']]) / 2

top5 = sorted(eligible, key=lambda p: p['avg_rank'])[:5]

print("\nTop 5 by rank averaging:")
for i, p in enumerate(top5, 1):
    print(f"{i}. avg rank {p['avg_rank']:.1f} - {p['likes']} likes, {p['likes_per_hour']:.2f}/hr - {p['date']}")
    print(f"   https://bsky.app/profile/randommetalgear.bsky.social/post/{p['uri'].split('/')[-1]}")

print("\n--- PREVIEW ---")
print(f"Intro post: {RECAP_INTRO}")
for i, p in enumerate(top5, 1):
    print(f"Reply {i}: #{i} - quote of {p['uri'].split('/')[-1]} ({p['likes']} likes, {p['likes_per_hour']:.2f}/hr)")

if not DRY_RUN:
    intro = client.send_post(text=RECAP_INTRO)
    parent = {'uri': intro.uri, 'cid': intro.cid}
    root = parent
    for i, p in enumerate(top5, 1):
        reply = client.send_post(
            text=f"#{i}",
            reply_to={'root': root, 'parent': parent},
            embed={'$type': 'app.bsky.embed.record', 'record': {'uri': p['uri'], 'cid': p['cid']}}
        )
        parent = {'uri': reply.uri, 'cid': reply.cid}
    print("Posted!")
else:
    print("(dry run - set DRY_RUN = False to post)")
