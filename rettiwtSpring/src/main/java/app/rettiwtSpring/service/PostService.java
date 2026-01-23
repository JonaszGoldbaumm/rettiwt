package app.rettiwtSpring.service;

import java.util.List;

import org.apache.catalina.User;
import org.springframework.stereotype.Service;

import app.rettiwtSpring.model.Post;
import app.rettiwtSpring.repository.PostRepository;
import app.rettiwtSpring.repository.UserRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class PostService {
    private final PostRepository postRepository;
    private final UserRepository userRepository;

    public List<Post> getGlobalFeed(){
        return postRepository.findAllPostsFeed();
    }
    public List<Post> getPostsByUsername(String username){
        User user = (User) userRepository.findByUsername(username)
                .orElseThrow(() -> new RuntimeException("User not found"));
        return postRepository.findByUserOrderByCreatedAtDesc(user);
    }
    public List<Post> getPostsWithMedia(){
        return postRepository.findPostsWithMedia();
    }
    public List<Post> getFeedFromFollowed(Long currentUserId){
        return postRepository.findPostsFromFollowed(currentUserId);
    }
}
