package app.rettiwtSpring.controllers;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import app.rettiwtSpring.dto.AuthResponse;
import app.rettiwtSpring.dto.LoginRequest;
import app.rettiwtSpring.dto.RegisterRequest;
import app.rettiwtSpring.dto.UserSummaryDto;
import app.rettiwtSpring.model.User;
import app.rettiwtSpring.service.AuthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;



@RestController
@RequiredArgsConstructor
public class AuthController {
    private final AuthService authService;

    @PostMapping("/register")
    public ResponseEntity<UserSummaryDto> register(@Valid @RequestBody RegisterRequest request) {
        User u = authService.register(request);
        return ResponseEntity.ok(new UserSummaryDto(u.getId(), u.getUsername()));
    }
    
    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }
    
}
