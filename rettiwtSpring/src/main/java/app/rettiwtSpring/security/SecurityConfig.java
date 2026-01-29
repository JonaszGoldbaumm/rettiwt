package app.rettiwtSpring.security;

import java.util.List;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import lombok.RequiredArgsConstructor;

@Configuration
@RequiredArgsConstructor
public class SecurityConfig {
    private final JwtAuthFilter jwtAuthFilter;
    private final JwtAuthenticationEntryPoint unauthorizedHandler;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception{
        http
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .csrf(csrf -> csrf.disable())
            .exceptionHandling(ex -> ex.authenticationEntryPoint(unauthorizedHandler))
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                    .requestMatchers("/swagger-ui/**")
                    .permitAll()
                    .requestMatchers("/v3/api-docs*/**")
                    .permitAll()
                .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()
                // 1. Auth Endpoints
                .requestMatchers("/login", "/register").permitAll()

                // 2. Feed Endpoints
                // Specific restricted feeds MUST come before general permitAll
                .requestMatchers("/feed/media", "/feed/followed").authenticated()
                .requestMatchers(HttpMethod.GET, "/feed/", "/feed", "/feed/**").permitAll()

                // 3. Post Endpoints
                // Creation, Liking, Commenting, and Deletion require auth
                .requestMatchers(HttpMethod.POST, "/post","/post/**").authenticated()
                .requestMatchers(HttpMethod.DELETE, "/post/**").authenticated()
                // Getting post details or post media is public
                .requestMatchers(HttpMethod.GET, "/post/**").permitAll()

                // 4. Profile Endpoints
                // Updates (PATCH) and Following (POST) require auth
                .requestMatchers(HttpMethod.PATCH, "/profile/**").authenticated()
                .requestMatchers(HttpMethod.POST, "/profile/**").authenticated()
                // Viewing profiles or profile photos is public
                .requestMatchers(HttpMethod.GET, "/profile/**").permitAll()

                // 5. Default Guard
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource(){
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOrigins(List.of("http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"));
        configuration.setAllowedMethods(List.of("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"));
        
        configuration.setAllowedHeaders(List.of("Authorization", "Content-Type", "X-Requested-With", "Accept"));
        
        configuration.setAllowCredentials(true); 

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception{
        return config.getAuthenticationManager();
    }

    
}
