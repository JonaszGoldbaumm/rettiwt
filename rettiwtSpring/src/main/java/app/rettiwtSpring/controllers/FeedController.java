package app.rettiwtSpring.controllers;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import app.rettiwtSpring.dto.FeedResponseDto;
import app.rettiwtSpring.dto.PostDto;
import app.rettiwtSpring.dto.UserSummaryDto;
import app.rettiwtSpring.model.Post;
import app.rettiwtSpring.model.User;
import app.rettiwtSpring.repository.CommentRepository;
import app.rettiwtSpring.repository.LikeRepository;
import app.rettiwtSpring.service.PostService;
import lombok.RequiredArgsConstructor;


@RestController
@RequestMapping("/feed")
@RequiredArgsConstructor
public class FeedController {
    private final PostService postService;
    private final LikeRepository likeRepository;
    private final CommentRepository commentRepository;

    private List<PostDto> mapToDtoList(List<Post> posts, User currUser) {
        return posts.stream().map(post -> {
            boolean liked = false;
            if (currUser != null) {
                liked = likeRepository.existsByPostIdAndUserId(post.getId(), currUser.getId());
            }
            boolean hasMedia = post.getMedia()!=null;
            return new PostDto(
                post.getId(),
                post.getText(),
                post.getCreatedAt(),
                new UserSummaryDto(post.getUser().getId(), post.getUser().getUsername()),
                likeRepository.countByPostId(post.getId()),
                commentRepository.findByPostIdWithUser(post.getId()).size(),
                liked,
                hasMedia
            );
        }).toList();
    }

    @GetMapping
    public ResponseEntity<FeedResponseDto> getGlobalFeed(@AuthenticationPrincipal User currUser){
        List<Post> posts = postService.getGlobalFeed();
        return ResponseEntity.ok(new FeedResponseDto(mapToDtoList(posts, currUser)));
    }
    @GetMapping("/user/{userId}")
    public ResponseEntity<FeedResponseDto> getUserPosts(@AuthenticationPrincipal User currUser, @PathVariable Long userId) {
       
        List<Post> posts = postService.getGlobalFeed().stream()
                .filter(p -> p.getUser().getId().equals(userId))
                .toList();
        return ResponseEntity.ok(new FeedResponseDto(mapToDtoList(posts, currUser)));
    }

    @GetMapping("/media")
    public ResponseEntity<FeedResponseDto> getMediaFeed(@AuthenticationPrincipal User currUser) {
        List<Post> posts = postService.getPostsWithMedia();
        return ResponseEntity.ok(new FeedResponseDto(mapToDtoList(posts, currUser)));
    }

    @GetMapping("/followed")
    public ResponseEntity<FeedResponseDto> getFollowedFeed(@AuthenticationPrincipal User currUser) {
        List<Post> posts = postService.getFeedFromFollowed(currUser.getId());
        return ResponseEntity.ok(new FeedResponseDto(mapToDtoList(posts, currUser)));
    }
    
}
