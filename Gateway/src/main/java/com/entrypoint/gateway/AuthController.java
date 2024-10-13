package com.entrypoint.gateway;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseCookie;
import org.springframework.http.ResponseEntity;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.entrypoint.gateway.entities.User;
import com.entrypoint.gateway.exceptions.InvalidPasswordException;
import com.entrypoint.gateway.exceptions.UserNotFoundException;
import com.entrypoint.gateway.exceptions.UsernameExistsException;
import com.entrypoint.gateway.repositories.UserRepository;

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
    public Mono<ResponseEntity<String>> login(@RequestBody User user, ServerHttpResponse response) {
    return userRepository.findByUsername(user.getUsername()).map(u -> {
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
        return ResponseEntity.ok("Zalogowano");
      } else {
        throw new BadCredentialsException("Niepoprawna nazwa uzytkownika lub haslo");
      }
    }).switchIfEmpty(Mono.error(new BadCredentialsException("Niepoprawna nazwa uzytkownika lub haslo")));
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
      throw new InvalidPasswordException("Password too short");
    }

        return userRepository.findByUsername(user.getUsername())
        .map(u -> {
            Boolean t = true;
            if (t) {
            throw new UsernameExistsException("Username: " + user.getUsername() + " already exist");
            }
            return u;
        }).switchIfEmpty(Mono.defer(() -> {
            user.hashPassword();
            return userRepository.save(user);
        }));
    }


    @GetMapping("/user/{id}")
    public Mono<User> getUser(@PathVariable Long id) {
        return userRepository.findById(id)
        .switchIfEmpty(Mono.error(new UserNotFoundException("User: " + id + " not found")));
    }


}