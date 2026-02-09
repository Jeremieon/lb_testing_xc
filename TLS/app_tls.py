"""
TLS App - HTTPS enabled app for testing mTLS and end-to-end encryption
Run with: uvicorn app_tls:app --host 0.0.0.0 --port 8443 --ssl-keyfile=./certs/key.pem --ssl-certfile=./certs/cert.pem
"""
from fastapi import FastAPI, Header
from typing import Optional

app = FastAPI(title="TLS App")

@app.get("/")
async def root():
    return {
        "app": "tls-app",
        "message": "This app runs on HTTPS",
        "tls_enabled": True
    }

@app.get("/secure-data")
async def secure_data(x_forwarded_proto: Optional[str] = Header(None)):
    """Returns secure data - check if request came through HTTPS"""
    return {
        "app": "tls-app",
        "endpoint": "/secure-data",
        "protocol": x_forwarded_proto or "direct-https",
        "message": "Sensitive data delivered over TLS"
    }

@app.get("/cert-info")
async def cert_info(
    x_client_cert: Optional[str] = Header(None),
    x_ssl_client_dn: Optional[str] = Header(None)
):
    """Display client certificate info if mTLS is configured"""
    return {
        "app": "tls-app",
        "endpoint": "/cert-info",
        "client_cert_present": x_client_cert is not None,
        "client_dn": x_ssl_client_dn,
        "message": "Use this endpoint to verify mTLS configuration"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "app": "tls-app", "tls": True}
