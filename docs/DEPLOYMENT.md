"""
DEPLOYMENT GUIDE

This guide covers deploying the AI Voice Receptionist to production.
"""

## Quick Deployment Checklist

- [ ] Configure environment variables
- [ ] Set up domain and SSL certificates
- [ ] Initialize database with migrations
- [ ] Configure Twilio webhooks
- [ ] Set up OpenAI API key
- [ ] Configure email/SMS services
- [ ] Set up AWS S3 for recordings
- [ ] Enable monitoring and logging
- [ ] Test end-to-end flows
- [ ] Set up backups

## Environment Setup

1. **Create .env file**
   ```bash
   cp .env.example .env
   # Edit with production values
   ```

2. **Database Setup**
   ```bash
   # Run migrations
   docker-compose exec backend alembic upgrade head
   
   # Seed initial data (optional)
   docker-compose exec backend python -m app.database.seed
   ```

3. **SSL Certificates** (for HTTPS)
   ```bash
   # Generate self-signed cert (dev)
   openssl req -x509 -newkey rsa:4096 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365
   
   # Production: Use Let's Encrypt
   certbot certonly --standalone -d yourdomain.com
   cp /etc/letsencrypt/live/yourdomain.com/*.pem nginx/ssl/
   ```

## Docker Deployment

```bash
# Build production images
docker-compose build

# Start services
docker-compose up -d

# Verify health
curl http://localhost/health
curl http://localhost:8000/health

# Check logs
docker-compose logs -f
```

## Server Configuration

### Nginx Configuration

Update `nginx/nginx.conf`:
- Set your domain name
- Configure SSL paths
- Adjust rate limiting as needed
- Add security headers

### Database Backup

```bash
# Backup database
docker-compose exec postgres pg_dump -U user business_assistant > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T postgres psql -U user business_assistant
```

## Monitoring

### Application Logs

```bash
# Real-time logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Store logs externally
docker-compose logs backend > logs/backend.log
```

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Database connection
curl http://localhost:8000/api/v1/health

# Dashboard access
curl http://localhost/
```

## Post-Deployment

1. **Verify Integrations**
   - Test Twilio incoming calls
   - Test email notifications
   - Test calendar sync

2. **Load Testing**
   ```bash
   # Simple load test
   ab -n 1000 -c 100 http://localhost/
   ```

3. **Security Audit**
   - Test authentication flows
   - Verify CORS settings
   - Check rate limiting
   - Test input validation

4. **Backup Strategy**
   - Automated database backups
   - Store recordings in S3
   - Backup configuration files

## Scaling

### Horizontal Scaling

1. **Load Balancer**: Use HAProxy/ALB in front of Nginx
2. **Database**: Use RDS with read replicas
3. **Cache**: Use managed Redis (ElastiCache)
4. **Storage**: Use managed S3

### Vertical Scaling

- Increase container resources in docker-compose
- Increase database machine size
- Increase Redis memory

## Troubleshooting

### Common Issues

**Backend not starting**
```bash
docker-compose logs backend
# Check database connection
# Check OpenAI API key
```

**Frontend not accessible**
```bash
docker-compose logs frontend
# Check API_URL configuration
# Check CORS settings
```

**Calls not being received**
```bash
# Check Twilio webhooks
# Verify incoming URL is accessible
# Check firewall rules
```

### Database Issues

```bash
# Check database status
docker-compose exec postgres pg_isready

# Connect to database
docker-compose exec postgres psql -U user -d business_assistant
```

## Upgrades

```bash
# Pull latest images
docker-compose pull

# Backup current database
docker-compose exec postgres pg_dump -U user business_assistant > backup_$(date +%s).sql

# Run migrations
docker-compose exec backend alembic upgrade head

# Restart services
docker-compose down
docker-compose up -d
```

## Support

For deployment issues, check:
- docker-compose logs
- Application error logs
- Database logs
- Nginx logs
- GitHub Issues
