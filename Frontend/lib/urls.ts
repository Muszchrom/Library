export const [gatewayClient, gatewayServer] = 
  process.env.NODE_ENV == "production" 
    ? ["https://lublean.com/gateway/", "https://lublean.com/gateway/"] 
    : ["http://localhost:8081/gateway/", "http://gateway:8081/gateway/"]
