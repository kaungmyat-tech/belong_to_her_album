# GitHub Pages Deployment Guide

## 🚀 Deploy Your Love Story Website to GitHub Pages

### 📋 Prerequisites
- GitHub account
- Git installed on your computer
- Your project files ready

### 🔧 Step 1: Set Up GitHub Authentication

#### Option A: Using Personal Access Token (Recommended)
1. **Generate Personal Access Token:**
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Give it a name (e.g., "Website Deployment")
   - Select scopes: `repo` (Full control of private repositories)
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again)

2. **Configure Git with Token:**
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/kaungmyat-tech/belong_to_her_album.git
   ```
   Replace `YOUR_TOKEN` with the actual token you copied.

#### Option B: Using GitHub CLI (Alternative)
```bash
# Install GitHub CLI if not already installed
# Then authenticate
gh auth login
```

### 📤 Step 2: Push to GitHub

```bash
# Push your changes
git push -u origin main
```

### 🌐 Step 3: Enable GitHub Pages

1. **Go to your repository:** https://github.com/kaungmyat-tech/belong_to_her_album
2. **Click Settings** tab
3. **Scroll down to "Pages" section**
4. **Source:** Select "Deploy from a branch"
5. **Branch:** Select `main`
6. **Folder:** Select `/ (root)`
7. **Click "Save"**

### ⏱️ Step 4: Wait for Deployment

- GitHub will build and deploy your site
- This usually takes 1-2 minutes
- You'll see a green checkmark when ready

### 🎯 Step 5: Access Your Website

Your website will be available at:
```
https://kaungmyat-tech.github.io/belong_to_her_album/
```

### 📁 Important Files for Your Website

Make sure these files are in your repository:
- `this_is_belong_to_her.html` (Main webpage)
- `media_links.json` (Gallery data)
- All CSS and JavaScript are embedded in the HTML

### 🎵 Music Files

The music files are already hosted on Cloudinary, so they don't need to be in your GitHub repository.

### 📱 Mobile Optimization

Your website is already optimized for mobile devices with:
- Responsive design
- Touch-friendly controls
- Mobile-optimized navigation

### 🔄 Updates

To update your website:
```bash
# Make changes to your files
git add .
git commit -m "Your update message"
git push origin main
```

GitHub Pages will automatically redeploy your site.

### 🎨 Features Included

✅ **Hanging Navigation Tabs** with ropes and glowing bulbs  
✅ **5 Romantic Music Tracks** from Cloudinary  
✅ **Photo Gallery** with 40+ images  
✅ **Mobile Responsive Design**  
✅ **Anniversary Counter**  
✅ **Love Letter Section**  
✅ **Secret Garden** with unlockable poem  
✅ **Timeline** of your relationship  
✅ **Lightbox** for photo viewing  

### 🐛 Troubleshooting

**If deployment fails:**
1. Check your GitHub token has `repo` permissions
2. Ensure your main branch is pushed
3. Wait a few minutes and try again

**If music doesn't play:**
1. Check browser console for errors
2. Try clicking anywhere on the page to start music
3. Ensure Cloudinary URLs are accessible

**If styles don't load:**
1. Check that all CSS is embedded in the HTML
2. Clear browser cache and reload

### 🎉 Success!

Once deployed, your romantic love story website will be live for the world to see! 💕

---

**Your Website URL:** https://kaungmyat-tech.github.io/belong_to_her_album/
