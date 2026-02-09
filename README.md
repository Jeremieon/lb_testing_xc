# F5 Distributed Cloud Test Apps

Simple FastAPI applications for learning F5XC features: routing, rewrites, mTLS, TLS, and load balancing.

## Apps Overview

| App | Port | Purpose | F5XC Learning Goal |
|-----|------|---------|-------------------|
| **Redirect App** | 8001 | Returns 3xx redirects | Learn URL rewrites, redirect handling |
| **CRUD App** | 8002 | Basic CRUD operations | URI-based routing destination |
| **Routing App** | 8003 | Multiple endpoints (/api/*, /admin/*, /public/*) | URI pattern matching, path-based routing |
| **TLS App** | 8443 | HTTPS enabled | mTLS, end-to-end TLS, SNI |

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run All Apps (separate terminals)

**Terminal 1 - Redirect App:**
```bash
uvicorn app_redirect:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - CRUD App:**
```bash
uvicorn app_crud:app --host 0.0.0.0 --port 8002 --reload
```

**Terminal 3 - Routing App:**
```bash
uvicorn app_routes:app --host 0.0.0.0 --port 8003 --reload
```

**Terminal 4 - TLS App:**
```bash
uvicorn app_tls:app --host 0.0.0.0 --port 8443 --ssl-keyfile=./certs/key.pem --ssl-certfile=./certs/cert.pem --reload
```

### 3. Test Locally

```bash
# Redirect App
curl http://localhost:8001/
curl -L http://localhost:8001/redirect-temp

# CRUD App
curl http://localhost:8002/items
curl -X POST http://localhost:8002/items -H "Content-Type: application/json" -d '{"name":"laptop","description":"Gaming laptop","price":1299.99}'

# Routing App
curl http://localhost:8003/api/users
curl http://localhost:8003/admin/dashboard
curl http://localhost:8003/old-path

# TLS App
curl -k https://localhost:8443/
curl -k https://localhost:8443/secure-data
```

## F5XC Learning Scenarios

### Scenario 1: Basic Load Balancing
- **Goal**: Deploy all 4 apps behind one F5XC Load Balancer
- **Test**: Access each app through the LB virtual host
- **Apps**: All apps on ports 8001-8003, 8443

### Scenario 2: URI-Based Routing
- **Goal**: Route to different backend apps based on URI patterns
- **Configuration**:
  - `/redirect/*` → Redirect App (8001)
  - `/items/*` → CRUD App (8002)
  - `/api/*` → Routing App (8003)
  - `/admin/*` → Routing App (8003)
  - `/public/*` → Routing App (8003)

### Scenario 3: URL Rewrites
- **Goal**: Rewrite URLs before sending to backend
- **Test Cases**:
  - Rewrite `/old-path` to `/new-path` on Routing App
  - Strip `/redirect` prefix before forwarding to Redirect App
  - Add `/items` prefix when routing to CRUD App

### Scenario 4: TLS/mTLS Configuration
- **Goal**: End-to-end encryption and mutual TLS
- **Configuration**:
  - F5XC terminates client TLS (frontend)
  - F5XC to backend uses TLS (backend TLS to port 8443)
  - Configure mTLS with client certificates
  - Test SNI for multiple hostnames

### Scenario 5: Redirect Handling (3xx)
- **Goal**: Learn how F5XC handles backend redirects
- **Test**:
  - `/redirect-temp` returns 302
  - `/redirect-perm` returns 301
  - Configure F5XC to follow or not follow redirects

## Endpoint Cheat Sheet

### Redirect App (8001)
```
GET  /                    - Root info
GET  /redirect-temp       - 302 redirect
GET  /redirect-perm       - 301 redirect
GET  /redirect-see-other  - 303 redirect
GET  /health              - Health check
```

### CRUD App (8002)
```
GET    /                  - Root info
GET    /items             - List all items
POST   /items             - Create item
GET    /items/{id}        - Get item
PUT    /items/{id}        - Update item
DELETE /items/{id}        - Delete item
GET    /health            - Health check
```

### Routing App (8003)
```
GET  /                    - Root info
GET  /api/users           - API endpoint
GET  /api/products        - API endpoint
GET  /api/orders          - API endpoint
GET  /admin/dashboard     - Admin endpoint
GET  /admin/settings      - Admin endpoint
GET  /public/info         - Public endpoint
GET  /public/contact      - Public endpoint
GET  /old-path            - Test rewrite source
GET  /new-path            - Test rewrite destination
GET  /health              - Health check
```

### TLS App (8443)
```
GET  /                    - Root info (HTTPS)
GET  /secure-data         - Secure endpoint
GET  /cert-info           - mTLS verification endpoint
GET  /health              - Health check
```

## Testing Examples

### Test CRUD Operations
```bash
# Create items
curl -X POST http://localhost:8002/items \
  -H "Content-Type: application/json" \
  -d '{"name":"laptop","description":"Gaming laptop","price":1299.99}'

curl -X POST http://localhost:8002/items \
  -H "Content-Type: application/json" \
  -d '{"name":"mouse","description":"Wireless mouse","price":29.99}'

# List items
curl http://localhost:8002/items

# Get specific item
curl http://localhost:8002/items/1

# Update item
curl -X PUT http://localhost:8002/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"laptop","description":"Updated gaming laptop","price":1199.99}'

# Delete item
curl -X DELETE http://localhost:8002/items/2
```

### Test Redirects
```bash
# See redirect without following
curl -I http://localhost:8001/redirect-temp

# Follow redirect
curl -L http://localhost:8001/redirect-temp
```

### Test TLS
```bash
# Test HTTPS (ignore self-signed cert)
curl -k https://localhost:8443/

# Test with verbose output
curl -kv https://localhost:8443/secure-data

# Check certificate
openssl s_client -connect localhost:8443 -showcerts
```

## F5XC Configuration Tips

1. **Origin Pools**: Create separate pools for each app
2. **Routes**: Use routes to match URI patterns
3. **Rewrites**: Test prefix stripping and path replacement
4. **TLS**: Configure both frontend and backend TLS
5. **Health Checks**: All apps have `/health` endpoints
6. **SNI**: Use different hostnames for TLS routing

## Next Steps for F5XC

1. Create HTTP Load Balancer in F5XC
2. Add origin pools for each backend app
3. Configure routes with URI matching
4. Set up URL rewrites
5. Enable TLS for frontend
6. Configure backend TLS to port 8443
7. Test mTLS with client certificates
8. Verify SNI-based routing

Good luck with your F5 Distributed Cloud learning! 🚀
