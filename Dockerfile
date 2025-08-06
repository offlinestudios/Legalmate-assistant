# Dockerfile for LegalMate
#
# This multi‑stage Docker build sets up a Node environment to build
# the React front‑end and then copies the generated static assets
# into a lightweight Python image that serves the Flask back‑end. It
# eliminates the need for Railway’s Nixpacks builder and avoids
# package conflicts.

### Stage 1: build the front‑end ###
FROM node:18-alpine AS frontend-build

# Set working directory for the front‑end build
WORKDIR /app/frontend

# Copy package manifest and install dependencies. We pass
# --legacy-peer-deps to npm install to bypass strict peer
# dependency resolution, which otherwise fails due to a mismatch
# between date-fns and react-day-picker.
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps

# Copy the rest of the front‑end source and build
COPY frontend .
RUN npm run build


### Stage 2: prepare the Python back‑end and serve the app ###
FROM python:3.11-slim AS backend-run

# Set working directory for the back‑end
WORKDIR /app

# Copy the back‑end source code
COPY backend ./backend

# Copy the built front‑end assets from the previous stage into the
# Flask static directory so that the Python app can serve them
COPY --from=frontend-build /app/frontend/dist/ ./backend/src/static/

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose the Flask port and set environment variable for OpenAI API
ENV PORT=5000
EXPOSE 5000

# Entrypoint to run the Flask application
CMD ["python", "backend/src/main.py"]