# Deployment Guide for Portafy

This guide explains how to deploy the Portafy Django application to Render.com or Railway using Docker containers and the provided configuration files.

## Prerequisites

1. A Render.com account
2. Git repository connected to Render
3. Chapa payment gateway account (for payment functionality)
4. Docker (for local development)

## Docker Configuration

The application is fully containerized using Docker for easy deployment and development.

### Files:
- **`Dockerfile`** - Main Django application container
- **`Dockerfile.worker`** - Celery worker container
- **`docker-compose.yml`** - Local development environment
- **`.dockerignore`** - Optimizes Docker build process

### Benefits of Docker:
- **Consistent deployment** across all environments
- **Isolated dependencies** - no conflicts
- **Easy local development** with docker-compose
- **Security** - non-root containers
- **Optimized builds** with layer caching

## Services Overview

The `render.yaml` file sets up four services (all on **free tier**):

1. **PostgreSQL Database** (`portafy-db`) - Stores application data
2. **Redis** (`portafy-redis`) - Message broker for Celery and caching
3. **Celery Worker** (`portafy-worker`) - Processes background tasks (PDF conversion, website generation)
4. **Web Application** (`portafy-web`) - Runs the Django application

### Free Tier Specifications:
- **Web Service**: 512MB RAM, shared CPU
- **Worker Service**: 512MB RAM, shared CPU
- **PostgreSQL**: 1GB storage, shared infrastructure
- **Redis**: 25MB storage, shared infrastructure

### Free Tier Limitations:
- **Cold starts**: Services may sleep after inactivity and take time to wake up
- **Resource limits**: Limited CPU and memory may cause slower performance
- **Concurrent connections**: Limited database connections
- **Build time**: Free tier builds may be queued behind paid users
- **Background tasks**: Celery worker may be slower with limited resources

### Performance Optimization Tips:
- **Reduce worker processes**: Using `--concurrency=1` for Celery worker
- **Optimize Gunicorn**: Using `--workers=2` and `sync` worker class
- **Database pooling**: Configure minimal database connections in Django
- **Task batching**: Process multiple small tasks together when possible
- **Caching**: Use Redis for caching to reduce database load

## Local Development with Docker

### Quick Start:
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Run migrations
docker-compose exec web python Backend/Portafy/manage.py migrate

# Create superuser
docker-compose exec web python Backend/Portafy/manage.py createsuperuser

# Stop all services
docker-compose down
```

### Services:
- **Web**: Django development server on http://localhost:8000
- **Database**: PostgreSQL on localhost:5432
- **Redis**: Redis on localhost:6379
- **Worker**: Celery worker for background tasks
- **Beat**: Celery beat for scheduled tasks

## Deployment Steps

### 1. Connect Repository to Render

1. Log in to your Render.com dashboard
2. Click "New +" and select "Blueprint"
3. Connect your Git repository (GitHub/GitLab)
4. Render will automatically detect the `render.yaml` file

### 2. Configure Environment Variables

In the Render dashboard, you'll need to set these environment variables for the `portafy-web` service:

#### Required Variables:
- `CHAPA_SECRET_KEY` - Your Chapa secret key
- `CHAPA_PUBLIC_KEY` - Your Chapa public key
- `FRONTEND_URL` - Your frontend application URL (if applicable)
- `DEFAULT_FROM_EMAIL` - Email address for notifications

#### Optional Variables:
- `SECRET_KEY` - Leave empty to auto-generate (recommended)
- `ALLOWED_HOSTS` - Auto-configured by Render

### 3. Deploy

1. Click "Apply" to create the services
2. Render will automatically:
   - Provision PostgreSQL database
   - Set up Redis instance
   - Build and deploy your Django application
   - Run migrations
   - Collect static files

## Post-Deployment Steps

### 1. Verify Deployment

1. Check the logs in Render dashboard for any errors
2. Visit your application URL (provided by Render)
3. Test the `/admin/` endpoint (health check path)

### 2. Set Up Domain (Optional)

1. In Render dashboard, go to your web service settings
2. Add custom domain if needed
3. Update `ALLOWED_HOSTS` if using custom domain

### 3. Configure Background Tasks

The deployment includes Celery with Redis for background processing:

- **Celery Worker** (`portafy-worker`) - Processes background tasks like PDF conversion and website generation
- **Redis** (`portafy-redis`) - Message broker that queues tasks between web app and worker
- **Automatic Integration** - Web application automatically queues tasks to Redis, worker processes them

The worker service will automatically:
- Start processing tasks when deployed
- Scale based on queue size (within plan limits)
- Handle failures and retries automatically
- Log all task processing activities

### 4. Monitor Background Tasks

You can monitor Celery worker activities in the Render dashboard:
- **Worker Logs**: Check `portafy-worker` service logs for task processing status
- **Task Success/Failure**: Monitor for any failed tasks that need attention
- **Queue Length**: Redis doesn't provide direct queue monitoring, but you can check worker logs

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | No | Auto-generated |
| `DEBUG` | Debug mode | No | `False` |
| `ALLOWED_HOSTS` | Allowed hostnames | No | Auto-configured |
| `DATABASE_URL` | Database connection | No | Auto-configured |
| `REDIS_URL` | Redis connection | No | Auto-configured |
| `CELERY_BROKER_URL` | Celery broker | No | Auto-configured |
| `CHAPA_SECRET_KEY` | Payment gateway secret | Yes | - |
| `CHAPA_PUBLIC_KEY` | Payment gateway public | Yes | - |
| `FRONTEND_URL` | Frontend application URL | Yes | - |
| `DEFAULT_FROM_EMAIL` | Email for notifications | Yes | - |

## Troubleshooting

### Common Issues:

1. **Build Failures**
   - Check Python version (should be 3.11+)
   - Verify all dependencies in `requirements/prod.txt`
   - Check for missing system packages

2. **Database Connection Issues**
   - Ensure PostgreSQL service is running
   - Check `DATABASE_URL` environment variable
   - Verify database migrations completed

3. **Static Files Not Loading**
   - Confirm `collectstatic` ran successfully
   - Check `WHITENOISE` configuration
   - Verify static files settings in Django

4. **Payment Integration Issues**
   - Verify Chapa API keys are correct
   - Check Chapa webhook configuration
   - Ensure payment URLs are properly configured

5. **Celery Worker Issues**
   - Check worker service logs for error messages
   - Verify Redis connection is working
   - Ensure all Python dependencies are installed in worker
   - Check if tasks are being queued properly from web app
   - Monitor worker resource usage (may need to upgrade plan for high-volume processing)

### Logs Access:

- **Web Service Logs**: Render dashboard → Your service → Logs
- **Database Logs**: Available in Render dashboard
- **Redis Logs**: Available in Render dashboard

## Monitoring and Maintenance

### Health Checks:
- Web service health check: `https://your-app.onrender.com/admin/`
- Database connectivity can be monitored via Render dashboard

### Backups:
- Render automatically backs up PostgreSQL databases
- Redis data is not automatically backed up (consider if needed)

### Updates:
1. Push changes to your Git repository
2. Render will automatically redeploy (if auto-deploy is enabled)
3. Monitor deployment logs for issues

## Support

For Render-specific issues, check:
- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)
- Render support channels

For application-specific issues, check the application logs and ensure all environment variables are properly configured.
