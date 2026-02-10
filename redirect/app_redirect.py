"""
Redirect App - Returns 3xx redirects for testing F5 rewrites
Run with: uvicorn app_redirect:app --host 0.0.0.0 --port 8001
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(title="Redirect App")


@app.get("/")
async def root():
    return {
        "app": "redirect-app",
        "message": "Click /redirect-temp or /redirect-perm to test redirects",
    }


@app.get("/redirect-temp")
async def redirect_temporary():
    """Returns 302 temporary redirect"""
    return RedirectResponse(url="https://crud.labtestdemo.com/items", status_code=302)


@app.get("/redirect-perm")
async def redirect_permanent():
    """Returns 301 permanent redirect"""
    return RedirectResponse(url="https://crud.labtestdemo.com/items", status_code=301)


@app.get("/redirect-see-other")
async def redirect_see_other():
    """Returns 303 See Other redirect"""
    return RedirectResponse(url="https://crud.labtestdemo.com", status_code=303)


@app.get("/health")
async def health():
    return {"status": "healthy", "app": "redirect-app"}
