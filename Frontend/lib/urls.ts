export const [gatewayClient, gatewayServer] = 
  process.env.NODE_ENV == "production" 
    ? [process.env.GATEWAY_URL, process.env.GATEWAY_URL] 
    : ["http://localhost:8081/gateway/", "http://gateway:8081/gateway/"]
