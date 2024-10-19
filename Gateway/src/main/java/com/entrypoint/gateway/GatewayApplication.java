package com.entrypoint.gateway;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.reactive.ReactiveSecurityAutoConfiguration;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.data.r2dbc.repository.config.EnableR2dbcRepositories;
import org.springframework.http.HttpMethod;

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


	@Bean
	public RouteLocator myRoutes(RouteLocatorBuilder builder){
		return builder.routes()

				.route("login and logout page" ,p -> p
						.path("/login/**","/logout")
						.and()
						.method(HttpMethod.GET,HttpMethod.POST)
						.uri("http://localhost:3000")
				)

				.route("Admin auth", p -> p
						.path("/admin/**")
						.filters(f -> {
							f.filter(authFilter);
							f.filter(authFilterAdmin);
							return f;
						})
						.uri("http://localhost:3000/admin")
				)

				.route("Employee auth", p -> p
						.path("/employee/**")
						.filters(f -> {
							f.filter(authFilter);
							f.filter(authFilterEmployee);
							return f;
						})
						.uri("http://localhost:3000/employee")
				)

				.route("User auth", p -> p
						.path("/user/**")
						.filters(f -> {
							f.filter(authFilter);
							f.filter(authFilterUser);
							return f;
						})
						.uri("http://localhost:3000/user")
				)

				.build();
	}
}
