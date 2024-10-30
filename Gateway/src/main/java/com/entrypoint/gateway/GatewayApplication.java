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

				// books routes
				.route("books for users", p-> p
						.path("/books")
						.and()
						.method(HttpMethod.GET)
						.filters(f-> {
							f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
							f.filter(authFilterUser);
							return f;
						})
						.uri("http://backend:8000/books/")
				)

				.route("books for employee", p-> p
						.path("/books")
						.and()
						.method(HttpMethod.POST)
						.filters(f-> {
							f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
							f.filter(authFilterEmployee);
							return f;
						})
						.uri("http://backend:8000/books/")
				)

				.route("books for admin", p-> p
						.path("/books")
						.and()
						.method(HttpMethod.DELETE,HttpMethod.PUT,HttpMethod.PATCH)
						.filters(f-> {
							f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
							f.filter(authFilterAdmin);
							return f;
						})
						.uri("http://backend:8000/books/")
				)

				//genres routes
				.route("genres for users", p-> p
						.path("/genres")
						.and()
						.method(HttpMethod.GET)
						.filters(f-> {
							f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
							f.filter(authFilterUser);
							return f;
						})
						.uri("http://backend:8000/genres/")
				)

				.route("genres for admin", p-> p
						.path("/genres")
						.and()
						.method(HttpMethod.POST,HttpMethod.DELETE,HttpMethod.PUT,HttpMethod.PATCH)
						.filters(f-> {
							f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
							f.filter(authFilterAdmin);
							return f;
						})
						.uri("http://backend:8000/genres/")
				)

				//authors routes
				.route("authors for users", p-> p
						.path("/authors")
						.and()
						.method(HttpMethod.GET)
						.filters(f-> {
							f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
							f.filter(authFilterUser);
							return f;
						})
						.uri("http://backend:8000/authors/")
				)

				.route("authors for employee", p-> p
						.path("/authors")
						.and()
						.method(HttpMethod.POST)
						.filters(f-> {
							f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
							f.filter(authFilterEmployee);
							return f;
						})
						.uri("http://backend:8000/authors/")
				)

				.route("authors for admin", p-> p
						.path("/authors")
						.and()
						.method(HttpMethod.DELETE,HttpMethod.PUT,HttpMethod.PATCH)
						.filters(f-> {
							f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
							f.filter(authFilterAdmin);
							return f;
						})
						.uri("http://backend:8000/authors/")
				)

				//book-genres routes
				.route("book-genres for users", p-> p
						.path("/book-genres")
						.and()
						.method(HttpMethod.GET)
						.filters(f-> {
							f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
							f.filter(authFilterUser);
							return f;
						})
						.uri("http://backend:8000/book-genres/")
				)

				.route("book-genres for employee", p-> p
						.path("/book-genres")
						.and()
						.method(HttpMethod.POST)
						.filters(f-> {
							f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
							f.filter(authFilterEmployee);
							return f;
						})
						.uri("http://backend:8000/book-genres/")
				)

				.route("book-genres for admin", p-> p
						.path("/book-genres")
						.and()
						.method(HttpMethod.DELETE,HttpMethod.PUT,HttpMethod.PATCH)
						.filters(f-> {
							f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
							f.filter(authFilterAdmin);
							return f;
						})
						.uri("http://backend:8000/book-genres/")
				)

				//login route
				.route("login and logout page" ,p -> p
						.path("/login/**","/logout")
						.and()
						.method(HttpMethod.GET,HttpMethod.POST)
						.uri("http://backend:8000")
				)

				//allow everything for everyone
//				.route("GET from all" , p-> p
//						.path("/waz/**")
//						.filters( f -> {
//							f.rewritePath("/waz/(?<segment>.*)", "/${segment}");
//							return f;
//						})
//						.uri("http://backend:8000")
//				)

				.build();
	}
}