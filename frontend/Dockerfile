# Use an official Node runtime as the base image
FROM node:18

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the React app
COPY . .

# Build the app
RUN npm run build

# Serve the app (using a simple server like serve)
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "5000"]

# Expose the port
EXPOSE 3000