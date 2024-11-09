package com.entrypoint.gateway;

import java.nio.charset.StandardCharsets;
import java.util.Date;



import org.springframework.stereotype.Component;
import javax.crypto.SecretKey;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;

@Component
public class JWTUtil {

    private static final String TOKEN_PREFIX = "Bearer ";
    private static byte[] decodedKey = System.getenv("SECRET_KEY").getBytes(StandardCharsets.UTF_8);
    private static SecretKey secretKey = Keys.hmacShaKeyFor(decodedKey);
    private static Long jwtExpiration = 2L * (60 * 60 * 1000);

    public static String generateToken(String username, int role, Long id) {
        String token = Jwts.builder()
                .setExpiration(new Date(System.currentTimeMillis() + jwtExpiration))
                .claim("username", username)
                .claim("role", role)
                .claim("id", id)
                .signWith(secretKey)
                .compact();

        //chuja to dziala jbc
        //String tokenForRole1 = JWTUtil.generateToken("janeDoe", 1, 37L);  
        //String tokenForRole2 = JWTUtil.generateToken("johnDoe", 2, 21L);
        //String tokenForRole3 = JWTUtil.generateToken("janeDoe", 3, 37L);  
        // Add Bearer prefix before returning the token
        return TOKEN_PREFIX + token;
        //return TOKEN_PREFIX + tokenForRole2;
    }

    public static Long getJWTExpiration() {
        return jwtExpiration;
    }

    public static SecretKey getSecretKey() {
        return secretKey;
    }
}