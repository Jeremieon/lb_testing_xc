# F5 Distributed Cloud - TCP Load Balancer Setup (PostgreSQL)

## Quick Start

**1. Start PostgreSQL instances:**
```bash
docker-compose -f docker-compose-postgres.yml up -d --build
```

**2. Verify both instances are running:**
```bash
docker ps | grep postgres
./test_postgres.sh
```

**3. Test connections locally:**
```bash
# Connect to PostgreSQL 1
psql -h localhost -p 5432 -U f5user -d f5testdb

# Connect to PostgreSQL 2
psql -h localhost -p 5433 -U f5user -d f5testdb

# Or using Docker exec
docker exec -it f5-postgres-1 psql -U f5user -d f5testdb
docker exec -it f5-postgres-2 psql -U f5user -d f5testdb
```

## F5XC TCP Load Balancer Configuration

### Step 1: Create Origin Pool (TCP)

Navigate to: **Manage > Load Balancers > Origin Pools**

**Configuration:**
- **Name**: `postgres-tcp-pool`
- **Origin Servers**:
  - **Server 1**: 
    - IP/DNS: `<your-server-ip>`
    - Port: `5432`
  - **Server 2**:
    - IP/DNS: `<your-server-ip>`
    - Port: `5433`
- **Port**: `5432` (default PostgreSQL)
- **Health Check**:
  - **Type**: TCP Health Check
  - **Interval**: 10 seconds
  - **Timeout**: 5 seconds
  - **Unhealthy Threshold**: 3
  - **Healthy Threshold**: 2

### Step 2: Create TCP Load Balancer

Navigate to: **Manage > Load Balancers > TCP Load Balancers**

**Configuration:**
- **Name**: `postgres-lb`
- **Listen Port**: `5432`
- **Domain**: `postgres.labtestdemo.com` (optional)
- **Origin Pools**: Select `postgres-tcp-pool`
- **Load Balancing Algorithm**: 
  - Round Robin (default)
  - OR Least Connections (better for long DB connections)

### Step 3: Configure Advanced Settings (Optional)

**Connection Timeout:**
- **Idle Timeout**: 3600 seconds (1 hour for long DB connections)
- **Max Connect Attempts**: 1

**TLS (if needed for encrypted PostgreSQL):**
- Frontend TLS: Terminate client TLS connections
- Backend TLS: Connect to PostgreSQL over TLS

### Step 4: Test the Load Balancer

**Test connection through F5XC:**
```bash
# Get F5XC Load Balancer endpoint
# Example: postgres-lb.tenant.xcnet.io or your custom domain

# Connect through F5XC LB
psql -h <f5xc-lb-endpoint> -p 5432 -U f5user -d f5testdb

# Test load balancing - run multiple connections
for i in {1..10}; do
  psql -h <f5xc-lb-endpoint> -p 5432 -U f5user -d f5testdb -c "SELECT 'Connection $i', pg_backend_pid();"
done
```

**Verify distribution:**
```bash
# Check backend connections on each PostgreSQL instance
docker exec f5-postgres-1 psql -U f5user -d f5testdb -c "SELECT count(*) FROM pg_stat_activity WHERE datname='f5testdb';"
docker exec f5-postgres-2 psql -U f5user -d f5testdb -c "SELECT count(*) FROM pg_stat_activity WHERE datname='f5testdb';"
```

## Load Balancing Algorithms

### Round Robin (Default)
- Distributes connections evenly
- Best for similar workloads

### Least Connections
```yaml
# Better for PostgreSQL where connection duration varies
Algorithm: Least Connections
```

### Ring Hash (Session Persistence)
```yaml
# For applications that need connection persistence
Algorithm: Ring Hash
Hash Policy: Source IP
```

## Health Monitoring

**Monitor in F5XC Dashboard:**
1. Navigate to **Performance > Dashboards**
2. Select your TCP Load Balancer
3. View:
   - Active Connections
   - Total Connections
   - Backend Health Status
   - Connection Distribution

## PostgreSQL-Specific Considerations

### Connection Pooling
PostgreSQL connections are expensive. Consider:
- Using PgBouncer in front of PostgreSQL
- F5XC session persistence for application consistency

### Read Replicas
For read scaling:
- Create read-only PostgreSQL replicas
- Use separate origin pools for read vs write
- Route SELECT queries to read pool

### High Availability
```
Primary (Write):     postgres-1:5432
Replica (Read-only): postgres-2:5433

Create two LBs:
- postgres-write-lb → postgres-1 only
- postgres-read-lb  → postgres-1, postgres-2 (load balanced)
```

## Testing Scenarios

### Test 1: Basic TCP Load Balancing
```bash
# Create test table
docker exec f5-postgres-1 psql -U f5user -d f5testdb -c "CREATE TABLE IF NOT EXISTS test_lb (id SERIAL, instance TEXT, timestamp TIMESTAMP DEFAULT NOW());"

# Insert through LB and see which instance handles it
psql -h <f5xc-lb> -p 5432 -U f5user -d f5testdb -c "INSERT INTO test_lb (instance) VALUES ('via-lb');"
```

### Test 2: Failover Testing
```bash
# Stop postgres-1
docker stop f5-postgres-1

# Connections should automatically route to postgres-2
psql -h <f5xc-lb> -p 5432 -U f5user -d f5testdb -c "SELECT 'Still working!' as status;"

# Restart postgres-1
docker start f5-postgres-1
```

### Test 3: Connection Distribution
```python
# Python test script
import psycopg2
import time

for i in range(20):
    conn = psycopg2.connect(
        host="<f5xc-lb-endpoint>",
        port=5432,
        database="f5testdb",
        user="f5user",
        password="f5password"
    )
    cur = conn.cursor()
    cur.execute("SELECT pg_backend_pid();")
    pid = cur.fetchone()[0]
    print(f"Connection {i+1}: Backend PID {pid}")
    conn.close()
    time.sleep(1)
```

## Security Best Practices

1. **Use TLS/SSL for PostgreSQL connections**
```bash
# Enable SSL in PostgreSQL
docker exec f5-postgres-1 psql -U f5user -d f5testdb -c "ALTER SYSTEM SET ssl = on;"
```

2. **Network Isolation**
- Use F5XC private connectivity
- Don't expose PostgreSQL ports publicly
- Only allow F5XC source IPs

3. **Authentication**
- Use strong passwords
- Consider certificate-based auth
- Enable pg_hba.conf restrictions

4. **Monitoring**
- Enable F5XC security monitoring
- Set up alerts for connection spikes
- Monitor failed authentication attempts

## Troubleshooting

**Issue**: Connections failing
```bash
# Check if PostgreSQL is listening
docker exec f5-postgres-1 netstat -tuln | grep 5432

# Check PostgreSQL logs
docker logs f5-postgres-1
docker logs f5-postgres-2
```

**Issue**: Uneven distribution
- Verify health checks are passing
- Check connection idle timeout settings
- Review load balancing algorithm

**Issue**: Connection timeout
- Increase idle timeout in F5XC
- Check PostgreSQL max_connections setting
- Monitor connection pool exhaustion

## Summary

You now have:
- ✅ 2 PostgreSQL instances for TCP load balancing
- ✅ Health monitoring setup
- ✅ Test scripts to verify distribution
- ✅ F5XC configuration guide

**Connection Info:**
- Instance 1: `localhost:5432`
- Instance 2: `localhost:5433`
- Username: `f5user`
- Password: `f5password`
- Database: `f5testdb`

Good luck learning TCP Load Balancing with F5XC! 🐘🚀
