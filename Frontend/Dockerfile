FROM node:20.16.0-alpine AS base
WORKDIR /app
COPY package.json package.json
COPY package-lock.json package-lock.json

FROM base AS dev
RUN npm ci
COPY . .
CMD ["npm", "run", "dev"]