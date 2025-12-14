import json
import os

from app.db import SessionLocal
from app.models import User

# NOTE: Env variables should be configured within dedicated Config Class
USER_JSON_PATH = os.getenv("USER_DATA", "user_data/user_data.json")


def migrate_users():
    print("MIGRATION SCRIPT STARTED")

    with open(USER_JSON_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    session = SessionLocal()
    count = 0
    skipped = 0

    targets = data.get("targets", {})
    print(f"Found {len(targets)} interaction records.")

    seen_uids = set()

    for path in targets.keys():
        parts = path.split("/")

        # "users/05IsdAyoSnekvovtyr2fC5cNOnF3/subjectsWeb/aqaGCSEBio/mocks/medlymockaqaGCSEBio_Sept_Mock1Higher/questions/aqaGCSEBio_1_1_1_EBc0BgD11T"
        if len(parts) < 2 or parts[0] != "users":
            skipped += 1
            continue

        firebase_uid = parts[1]
        if firebase_uid in seen_uids:
            continue

        seen_uids.add(firebase_uid)    
        
        user_exists = (
            session.query(User)
            .filter(User.firebase_uid == firebase_uid)
            .first()
        )

        if user_exists:
            skipped += 1
            continue

        user = User(id=count, firebase_uid=firebase_uid)
        session.add(user)
        count += 1


    session.commit()
    print(f"Inserted {count} new users to database.")
    print(f"Skipped {skipped} existing/invalid users.")
    

if __name__ == "__main__":
    migrate_users()

