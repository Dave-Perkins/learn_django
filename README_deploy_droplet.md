# Django Project Deployment Workflow on DigitalOcean Droplet

This guide outlines the typical steps for deploying code updates to your DigitalOcean droplet, as well as managing supporting services like EmailEngine and Redis.

---

## 1. Prerequisites (One-Time Setup)
- **EmailEngine and Redis** should already be installed and running on your droplet. (See below for restart instructions if needed.)
- Your Django project and virtual environment are set up on the droplet.
- Your code is managed with git.

---

## 2. Deploying Code Updates

1. **Push your changes from local to your remote git repository (if using one):**
   ```sh
   git add .
   git commit -m "Describe your changes"
   git push
   ```

2. **SSH into your droplet:**
   ```sh
   ssh root@<your-droplet-ip>
   cd /var/www/learn_django
   ```

3. **Pull the latest code:**
   ```sh
   git pull
   ```

4. **Activate your virtual environment:**
   ```sh
   source venv/bin/activate
   ```

5. **Install any new dependencies (if requirements.txt changed):**
   ```sh
   pip install -r requirements.txt
   ```

6. **Apply database migrations (if needed):**
   ```sh
   python manage.py migrate
   ```

7. **Collect static files (if static files changed):**
   ```sh
   python manage.py collectstatic
   ```

8. **Restart your Django app (if using gunicorn):**
   ```sh
   systemctl restart gunicorn
   # or whatever process manager you use
   ```

---

## 3. Managing EmailEngine and Redis

- **To check if EmailEngine is running:**
  ```sh
  docker ps
  # Look for the 'emailengine' container
  ```

- **To start EmailEngine if it is stopped:**
  ```sh
  docker start emailengine
  ```

- **To set EmailEngine to start automatically on reboot:**
  ```sh
  docker update --restart=always emailengine
  ```

- **To check if Redis is running:**
  ```sh
  systemctl status redis-server
  ```

- **To start Redis if it is stopped:**
  ```sh
  systemctl start redis-server
  ```

---

## 4. Notes
- You do **not** need to reinstall or reconfigure EmailEngine or Redis for each code update.
- Only restart these services if you reboot the droplet or change their configuration.
- For troubleshooting, check logs:
  - Django: `journalctl -u gunicorn` or your process manager's logs
  - EmailEngine: `docker logs emailengine`
  - Redis: `journalctl -u redis-server`

---

## 5. Quick Reference
- **Update code:** `git pull`
- **Activate venv:** `source venv/bin/activate`
- **Migrate:** `python manage.py migrate`
- **Collect static:** `python manage.py collectstatic`
- **Restart app:** `systemctl restart gunicorn`
- **Start EmailEngine:** `docker start emailengine`
- **Start Redis:** `systemctl start redis-server`

---

Keep this guide handy for all future deployments!
