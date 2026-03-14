import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import json

# Configure Cloudinary (using your existing credentials)
cloudinary.config(
    cloud_name="dr0q4kzis",
    api_key="172828671911916",
    api_secret="_qJqdqGUBqz_jbj_9byyvzBghhI"
)

def upload_music_files():
    music_folder = "music"
    uploaded_files = []
    
    # List of music files
    music_files = [
        "deltax-music-honey-kisses-413841.mp3",
        "nastelbom-romantic-436840.mp3", 
        "paulyudin-romantic-romantic-music-493488.mp3",
        "solarflex-romantic-495654.mp3",
        "the_mountain-inspirational-piano-romantic-375982.mp3"
    ]
    
    print("Starting upload of music files to Cloudinary...")
    
    for filename in music_files:
        file_path = os.path.join(music_folder, filename)
        
        if os.path.exists(file_path):
            try:
                print(f"Uploading {filename}...")
                
                # Upload to Cloudinary as raw file (for audio)
                response = cloudinary.uploader.upload(
                    file_path,
                    resource_type="raw",  # Important for audio files
                    folder="romantic_music",
                    use_filename=True,
                    unique_filename=False,
                    overwrite=True
                )
                
                # Get the permanent URL
                url = response.get('secure_url')
                public_id = response.get('public_id')
                
                uploaded_files.append({
                    "filename": filename,
                    "public_id": public_id,
                    "url": url,
                    "size": os.path.getsize(file_path)
                })
                
                print(f"✅ Uploaded: {filename}")
                print(f"   URL: {url}")
                print(f"   Public ID: {public_id}")
                print()
                
            except Exception as e:
                print(f"❌ Error uploading {filename}: {str(e)}")
        else:
            print(f"❌ File not found: {file_path}")
    
    # Save the results to a JSON file
    with open("music_links.json", "w") as f:
        json.dump(uploaded_files, f, indent=2)
    
    print(f"✅ Upload complete! {len(uploaded_files)} files uploaded.")
    print("📁 Results saved to: music_links.json")
    
    # Print summary
    print("\n📋 Summary:")
    for i, file_info in enumerate(uploaded_files, 1):
        print(f"{i}. {file_info['filename']}")
        print(f"   URL: {file_info['url']}")
    
    return uploaded_files

if __name__ == "__main__":
    # Note: You need to install cloudinary first: pip install cloudinary
    uploaded_files = upload_music_files()
