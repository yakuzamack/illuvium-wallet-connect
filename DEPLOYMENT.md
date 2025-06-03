# Deployment Guide

## Repository Information
- **GitHub Repository**: https://github.com/yakuzamack/illuvium-wallet-connect
- **Project Type**: Flask Python Web Application
- **Description**: Illuvium Web Application with Wallet Connect Integration

## Files Included in Deployment

### Core Application Files
- `app.py` - Main Flask application (2015 lines)
- `wsgi.py` - WSGI entry point for production
- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel deployment configuration

### Templates and Static Assets
- `templates/` - HTML templates (index.html, autodrone.html, 403.html)
- `static/` - Static assets (CSS, JS, images)
- `images/` - Game assets and graphics
- `_next/` - Next.js style assets

### Configuration Files
- `.gitignore` - Git ignore patterns
- `render.yaml` - Alternative Render.com deployment config
- `README.md` - Project documentation

## Vercel Deployment Instructions

### Method 1: Deploy via Vercel Dashboard (Recommended)
1. Go to [vercel.com](https://vercel.com) and sign in with your GitHub account
2. Click "New Project"
3. Import the repository: `yakuzamack/illuvium-wallet-connect`
4. Vercel will automatically detect it's a Python project
5. Configure deployment settings:
   - **Framework Preset**: Other
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
   - **Install Command**: `pip install -r requirements.txt`
6. Click "Deploy"

### Method 2: Deploy via Vercel CLI
```bash
npm i -g vercel
vercel login
cd /path/to/your/project
vercel --prod
```

### Method 3: Connect to Existing Repository
1. Fork or clone the repository: https://github.com/yakuzamack/illuvium-wallet-connect
2. Follow Method 1 with your forked repository

## Environment Variables (Optional)
If needed, you can add these environment variables in Vercel:
- `FLASK_ENV=production`
- `DEBUG_MODE=false`

## Expected Deployment URL
After successful deployment, your app will be available at:
`https://your-project-name.vercel.app`

## Features Deployed
- ✅ Wallet Connect Modal functionality
- ✅ Proxy functionality for Illuvium content
- ✅ Static standalone version
- ✅ CORS and permission policy fixes
- ✅ All static assets (images, CSS, JS)

## Troubleshooting

### Common Issues:
1. **Build Timeout**: Vercel has a 10-minute build limit. Our `vercel.json` is configured for this.
2. **Large Assets**: Some image assets are large. Consider using Vercel's image optimization.
3. **Function Size**: The app is configured with appropriate function limits.

### Alternative Deployment Options:
- **Render.com**: Use the included `render.yaml` file
- **Railway**: Push the repository to Railway
- **PythonAnywhere**: Upload files manually

## Support
- Repository: https://github.com/yakuzamack/illuvium-wallet-connect
- Original Documentation: See `README.md` in the repository

## Version Information
- Flask: 2.3.3
- Python: 3.7+
- Deployment Date: $(date)
- Last Updated: June 2025 