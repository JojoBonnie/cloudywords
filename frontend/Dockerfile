FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy project
COPY . .

# Expose the port
EXPOSE 3000

# Run the application
CMD ["npm", "start"]
