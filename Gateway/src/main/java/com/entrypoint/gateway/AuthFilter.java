package com.entrypoint.gateway;

import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.http.HttpStatus;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.stereotype.Component;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.web.server.ServerWebExchange;

import reactor.core.publisher.Mono;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;

@Component
public class AuthFilter implements GatewayFilter {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();

        // check if JWT cookie exists
        if (isCookieMissing(request) && isBearerMissing(request)) {
            return this.onError(
                    exchange,
                    "Authorization data is missing (cookie or bearer) in request or it's contents are invalid",
                    HttpStatus.UNAUTHORIZED);
        }

        String token = getToken(request);

        // Check if token is valid
        try {
            Jwts.parser().verifyWith(JWTUtil.getSecretKey()).build().parseSignedClaims(token);
        } catch (JwtException ex) {
            System.out.println(ex.getMessage());
            return this.onError(
                    exchange,
                    "Authorization token is invalid",
                    HttpStatus.FORBIDDEN);
        }
        return chain.filter(exchange);
    }

    private String getToken(ServerHttpRequest request) {
        if (!isCookieMissing(request)) {
            return request.getCookies().getFirst("JWT").getValue();
        }
        return request.getHeaders().getOrEmpty("Authorization").get(0).substring(7);
    }

    private boolean isCookieMissing(ServerHttpRequest request) {
        return null == request.getCookies().getFirst("JWT");
    }

    private boolean isBearerMissing(ServerHttpRequest request) {
        return request.getHeaders().getOrEmpty("Authorization").isEmpty();
    }

    private Mono<Void> onError(ServerWebExchange exchange, String err, HttpStatus httpStatus) {
        ServerHttpResponse response = exchange.getResponse();
        response.setStatusCode(httpStatus);
        return response.setComplete();
    }
}