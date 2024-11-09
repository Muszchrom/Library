package com.entrypoint.gateway;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.http.HttpStatus;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

@Component
public class AuthFilterAdmin implements GatewayFilter {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String authorizationHeader = exchange.getRequest().getHeaders().getFirst("Authorization");
    
    
        if (authorizationHeader != null && authorizationHeader.startsWith("Bearer ")) {
            String token = authorizationHeader.substring(7);
    
            try {
                //Claims claims = (Claims) Jwts.parser().setSigningKey(JWTUtil.getSecretKey()).parseClaimsJws(token).getBody();
                Claims claims = Jwts.parser().setSigningKey(JWTUtil.getSecretKey()).build().parseSignedClaims(token).getPayload();

    
                Integer role = (Integer) claims.get("role");
                if (role != null && role == 1) {
                    return chain.filter(exchange);
                } else {
                    ServerHttpResponse response = exchange.getResponse();
                    response.setStatusCode(HttpStatus.FORBIDDEN); 
    
                    return response.setComplete();
                }
            } catch (Exception e) {
                ServerHttpResponse response = exchange.getResponse();
                response.setStatusCode(HttpStatus.UNAUTHORIZED);
    
                return response.setComplete();
            }
        } else {
            ServerHttpResponse response = exchange.getResponse();
            response.setStatusCode(HttpStatus.UNAUTHORIZED);
            return
     response.setComplete();
        }
    }
}