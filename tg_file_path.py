import requests
import json
import time
import os
import signal
import sys

# --- CONFIGURATION ---
TOKEN = "8634969910:AAGzZUoWYXhjIOGig-86hou1UQFtevSKcuw"
# Cloudinary Dashboard ကအချက်အလက်များကို အောက်တွင် ထည့်သွင်းထားသည်
CLOUDINARY_CLOUD_NAME = "dxovof71b"
CLOUDINARY_API_KEY = "172828671911916"
CLOUDINARY_API_SECRET = "_qJqdqGUBqz_jbj_9byyvzBghhI"

BASE = f"https://api.telegram.org/bot{TOKEN}"

if not os.path.exists("media_files"):
    os.makedirs("media_files")

processed = set()
last_update_id = 0  # Update အဟောင်းတွေ ထပ်မဖတ်မိစေဖို့

# Global flag for graceful shutdown
shutdown_requested = False

def signal_handler(signum, frame):
    global shutdown_requested
    print("\nShutdown signal received. Cleaning up...")
    shutdown_requested = True

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def upload_to_cloudinary(file_path):
    """Cloudinary ကို ပုံ/ဗီဒီယို တင်ပြီး Permanent link ယူမည့် function"""
    url = f"https://api.cloudinary.com/v1_1/{CLOUDINARY_CLOUD_NAME}/auto/upload"

    files = {"file": open(file_path, "rb")}
    payload = {
        "upload_preset": "ml_default",
        "api_key": CLOUDINARY_API_KEY,
    }

    try:
        # Timeout ထည့်ထားခြင်းဖြင့် အကြာကြီး ရပ်မနေစေရန်
        response = requests.post(url, data=payload, files=files, timeout=30)
        data = response.json()
        if "secure_url" in data:
            return data.get("secure_url")
        else:
            print(f"Cloudinary response error: {data}")
            return None
    except Exception as e:
        print(f"Cloudinary Error: {e}")
        return None


print("Monitoring Telegram Channel for media...")
print("Press Ctrl+C to stop safely")

# Counter for debugging
loop_count = 0
no_updates_count = 0

while not shutdown_requested:
    try:
        loop_count += 1
        print(f"Loop #{loop_count} - Checking for updates...")
        
        # offset သုံးပြီး update အသစ်ကိုပဲ ယူမယ်
        params = {"timeout": 10, "offset": last_update_id + 1, "limit": 10}
        
        try:
            response = requests.get(BASE + "/getUpdates", params=params, timeout=15)
            if response.status_code != 200:
                print(f"HTTP Error {response.status_code}: {response.text}")
                time.sleep(5)
                continue
                
            updates = response.json()
            
            if "result" not in updates:
                print("Invalid response format")
                time.sleep(5)
                continue
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(10)
            continue

        if not updates["result"]:
            no_updates_count += 1
            print(f"No new updates ({no_updates_count} consecutive). Waiting...")
            if no_updates_count >= 6:  # After 1 minute of no updates
                print("Taking longer pause - no recent activity")
                time.sleep(30)
                no_updates_count = 0
            else:
                time.sleep(10)
            continue
            
        # Reset counter when we get updates
        no_updates_count = 0

        for item in updates["result"]:
            last_update_id = item["update_id"]  # နောက်ဆုံးရတဲ့ id ကို မှတ်ထားမယ်

            msg = item.get("message") or item.get("channel_post")
            if not msg:
                continue

            file_id = None
            ext = ""
            if "photo" in msg:
                file_id = msg["photo"][-1]["file_id"]
                ext = ".jpg"
            elif "video" in msg:
                file_id = msg["video"]["file_id"]
                ext = ".mp4"

            if not file_id or file_id in processed:
                continue
            processed.add(file_id)

            print(f"New media found! Fetching file path...")
            try:
                file_data = requests.get(
                    BASE + f"/getFile?file_id={file_id}", timeout=10
                ).json()

                if "result" not in file_data:
                    print("Failed to get file path from Telegram.")
                    continue

                file_path = file_data["result"]["file_path"]
                download_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

                filename = f"temp_{int(time.time())}{ext}"
                local_path = os.path.join("media_files", filename)

                print(f"Downloading from Telegram: {file_path}")
                file_content = requests.get(download_url, timeout=20)
                file_content.raise_for_status()
                
                with open(local_path, "wb") as f:
                    f.write(file_content.content)

                print(f"Uploading to Cloudinary...")
                permanent_url = upload_to_cloudinary(local_path)

                if permanent_url:
                    entry = {"timestamp": time.ctime(), "url": permanent_url}
                    with open("media_links.json", "a") as f:
                        f.write(json.dumps(entry) + "\n")
                    print(f"Done! Saved: {permanent_url}")
                else:
                    print("Upload failed.")
                    
                # Clean up temp file
                try:
                    os.remove(local_path)
                except:
                    pass
                    
            except Exception as e:
                print(f"Error processing media: {e}")
                continue

        print(f"Processed {len(updates['result'])} updates. Waiting for next check...")
        time.sleep(3)  # Shorter wait between checks

    except requests.exceptions.ReadTimeout:
        print("Timeout waiting for updates. Continuing...")
        time.sleep(5)
        continue
    except KeyboardInterrupt:
        print("\nShutdown requested by user.")
        break
    except Exception as e:
        print(f"Main Loop Error: {e}")
        print("Continuing after 5 seconds...")
        time.sleep(5)

print("Script stopped safely.")
