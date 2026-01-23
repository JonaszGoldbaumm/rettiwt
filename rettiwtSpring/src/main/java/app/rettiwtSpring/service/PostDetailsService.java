package app.rettiwtSpring.service;

import java.util.List;

import org.springframework.stereotype.Service;

import app.rettiwtSpring.dto.PostDetailsDto;
import app.rettiwtSpring.model.Comment;
import app.rettiwtSpring.repository.CommentRepository;
import app.rettiwtSpring.repository.LikeRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class PostDetailsService {
    private final CommentRepository commentRepository;
    private final LikeRepository likeRepository;

    public PostDetailsDto getPostDetails(Long postId, Long currUserId){
        List<Comment> comments = commentRepository.findByPostIdWithUser(postId);

        long likecnt = likeRepository.countByPostId(postId);
        boolean likedByUser= false;
        if(currUserId != null){
            likedByUser = likeRepository.existsByPostIdAndUserId(postId, currUserId);
        }

        return new PostDetailsDto(postId, likecnt, likedByUser, comments);

    }
}
