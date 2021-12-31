FROM node:12.22.5-alpine

WORKDIR /app/react/

COPY package.json ./
RUN npm install 
RUN npm install react-scripts@3.4.1 -g
RUN npm install @material-ui/core
COPY . /app/react/
EXPOSE 3000

CMD ["npm", "start"]