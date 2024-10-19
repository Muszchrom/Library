package com.entrypoint.gateway;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.reactive.ReactiveSecurityAutoConfiguration;
import org.springframework.data.r2dbc.repository.config.EnableR2dbcRepositories;

@EnableR2dbcRepositories
@SpringBootApplication(exclude={ReactiveSecurityAutoConfiguration.class})
public class GatewayApplication {

	@Autowired
	private AuthFilter authFilter;

	@Autowired
	private AuthFilterAdmin authFilterAdmin;

	@Autowired
	private AuthFilterEmployee authFilterEmployee;

	@Autowired
	private AuthFilterUser authFilterUser;

	public static void main(String[] args) {
		SpringApplication.run(GatewayApplication.class, args);
	}

}
