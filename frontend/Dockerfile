# Use the official Node.js image as a parent image
FROM node:18 as build

# Set working directory inside the container
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json /app/package.json
RUN npm install

# Copy the rest of the React app into the container
COPY . /app

# Build the React app for production
RUN npm run build

# Install 'serve' to serve the built files
RUN npm install -g serve

# Expose port 80 to serve the app
EXPOSE 3000

# Start Nginx server
CMD ["serve", "-s", "dist", "-l", "3000"]
