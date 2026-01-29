package app.rettiwtSpring.service;

import java.util.List;

import org.springframework.stereotype.Service;

import app.rettiwtSpring.config.UserNotFoundException;
import app.rettiwtSpring.dto.UserProfileDto;
import app.rettiwtSpring.dto.UserSummaryDto;
import app.rettiwtSpring.model.Followed;
import app.rettiwtSpring.model.User;
import app.rettiwtSpring.repository.FollowedRepository;
import app.rettiwtSpring.repository.UserRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ProfileService {
    private final UserRepository userRepository;
    private final FollowedRepository followedRepository;

    public UserProfileDto getUserProfile(Long userId){
        User user = userRepository.findById(userId).orElseThrow(()-> new UserNotFoundException(userId.toString()));
        
        List<Followed> followerLinks = followedRepository.findByUser(user);
        List<Followed> followedLinks = followedRepository.findByFollowedBy(user);


        List<UserSummaryDto> followers = followerLinks.stream()
            .map(f -> new UserSummaryDto(f.getFollowedBy().getId(), f.getFollowedBy().getUsername()))
            .toList();
        List<UserSummaryDto> followed = followedLinks.stream()
            .map(f-> new UserSummaryDto(f.getUser().getId(), f.getUser().getUsername()))
            .toList();

        return new UserProfileDto(userId, user.getUsername(), user.getEmail(), user.getDescription(), followers.size(), followed.size(), followers, followed);
    }

}
