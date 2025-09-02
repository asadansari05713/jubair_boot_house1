#!/usr/bin/env python3
"""
Vercel Deployment Preparation Script for Jubair Boot House
This script helps prepare your project for Vercel deployment
"""

import os
import sys
import shutil
from pathlib import Path

def check_vercel_files():
    """Check if all required Vercel files exist"""
    print("Checking Vercel deployment files...")
    
    required_files = [
        "vercel.json",
        "vercel_main.py", 
        "requirements-vercel.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All Vercel files are present!")
    return True

def check_project_structure():
    """Check if project structure is correct for Vercel"""
    print("\n🏗️  Checking project structure...")
    
    required_dirs = [
        "app",
        "static", 
        "templates"
    ]
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            print(f"✅ {dir_name}/ directory")
        else:
            print(f"❌ {dir_name}/ directory missing")
            return False
    
    print("✅ Project structure is correct!")
    return True

def generate_secret_key():
    """Generate a secure secret key for Vercel"""
    print("\n🔑 Generating secure secret key...")
    
    try:
        import secrets
        secret_key = secrets.token_urlsafe(32)
        print(f"✅ Generated SECRET_KEY: {secret_key}")
        
        # Save to a file for easy copying
        with open("vercel_secret_key.txt", "w", encoding="utf-8") as f:
            f.write(f"SECRET_KEY={secret_key}\n")
            f.write("ENVIRONMENT=production\n")
            f.write("DEBUG=false\n")
        
        print("📝 Secret key saved to 'vercel_secret_key.txt'")
        print("💡 Copy these environment variables to Vercel dashboard")
        
        return secret_key
    except Exception as e:
        print(f"❌ Error generating secret key: {e}")
        return None

def create_deployment_checklist():
    """Create a deployment checklist"""
    print("\n📋 Creating deployment checklist...")
    
    checklist_content = """# Vercel Deployment Checklist

## ✅ Pre-Deployment
- [ ] All Vercel files are present (vercel.json, vercel_main.py, requirements-vercel.txt)
- [ ] Project structure is correct (app/, static/, templates/)
- [ ] Code is pushed to GitHub
- [ ] Secret key is generated

## 🏗️ Deployment Steps
1. [ ] Go to [vercel.com](https://vercel.com) and sign up/login
2. [ ] Click "New Project"
3. [ ] Import your GitHub repository
4. [ ] Configure project settings
5. [ ] Click "Deploy"
6. [ ] Add environment variables:
   - ENVIRONMENT=production
   - DEBUG=false
   - SECRET_KEY=[your-generated-key]
7. [ ] Redeploy with environment variables

## 🧪 Post-Deployment Testing
- [ ] App is accessible at Vercel URL
- [ ] Health endpoint (/health) works
- [ ] Home page loads correctly
- [ ] All navigation works
- [ ] User registration works
- [ ] Admin login works

## 🔧 Environment Variables for Vercel
```
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=[your-secret-key-here]
```

## 📱 Your Vercel URL
After deployment, your app will be available at:
`https://your-project-name.vercel.app`

## 🚨 Important Notes
- Vercel uses serverless functions (no persistent storage)
- Database resets on each deployment
- Cold starts may cause initial delays
- Perfect for demos and testing
- Consider external database for production data

---
**Happy deploying on Vercel! 🚀**
"""
    
    with open("VERCEL-CHECKLIST.md", "w", encoding="utf-8") as f:
        f.write(checklist_content)
    
    print("✅ Deployment checklist created: 'VERCEL-CHECKLIST.md'")

def main():
    """Main deployment preparation function"""
    print("🚀 Vercel Deployment Preparation for Jubair Boot House")
    print("=" * 60)
    
    # Check all requirements
    if not check_vercel_files():
        print("\n❌ Please create missing Vercel files before deployment")
        return False
    
    if not check_project_structure():
        print("\n❌ Please fix project structure before deployment")
        return False
    
    # Generate secret key
    secret_key = generate_secret_key()
    if not secret_key:
        print("\n❌ Failed to generate secret key")
        return False
    
    # Create deployment checklist
    create_deployment_checklist()
    
    print("\n" + "=" * 60)
    print("🎉 Vercel deployment preparation completed!")
    print("\n📝 Next steps:")
    print("1. Push your code to GitHub")
    print("2. Go to vercel.com and create account")
    print("3. Import your repository")
    print("4. Deploy with the generated environment variables")
    print("\n📋 Check 'VERCEL-CHECKLIST.md' for detailed steps")
    print("🔑 Check 'vercel_secret_key.txt' for environment variables")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
