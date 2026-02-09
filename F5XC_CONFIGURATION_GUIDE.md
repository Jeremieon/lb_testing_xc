# F5 Distributed Cloud Configuration Guide

This guide helps you configure F5XC to work with these test apps.

## Architecture Overview

```
Internet/Client
       |
       v
  F5XC Load Balancer (HTTPS/TLS Termination)
       |
       +-- Routes & Rewrites
       |
       +-- Origin Pools
           |
           +-- Redirect App (8001)
           +-- CRUD App (8002)
           +-- Routing App (8003)
           +-- TLS App (8443) [with backend TLS]
```

## Step-by-Step Configuration

### 1. Create Origin Pools

Navigate to: **Manage > Load Balancers > Origin Pools**

#### Origin Pool 1: redirect-pool
- **Name**: `redirect-pool`
- **Origin Servers**:
  - Public DNS Name or IP: `<your-server-ip>`
  - Port: `8001`
  - Health Check: Enable on `/health`

#### Origin Pool 2: crud-pool
- **Name**: `crud-pool`
- **Origin Servers**:
  - Public DNS Name or IP: `<your-server-ip>`
  - Port: `8002`
  - Health Check: Enable on `/health`

#### Origin Pool 3: routing-pool
- **Name**: `routing-pool`
- **Origin Servers**:
  - Public DNS Name or IP: `<your-server-ip>`
  - Port: `8003`
  - Health Check: Enable on `/health`

#### Origin Pool 4: tls-pool
- **Name**: `tls-pool`
- **Origin Servers**:
  - Public DNS Name or IP: `<your-server-ip>`
  - Port: `8443`
  - **TLS Configuration**:
    - Enable TLS
    - Skip Server Verification (for self-signed cert)
    - OR upload the cert.pem to trusted CA list
  - Health Check: Enable on `/health`

### 2. Create HTTP Load Balancer

Navigate to: **Manage > Load Balancers > HTTP Load Balancers**

**Basic Configuration:**
- **Name**: `f5-test-lb`
- **Domains**: `test.example.com` (or your domain)
- **Load Balancer Type**: HTTP

**Routes Configuration:**

Add these routes in order (order matters!):

#### Route 1: TLS App
- **Matching**: 
  - Simple Route
  - Path: `/secure` (prefix match)
- **Origin Pool**: `tls-pool`
- **Route Settings**:
  - Path Rewrite: Strip prefix `/secure`

#### Route 2: Admin Routes
- **Matching**:
  - Path: `/admin` (prefix match)
- **Origin Pool**: `routing-pool`

#### Route 3: API Routes  
- **Matching**:
  - Path: `/api` (prefix match)
- **Origin Pool**: `routing-pool`

#### Route 4: Public Routes
- **Matching**:
  - Path: `/public` (prefix match)
- **Origin Pool**: `routing-pool`

#### Route 5: Items/CRUD
- **Matching**:
  - Path: `/items` (prefix match)
- **Origin Pool**: `crud-pool`

#### Route 6: Redirects
- **Matching**:
  - Path: `/redirect` (prefix match)
- **Origin Pool**: `redirect-pool`

#### Default Route
- **Origin Pool**: `routing-pool` (or landing page)

### 3. Enable TLS/HTTPS

**Option A: Let F5XC manage certificates**
- Enable "Automatic Certificate Management"
- F5XC will provision Let's Encrypt cert

**Option B: Upload your own certificate**
- Navigate to: **Manage > Certificates**
- Upload your certificate and private key
- Reference it in the Load Balancer config

### 4. Advanced Features to Test

#### URL Rewrites
Add to specific routes:
```
Path Rewrite Examples:
- Strip Prefix: /api → / (removes /api before forwarding)
- Regex Replace: /old/(.*) → /new/$1
```

#### Header Manipulation
Add custom headers:
```
Request Headers:
- X-Forwarded-Proto: https
- X-App-Name: my-app

Response Headers:
- X-Served-By: F5XC
```

