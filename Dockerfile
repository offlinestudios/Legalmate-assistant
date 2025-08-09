# ---------- Build stage ----------
FROM node:20-bullseye-slim AS builder
WORKDIR /app

# Enable pnpm via corepack (bundled with Node 20+)
RUN corepack enable

# Copy manifests first for better caching
COPY package.json pnpm-lock.yaml ./

# Install dependencies using the lockfile
RUN pnpm install --frozen-lockfile

# Copy the rest of the source
COPY . .

# Build-time environment variables for Vite (optional)
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build the production bundle
RUN pnpm run build

# ---------- Runtime stage ----------
# Use AWS ECR mirror of nginx to avoid Docker Hub rate limits/network issues
FROM public.ecr.aws/nginx/nginx:alpine

# Copy compiled static files
COPY --from=builder /app/dist /usr/share/nginx/html

# SPA-friendly nginx config
RUN printf 'server {\n  listen 80;\n  server_name _;\n  root /usr/share/nginx/html;\n  index index.html;\n  location / {\n    try_files $uri /index.html;\n  }\n  location /assets/ {\n    access_log off;\n    expires 1y;\n    add_header Cache-Control "public";\n  }\n}\n' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
