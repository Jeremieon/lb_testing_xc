"""
Path-Based Routing App - Different endpoints for URI-based routing practice
Run with: uvicorn app_routes:app --host 0.0.0.0 --port 8003
"""
from fastapi import FastAPI

app = FastAPI(title="Routing App")

@app.get("/")
async def root():
    return {"app": "routing-app", "message": "Try /api/*, /admin/*, /public/* endpoints"}

# API endpoints
@app.get("/api/users")
async def api_users():
    return {"app": "routing-app", "endpoint": "/api/users", "data": ["user1", "user2", "user3"]}

@app.get("/api/products")
async def api_products():
    return {"app": "routing-app", "endpoint": "/api/products", "data": ["laptop", "phone", "tablet"]}

@app.get("/api/orders")
async def api_orders():
    return {"app": "routing-app", "endpoint": "/api/orders", "data": ["order123", "order456"]}

# Admin endpoints
@app.get("/admin/dashboard")
async def admin_dashboard():
    return {"app": "routing-app", "endpoint": "/admin/dashboard", "message": "Admin Dashboard"}

@app.get("/admin/settings")
async def admin_settings():
    return {"app": "routing-app", "endpoint": "/admin/settings", "message": "Admin Settings"}

# Public endpoints
@app.get("/public/info")
async def public_info():
    return {"app": "routing-app", "endpoint": "/public/info", "message": "Public Information"}

@app.get("/public/contact")
async def public_contact():
    return {"app": "routing-app", "endpoint": "/public/contact", "message": "Contact Us"}

# Special endpoint for testing rewrites
@app.get("/old-path")
async def old_path():
    return {"app": "routing-app", "endpoint": "/old-path", "message": "This is the old path - test rewrite to /new-path"}

@app.get("/new-path")
async def new_path():
    return {"app": "routing-app", "endpoint": "/new-path", "message": "Successfully rewritten to new path!"}

@app.get("/health")
async def health():
    return {"status": "healthy", "app": "routing-app"}