#### Rate Limiting
```
- Navigate to route settings
- Enable Rate Limiting
- Set: 100 requests per minute
```

#### CORS Settings
```
- Enable CORS
- Allowed Origins: *
- Allowed Methods: GET, POST, PUT, DELETE
- Allowed Headers: Content-Type
```

#### mTLS Configuration
```
- Navigate to Load Balancer settings
- Client Certificate Validation: Enable
- Upload CA certificate
- Set validation mode: Require Valid Certificate
```

### 5. Testing Your Configuration

#### Test Basic Routing
```bash
# Test routing to CRUD app
curl https://test.example.com/items

# Test routing to API endpoints
curl https://test.example.com/api/users

# Test routing to admin
curl https://test.example.com/admin/dashboard
```

#### Test Rewrites
```bash
# If you configured strip prefix on /api
curl https://test.example.com/api/users
# Should route to routing-pool as /users (prefix stripped)

# Test old-path to new-path rewrite
curl https://test.example.com/old-path
```

#### Test TLS Backend
```bash
# Should proxy HTTPS to backend
curl https://test.example.com/secure/secure-data
```

#### Test Redirects
```bash
# Should return 302
curl -I https://test.example.com/redirect/redirect-temp
```

#### Test mTLS (if configured)
```bash
# Generate client certificate
openssl req -x509 -newkey rsa:2048 -keyout client-key.pem \
  -out client-cert.pem -days 365 -nodes

# Test with client cert
curl --cert client-cert.pem --key client-key.pem \
  https://test.example.com/secure/cert-info
```

## Common Use Cases

### Use Case 1: Microservices Gateway
Route different microservices based on URI:
- `/auth/*` → Auth service
- `/users/*` → User service  
- `/orders/*` → Order service

### Use Case 2: Blue/Green Deployment
- Create two origin pools (blue, green)
- Route percentage of traffic to each
- Gradually shift traffic to green

### Use Case 3: API Versioning
```
/v1/api/* → v1-pool
/v2/api/* → v2-pool
/api/* → latest-pool
```

### Use Case 4: Legacy App Migration
```
/old-path → Rewrite to /new-path
/legacy/* → Strip /legacy, route to new-app-pool
```

## Monitoring & Troubleshooting

### View Analytics
- Navigate to: **Performance > Dashboards**
- Select your Load Balancer
- View: Requests, Response Time, Error Rates

### Debug Mode
- Enable debug headers to see routing decisions
- Check F5XC logs for routing issues

### Common Issues

**Issue**: Backend health check failing
- **Solution**: Verify backend is reachable on health check port
- Check firewall rules allow F5XC to reach backend

**Issue**: TLS handshake errors
- **Solution**: Verify cert matches domain name
- Check TLS version compatibility

**Issue**: Routing not working as expected
- **Solution**: Check route order (first match wins)
- Verify path matching (exact vs prefix)

**Issue**: mTLS not validating
- **Solution**: Ensure client cert is signed by uploaded CA
- Check certificate chain is complete

## Security Best Practices

1. **Always use HTTPS** on the frontend
2. **Enable WAF** (Web Application Firewall)
3. **Configure rate limiting** to prevent abuse
4. **Use mTLS** for sensitive services
5. **Restrict origin access** (firewall backend to only allow F5XC)
6. **Enable DDoS protection**
7. **Use API tokens** for service mesh communication

## Next Steps

1. ✅ Deploy the test apps
2. ✅ Create origin pools in F5XC
3. ✅ Configure HTTP Load Balancer
4. ✅ Set up routing rules
5. ✅ Test each route
6. ✅ Configure TLS/mTLS
7. ✅ Test backend TLS
8. ✅ Implement rewrites
9. ✅ Test SNI routing
10. ✅ Monitor and optimize

Happy learning! 🚀
