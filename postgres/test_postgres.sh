#!/bin/bash

echo "Testing PostgreSQL Instances for F5XC TCP Load Balancing"
echo "========================================================="
echo ""

# Test PostgreSQL 1
echo "Testing PostgreSQL Instance 1 (port 5432)..."
docker exec f5-postgres-1 psql -U f5user -d f5testdb -c "SELECT 'Postgres-1 is healthy' as status, version();"

echo ""

# Test PostgreSQL 2
echo "Testing PostgreSQL Instance 2 (port 5433)..."
docker exec f5-postgres-2 psql -U f5user -d f5testdb -c "SELECT 'Postgres-2 is healthy' as status, version();"

echo ""
echo "========================================================="
echo "Connection Strings for F5XC TCP Load Balancer:"
echo "========================================================="
echo "PostgreSQL 1: postgresql://f5user:f5password@<server-ip>:5432/f5testdb"
echo "PostgreSQL 2: postgresql://f5user:f5password@<server-ip>:5433/f5testdb"
echo ""
echo "For F5XC Origin Pool, use:"
echo "  - Server 1: <server-ip>:5432"
echo "  - Server 2: <server-ip>:5433"
echo "  - Health Check: TCP port check on 5432/5433"
