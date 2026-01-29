package app.rettiwtSpring.service;

import org.springframework.stereotype.Service;

import app.rettiwtSpring.config.UserNotFoundException;
import app.rettiwtSpring.model.Followed;
import app.rettiwtSpring.model.FollowedId;
import app.rettiwtSpring.model.User;
import app.rettiwtSpring.repository.FollowedRepository;
import app.rettiwtSpring.repository.UserRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class FollowService {
    private final FollowedRepository followedRepository;
    private final UserRepository userRepository;

    public boolean toggleFollow(Long userId, Long byUserId){
        User user = userRepository.findById(userId)
            .orElseThrow(()->new UserNotFoundException(userId.toString()));
        User byUser = userRepository.findById(byUserId)
            .orElseThrow(()->new UserNotFoundException(byUserId.toString()));

        if(followedRepository.existsByUserAndFollowedBy(user, byUser)){
            followedRepository.deleteByUserAndFollowedBy(user, byUser);
            return false;
        } else {
            Followed f = new Followed(new FollowedId(userId, byUserId), user, byUser, null);
            followedRepository.save(f);
            return true;
        }
    }

    public boolean isFollowing(Long userId, Long byUserId){
        User user= userRepository.getReferenceById(userId);
        User byUser = userRepository.getReferenceById(byUserId);
        return followedRepository.existsByUserAndFollowedBy(user, byUser);
    }
}
