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
				.route("Everyone is allowed", p-> p
					.path("/waz/books/**", 
						"/waz/genres/**",
						"/waz/authors/**",
						"/waz/libraries/**",
						"/waz/media/covers/**",
						"/waz/book-genres/**")
					.and()
					.method(HttpMethod.GET, HttpMethod.HEAD, HttpMethod.OPTIONS)
					.filters(f -> f.rewritePath("/waz/(?<segment>.*)", "/${segment}"))
					.uri("http://backend:8000")
				)
				.route("Employees allowed", p-> p
					.path("/waz/authors/**", 
						"/waz/libraries/**")
					.filters(f-> {
						f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
						f.filter(authFilterEmployee);
						return f;
					})
					.uri("http://backend:8000")
				)
				.route("Employees allowed for specific methods", p-> p
					.path("/waz/books/**",
						"/waz/genres/**",
						"/waz/book-genres/**")
					.and()
					.method(HttpMethod.PATCH,HttpMethod.POST)
					.filters(f-> {
						f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
						f.filter(authFilterEmployee);
						return f;
					})
					.uri("http://backend:8000")
				)
				// /rentals/ is build around header with userId and userRole for easier use of backend
				// thus separate route
				.route("Rentals path", p -> p
					.path("/waz/rentals/**")
					.and()
					.method(HttpMethod.GET, HttpMethod.POST, HttpMethod.PUT, HttpMethod.OPTIONS)
					.filters(f -> f.rewritePath("/waz/(?<segment>.*)", "/${segment}"))
					.uri("http://backend:8000")
				)
				
				.route("Admins allowed", p-> p
						// .path("/waz/books/**",
						// 	"/waz/genres/**",
						// 	"/waz/authors/**",
						// 	"/waz/book-genres/**",
						// 	"/waz/libraries/**")
						.path("/waz/**") // easier development/bug finding. In production it is recommended to make paths more strict
						.filters(f-> {
							f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
							f.filter(authFilterAdmin);
							return f;
						})
						.uri("http://backend:8000")
				)
				.build();
	}
}