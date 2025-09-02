"""
Vercel-optimized main file for Jubair Boot House
This file is specifically designed for Vercel's serverless deployment
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from fastapi import FastAPI, Request, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_db, test_connection, init_db
from app.routers import auth, products
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session

# Create FastAPI app
app = FastAPI(
    title="Jubair Boot House",
    description="Professional footwear store with admin management",
    version="1.0.0"
)

# Add CORS middleware for Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (Vercel will serve these from public directory)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(products.router)

# Templates
templates = Jinja2Templates(directory="templates")

# Note: Session management is handled client-side via JavaScript

@app.on_event("startup")
async def startup_event():
    """Initialize database and other services on startup"""
    print("🚀 Starting Jubair Boot House on Vercel...")
    
    # For Vercel, we'll use SQLite (no external database connections)
    print("💻 Vercel mode: Using SQLite database")
    
    # Test database connection
    if test_connection():
        print("✅ SQLite connection established")
        
        # Ensure tables exist
        if init_db():
            print("✅ SQLite tables verified/created")
        else:
            print("⚠️  SQLite table initialization had issues")
    else:
        print("❌ SQLite connection failed - app will continue with limited functionality")

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        db_status = "connected" if test_connection() else "disconnected"
        
        return {
            "status": "healthy" if db_status == "connected" else "warning",
            "database": {
                "type": "SQLite",
                "status": db_status
            },
            "environment": "vercel",
            "platform": "serverless",
            "app": "Jubair Boot House",
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e), 
            "environment": "vercel"
        }

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Home page with hero banner and categories"""
    return templates.TemplateResponse("home.html", {
        "request": request
    })

@app.get("/catalog", response_class=HTMLResponse)
async def catalog_redirect(request: Request):
    """Redirect /catalog to /products/"""
    return RedirectResponse(url="/products/")

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard_redirect(request: Request):
    """Redirect /admin/dashboard to /products/admin/dashboard"""
    return RedirectResponse(url="/products/admin/dashboard")

@app.get("/admin/users", response_class=HTMLResponse)
async def admin_users_redirect(request: Request):
    """Redirect /admin/users to /auth/admin/users"""
    return RedirectResponse(url="/auth/admin/users")

@app.get("/size-guide", response_class=HTMLResponse)
async def size_guide_page(request: Request):
    """Size guide page with shoe sizing information"""
    return templates.TemplateResponse("size_guide.html", {
        "request": request
    })

@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    """Contact page with contact form and information"""
    return templates.TemplateResponse("contact.html", {
        "request": request
    })

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """About page with company information"""
    return templates.TemplateResponse("about.html", {
        "request": request
    })

@app.get("/faq", response_class=HTMLResponse)
async def faq_page(request: Request):
    """FAQ page with frequently asked questions"""
    return templates.TemplateResponse("faq.html", {
        "request": request
    })

@app.get("/terms", response_class=HTMLResponse)
async def terms_page(request: Request):
    """Terms and conditions page"""
    return templates.TemplateResponse("terms.html", {
        "request": request
    })

@app.get("/privacy", response_class=HTMLResponse)
async def privacy_page(request: Request):
    """Privacy policy page"""
    return templates.TemplateResponse("privacy.html", {
        "request": request
    })

@app.get("/cookies", response_class=HTMLResponse)
async def cookies_page(request: Request):
    """Cookies policy page"""
    return templates.TemplateResponse("cookies.html", {
        "request": request
    })

@app.get("/returns", response_class=HTMLResponse)
async def returns_page(request: Request):
    """Returns and refunds page"""
    return templates.TemplateResponse("returns.html", {
        "request": request
    })

@app.get("/shipping", response_class=HTMLResponse)
async def shipping_page(request: Request):
    """Shipping information page"""
    return templates.TemplateResponse("shipping.html", {
        "request": request
    })

# Vercel requires this for serverless deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
