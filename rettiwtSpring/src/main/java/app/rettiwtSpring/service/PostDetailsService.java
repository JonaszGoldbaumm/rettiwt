package app.rettiwtSpring.service;

import java.util.List;

import org.springframework.stereotype.Service;

import app.rettiwtSpring.config.PostNotFoundException;
import app.rettiwtSpring.dto.CommentDto;
import app.rettiwtSpring.dto.PostDetailsDto;
import app.rettiwtSpring.dto.UserSummaryDto;
import app.rettiwtSpring.model.Post;
import app.rettiwtSpring.repository.CommentRepository;
import app.rettiwtSpring.repository.LikeRepository;
import app.rettiwtSpring.repository.PostRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class PostDetailsService {
    private final CommentRepository commentRepository;
    private final LikeRepository likeRepository;
    private final PostRepository postRepository;
    

    public PostDetailsDto getPostDetails(Long postId, Long currUserId){
        Post post = postRepository.findByIdWithUser(postId);
        if(post == null) throw new PostNotFoundException(postId.toString());

        List<CommentDto> comments = commentRepository.findByPostIdWithUser(postId)
            .stream().map(c -> new CommentDto(c.getId(), c.getText(), c.getCreatedAt(),
            new UserSummaryDto(c.getUser().getId(), c.getUser().getUsername())
        )).toList();
        int likeCnt = likeRepository.countByPostId(postId);
        boolean liked = currUserId != null && likeRepository.existsByPostIdAndUserId(postId, currUserId);

        return new PostDetailsDto(
            post.getId(),
            post.getText(),
            post.getCreatedAt(),
            new UserSummaryDto(post.getUser().getId(), post.getUser().getUsername()),
            likeCnt,
            liked,
            comments,
            post.getMedia() != null
        );
    }
}
