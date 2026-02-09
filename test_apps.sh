#!/bin/bash

echo "Testing F5XC Test Apps"
echo "======================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test Redirect App
echo "Testing Redirect App (port 8001)..."
if curl -s http://localhost:8001/health | grep -q "redirect-app"; then
    echo -e "${GREEN}✓ Redirect App is running${NC}"
else
    echo -e "${RED}✗ Redirect App is not responding${NC}"
fi

# Test CRUD App
echo "Testing CRUD App (port 8002)..."
if curl -s http://localhost:8002/health | grep -q "crud-app"; then
    echo -e "${GREEN}✓ CRUD App is running${NC}"
else
    echo -e "${RED}✗ CRUD App is not responding${NC}"
fi

# Test Routing App
echo "Testing Routing App (port 8003)..."
if curl -s http://localhost:8003/health | grep -q "routing-app"; then
    echo -e "${GREEN}✓ Routing App is running${NC}"
else
    echo -e "${RED}✗ Routing App is not responding${NC}"
fi

# Test TLS App
echo "Testing TLS App (port 8443)..."
if curl -sk https://localhost:8443/health | grep -q "tls-app"; then
    echo -e "${GREEN}✓ TLS App is running${NC}"
else
    echo -e "${RED}✗ TLS App is not responding${NC}"
fi

echo ""
echo "======================"
echo "Functional Tests"
echo "======================"

# Test redirect
echo ""
echo "Testing 302 redirect..."
REDIRECT_LOCATION=$(curl -s -I http://localhost:8001/redirect-temp | grep -i "location:" | cut -d' ' -f2 | tr -d '\r')
if [ ! -z "$REDIRECT_LOCATION" ]; then
    echo -e "${GREEN}✓ Redirect working: $REDIRECT_LOCATION${NC}"
else
    echo -e "${RED}✗ Redirect not working${NC}"
fi

# Test CRUD
echo ""
echo "Testing CRUD create..."
CREATE_RESPONSE=$(curl -s -X POST http://localhost:8002/items \
    -H "Content-Type: application/json" \
    -d '{"name":"test-item","description":"Test","price":9.99}')
if echo "$CREATE_RESPONSE" | grep -q "test-item"; then
    echo -e "${GREEN}✓ CRUD create working${NC}"
    echo "$CREATE_RESPONSE"
else
    echo -e "${RED}✗ CRUD create failed${NC}"
fi

# Test routing
echo ""
echo "Testing routing /api/users..."
API_RESPONSE=$(curl -s http://localhost:8003/api/users)
if echo "$API_RESPONSE" | grep -q "user1"; then
    echo -e "${GREEN}✓ Routing working${NC}"
    echo "$API_RESPONSE"
else
    echo -e "${RED}✗ Routing failed${NC}"
fi

echo ""
echo "======================"
echo "All tests complete!"
echo "======================"
