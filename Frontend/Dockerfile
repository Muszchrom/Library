FROM node:20.16.0-alpine AS base
WORKDIR /app
COPY package.json package.json
COPY package-lock.json package-lock.json

FROM base AS deps
WORKDIR /app
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1
RUN addgroup nodejs
RUN adduser -SDH nextjs
RUN mkdir .next
RUN chown nextjs:nodejs .next
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
USER nextjs
EXPOSE 3000
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "wget", "-q0", "http://localhost:3000/health" ]
CMD ["node", "server.js"]

FROM base AS dev
RUN npm ci
COPY . .
CMD ["npm", "run", "dev"]