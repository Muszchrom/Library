package com.entrypoint.gateway.repositories;

import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;

import com.entrypoint.gateway.entities.User;

import reactor.core.publisher.Mono;

@Repository
public interface UserRepository extends R2dbcRepository<User, Integer> {
  Mono<User> findByUsername(String username);
  Mono<User> findById(Long id);
  Mono<Void> deleteById(Long id);
}