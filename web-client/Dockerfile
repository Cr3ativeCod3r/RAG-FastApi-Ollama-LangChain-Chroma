FROM node:22-alpine

WORKDIR /app

# Copy package descriptors first for layer caching
COPY package.json ./

# Install npm dependencies
RUN npm install

# Copy source code and config files
COPY . .

# Expose Vite dev server port
EXPOSE 3000

# Start Vite dev server on 0.0.0.0:3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
