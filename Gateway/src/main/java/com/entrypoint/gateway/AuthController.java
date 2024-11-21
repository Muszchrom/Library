package com.entrypoint.gateway;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseCookie;
import org.springframework.http.ResponseEntity;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.entrypoint.gateway.entities.User;
import com.entrypoint.gateway.entities.UserDTO;
import com.entrypoint.gateway.exceptions.BadRequestException;
import com.entrypoint.gateway.exceptions.InvalidPasswordException;
import com.entrypoint.gateway.exceptions.UserNotFoundException;
import com.entrypoint.gateway.exceptions.UsernameExistsException;
import com.entrypoint.gateway.repositories.UserRepository;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.MalformedJwtException;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/auth")
public class AuthController {
    
    @Value("${TARGET:net_dev}")
    private String appTarget;

    private final UserRepository userRepository;

    AuthController(UserRepository userRepository){
        this.userRepository = userRepository;
    }

    @PostMapping("/login")
    public Mono<ResponseEntity<LoginResponse>> login(@RequestBody User user, ServerHttpResponse response) {
        return userRepository.findByUsername(user.getUsername())
                .map(u -> {
                    BCryptPasswordEncoder bcPsswdEncoder = new BCryptPasswordEncoder();
                    if (bcPsswdEncoder.matches(user.getPassword(), u.getPassword())) {
                        String token = JWTUtil.generateToken(u.getUsername(), u.getRole(), u.getId());
                        ResponseCookie responseCookie = ResponseCookie.from("JWT", token)
                                .httpOnly(true)
                                .secure(!appTarget.equals("DEV")) // !appTarget.equals("DEV")
                                .sameSite("Lax")
                                .maxAge(JWTUtil.getJWTExpiration())
                                .path("/")
                                .build();

                        response.addCookie(responseCookie);

                        // Create a LoginResponse object with the desired fields
                        LoginResponse loginResponse = new LoginResponse();
                        loginResponse.setToken(token);
                        loginResponse.setId(Long.toString(u.getId()));
                        loginResponse.setUsername(u.getUsername());
                        loginResponse.setEmail(u.getEmail());
                        loginResponse.setPhone(String.valueOf(u.getPhone()));
                        loginResponse.setRole(String.valueOf(u.getRole()));

                        // Return the LoginResponse object as JSON
                        return ResponseEntity.ok(loginResponse);
                    } else {
                        throw new BadCredentialsException("Niepoprawna nazwa uzytkownika lub haslo");
                    }
                })
                .switchIfEmpty(Mono.error(new BadCredentialsException("Niepoprawna nazwa uzytkownika lub haslo")));
    }


    @GetMapping("/logout")
    public Mono<Void> logout(ServerHttpResponse response) {
    ResponseCookie responseCookie = ResponseCookie.from("JWT", "")
      .httpOnly(true)
      .secure(!appTarget.equals("DEV"))
      .sameSite("Lax")
      .maxAge(0)
      .path("/")
      .build();

    response.addCookie(responseCookie);
    return response.setComplete();
    }

    @PostMapping("/user")
    public Mono<User> register(@RequestBody User user) {
        if (user.getPassword().length() < 7) {
            throw new InvalidPasswordException("Haslo za krotkie");
        }

        return userRepository.findByUsername(user.getUsername())
            .map(u -> {
                Boolean t = true;
                if (t) {
                    throw new UsernameExistsException("Username: " + user.getUsername() + " juz istnieje");
                }
                return u;
            }).switchIfEmpty(Mono.defer(() -> {
                user.hashPassword();
                return userRepository.save(user);
            }));
    }



    @PatchMapping("/user")
    public Mono<User> patchUser(@RequestBody UserDTO user, @RequestHeader("Authorization") String token) {
        // get data from token
        Claims claims;
        try {
            claims = Jwts.parser()
                                .verifyWith(JWTUtil.getSecretKey())
                                .build()
                                .parseSignedClaims(token.substring(7))
                                .getPayload();
        } catch (MalformedJwtException ex) {
            throw new BadCredentialsException("Invalid JWT syntax");
        }

        Integer id = (Integer) claims.get("id");

        return userRepository.findById(id).flatMap(u -> {
            // check if password matches with token username
            BCryptPasswordEncoder bcPsswdEncoder = new BCryptPasswordEncoder();
            if (!bcPsswdEncoder.matches(user.getPassword(), u.getPassword())) {
                throw new InvalidPasswordException("Niepoprawne hasło");
            }

            // if newPassword in request body alter current password
            if (user.getNewPassword() != null) {
                if (user.getNewPassword().length() < 7) {
                    throw new InvalidPasswordException("Haslo za krotkie");
                }
                u.setPassword(user.getNewPassword());
                u.hashPassword();
                return userRepository.save(u);
            }

            // if username in request body alter current username
            if (user.getUsername() != null) {
                return userRepository.findByUsername(user.getUsername())
                    .map(us -> {
                        Boolean t = true;
                        if (t) {
                            throw new UsernameExistsException("Username: " + user.getUsername() + " juz istnieje");
                        } 
                        return us;
                    }).switchIfEmpty(Mono.defer(() -> {
                        u.setUsername(user.getUsername());
                        System.out.println("XD>D>>");
                        return userRepository.save(u);
                    }));
            }

            // if email in request
            if (user.getEmail() != null) {
                u.setEmail(user.getEmail());
                return userRepository.save(u);
            }

            // if phone in request
            if (user.getPhone() != null) {
                u.setPhone(user.getPhone());
                return userRepository.save(u);
            }

            throw new BadRequestException("No matching field provided. Please provide one of the following: newPassword, username, email, phone");
        });
    }

    @GetMapping("/user/{id}")
    public Mono<User> getUser(@PathVariable Long id) {
        return userRepository.findById(id)
        .switchIfEmpty(Mono.error(new UserNotFoundException("User: " + id + " nie znaleziono")));
    }


}