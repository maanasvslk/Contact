# Build stage
FROM node:18-slim AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY src/ ./src/
COPY public/ ./public/
COPY postcss.config.js tailwind.config.js ./

RUN npm run build

# Production stage
FROM node:18-slim

WORKDIR /app

COPY --from=build /app/build ./build

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]