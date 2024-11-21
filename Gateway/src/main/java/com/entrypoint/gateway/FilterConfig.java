package com.entrypoint.gateway;

import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.MalformedJwtException;
import reactor.core.publisher.Mono;

@Component
public class FilterConfig implements GlobalFilter, Ordered {
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String bearer = exchange.getRequest().getHeaders().getFirst("Authorization");
        if (bearer == null || !bearer.startsWith("Bearer ")) return chain.filter(exchange);
        String token = bearer.substring(7);
        try {
            Claims claims = Jwts.parser().verifyWith(JWTUtil.getSecretKey()).build().parseSignedClaims(token).getPayload();
            exchange.getRequest().mutate().header(
                "X-role-id", claims.get("role") + " " + claims.get("id")
            ).build();
            return chain.filter(exchange);
        } catch (MalformedJwtException ex) {
            throw new BadCredentialsException("Invalid token");
        }
    }

    @Override
    public int getOrder() {
        return -1;
    }
}
