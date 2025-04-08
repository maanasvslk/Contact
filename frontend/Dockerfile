FROM node:18-slim AS build

WORKDIR /app

# Copy package files first to cache npm install
COPY package.json package-lock.json ./
RUN npm install

# Copy only source files needed for build
COPY src/ ./src/
COPY public/ ./public/
COPY postcss.config.js tailwind.config.js ./
RUN npm run build

# Final stage for serving
FROM node:18-slim

WORKDIR /app
COPY --from=build /app/build ./build
RUN npm install -g serve

EXPOSE 5000
CMD ["serve", "-s", "build", "-l", "5000"]