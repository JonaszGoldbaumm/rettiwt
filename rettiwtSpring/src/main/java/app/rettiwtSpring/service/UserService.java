package app.rettiwtSpring.service;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import app.rettiwtSpring.config.UserNotFoundException;
import app.rettiwtSpring.model.User;
import app.rettiwtSpring.repository.UserRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public User updateUsername(Long userId, String newUsername){
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException(userId.toString()));
        user.setUsername(newUsername);
        return userRepository.save(user);
    }

    public User updatePassword(Long userId, String newPassword){
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException(userId.toString()));
        user.setPassword(passwordEncoder.encode(newPassword));
        return userRepository.save(user);
    }

    public User updateProfilePic(Long userId, byte[] pic){
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException(userId.toString()));
        user.setProfilePic(pic);
        return userRepository.save(user);
    }

    public User updateDescription(Long userId, String desc){
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException(userId.toString()));
        user.setDescription(desc);
        return userRepository.save(user);
    }
}
