package app.rettiwtSpring.service;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import app.rettiwtSpring.config.InvalidPasswordException;
import app.rettiwtSpring.config.UserNotFoundException;
import app.rettiwtSpring.dto.AuthResponse;
import app.rettiwtSpring.dto.LoginRequest;
import app.rettiwtSpring.dto.RegisterRequest;
import app.rettiwtSpring.model.User;
import app.rettiwtSpring.repository.UserRepository;
import app.rettiwtSpring.security.JwtService;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    public User register(RegisterRequest request){
        if(userRepository.existsByUsername(request.getUsername())){
            throw new RuntimeException("Username already taken");
        }
        if(userRepository.existsByEmail(request.getEmail())){
            throw new RuntimeException("Email already in use");
        }
        User user = new User();
        user.setUsername(request.getUsername().trim());
        user.setEmail(request.getEmail());
        user.setPassword(passwordEncoder.encode(request.getPassword()));

        return userRepository.save(user);
    }

    public AuthResponse login(LoginRequest request){
        User user = userRepository.findByUsername(request.getUsername_or_email())
            .or(()->userRepository.findByEmail(request.getUsername_or_email()))
            .orElseThrow(()-> new UserNotFoundException(request.getUsername_or_email()));

        if(!passwordEncoder.matches(request.getPassword(), user.getPassword())){
            throw new InvalidPasswordException(request.getUsername_or_email());
        }
        String token = jwtService.generateToken(user);

        return new AuthResponse(token, "bearer", user.getId(), user.getUsername());
    }
}
