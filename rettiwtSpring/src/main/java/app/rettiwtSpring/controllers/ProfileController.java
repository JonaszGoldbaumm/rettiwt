package app.rettiwtSpring.controllers;

import java.io.IOException;
import java.util.List;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.server.ResponseStatusException;

import app.rettiwtSpring.dto.DescriptionUpdateRequest;
import app.rettiwtSpring.dto.PasswordUpdateRequest;
import app.rettiwtSpring.dto.UserProfileDto;
import app.rettiwtSpring.dto.UserSummaryDto;
import app.rettiwtSpring.dto.UsernameUpdateRequest;
import app.rettiwtSpring.model.User;
import app.rettiwtSpring.repository.UserRepository;
import app.rettiwtSpring.service.FollowService;
import app.rettiwtSpring.service.ProfileService;
import app.rettiwtSpring.service.UserService;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/profile")
@RequiredArgsConstructor
public class ProfileController {
    private final ProfileService profileService;
    private final UserService userService;
    private final FollowService followService;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    // 1. Get User Profile
    @GetMapping("/{userId}")
    public ResponseEntity<UserProfileDto> getProfile(@PathVariable Long userId) {
        // ProfileService already handles the UserNotFoundException
        return ResponseEntity.ok(profileService.getUserProfile(userId));
    }

    // 2. Current User Info
    @GetMapping("/me/profile")
    public ResponseEntity<UserSummaryDto> getCurrentUserInfo(@AuthenticationPrincipal User user) {
        return ResponseEntity.ok(new UserSummaryDto(user.getId(), user.getUsername()));
    }

    // 3. Get Profile Photo (Binary Stream)
    @GetMapping("/{userId}/photo")
    public ResponseEntity<byte[]> getProfilePhoto(@PathVariable Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found"));
        
        if (user.getProfilePic() == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Profile photo not found");
        }

        return ResponseEntity.ok()
                .contentType(MediaType.IMAGE_JPEG) 
                .body(user.getProfilePic());
    }

    // 4. Update Username
    @PatchMapping("/me/username")
    public ResponseEntity<?> updateUsername(@RequestBody UsernameUpdateRequest data, @AuthenticationPrincipal User user) {
        if (userRepository.existsByUsername(data.getNew_username())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Username already taken");
        }
        User updated = userService.updateUsername(user.getId(), data.getNew_username().trim());
        return ResponseEntity.ok(Map.of(
            "message", "Username updated",
            "username", updated.getUsername()
        ));
    }

    // 5. Update Password
    @PatchMapping("/me/password")
    public ResponseEntity<?> updatePassword(@RequestBody PasswordUpdateRequest data, @AuthenticationPrincipal User user) {
        if (!passwordEncoder.matches(data.getOld_password(), user.getPassword())) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Old password is incorrect");
        }
        userService.updatePassword(user.getId(), data.getNew_password());
        return ResponseEntity.ok(Map.of("message", "Password updated"));
    }

    // 6. Update Description
    @PatchMapping("/me/description")
    public ResponseEntity<?> updateDescription(@RequestBody DescriptionUpdateRequest data, @AuthenticationPrincipal User user) {
        userService.updateDescription(user.getId(), data.getDescription());
        return ResponseEntity.ok(Map.of("message", "Description updated"));
    }

    // 7. Update Profile Picture (Multipart)
    @PatchMapping(value = "/me/profile-pic", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<?> updateProfilePic(@RequestParam("pic") MultipartFile pic, @AuthenticationPrincipal User user) throws IOException {
        if (pic.isEmpty() || !List.of("image/jpeg", "image/png", "image/webp").contains(pic.getContentType())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Invalid image type");
        }
        userService.updateProfilePic(user.getId(), pic.getBytes());
        return ResponseEntity.ok(Map.of("message", "Profile picture updated"));
    }

    // 8. Get Followers
    @GetMapping("/{userId}/followers")
    public ResponseEntity<List<UserSummaryDto>> getFollowers(@PathVariable Long userId) {
        return ResponseEntity.ok(profileService.getUserProfile(userId).getFollowers());
    }

    // 9. Get Followed Users
    @GetMapping("/{userId}/followed")
    public ResponseEntity<List<UserSummaryDto>> getFollowed(@PathVariable Long userId) {
        return ResponseEntity.ok(profileService.getUserProfile(userId).getFollowed());
    }

    // 10. Toggle Follow
    @PostMapping("/{userId}/follow")
    public ResponseEntity<?> toggleFollow(@PathVariable Long userId, @AuthenticationPrincipal User user) {
        if (user.getId().equals(userId)) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Cannot follow yourself");
        }
        boolean following = followService.toggleFollow(userId, user.getId());
        return ResponseEntity.ok(Map.of("following", following));
    }

    // 11. Check Following Status
    @GetMapping("/{userId}/isfollow")
    public ResponseEntity<?> checkFollowing(@PathVariable Long userId, @AuthenticationPrincipal User user) {
        if (user.getId().equals(userId)) {
            return ResponseEntity.ok(Map.of("following", false));
        }
        boolean following = followService.isFollowing(userId, user.getId());
        return ResponseEntity.ok(Map.of("following", following));
    }
}

