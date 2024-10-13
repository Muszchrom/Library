package com.entrypoint.gateway;

import java.nio.charset.StandardCharsets;
import java.util.Date;



import org.springframework.stereotype.Component;
import javax.crypto.SecretKey;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;

@Component
public class JWTUtil{
      private static byte[] decodedKey = System.getenv("SECRET_KEY").getBytes(StandardCharsets.UTF_8);
      private static SecretKey secretKey = Keys.hmacShaKeyFor(decodedKey); // and this not
        
      //                                  ↓ number of hours so like n*(an hour)
      private static Long jwtExpiration = 2L*(60*60*1000);

    public static String generateToken(String username, int role, Long id) {
        return Jwts.builder()
            .setExpiration(new Date(System.currentTimeMillis() + jwtExpiration))
            .claim("username", username)
            .claim("role", role)
            .claim("id", id)
            .signWith(secretKey)
            .compact();
    }

    public static Long getJWTExpiration() {
    return jwtExpiration; 
    }

    public static SecretKey getSecretKey() {
    return secretKey;
    }

}