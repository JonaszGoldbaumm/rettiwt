package app.rettiwtSpring.service;

import org.springframework.stereotype.Service;

import app.rettiwtSpring.config.PostNotFoundException;
import app.rettiwtSpring.config.UserNotFoundException;
import app.rettiwtSpring.model.Comment;
import app.rettiwtSpring.model.Like;
import app.rettiwtSpring.model.LikeId;
import app.rettiwtSpring.model.Post;
import app.rettiwtSpring.model.User;
import app.rettiwtSpring.repository.CommentRepository;
import app.rettiwtSpring.repository.LikeRepository;
import app.rettiwtSpring.repository.PostRepository;
import app.rettiwtSpring.repository.UserRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class PostInteractionService {
    private final PostRepository postRepository;
    private final CommentRepository commentRepository;
    private final LikeRepository likeRepository;
    private final UserRepository userRepository;

    public void createPost(Long userId, String text, byte[] media){
        User user = userRepository.findById(userId).orElseThrow(()->new UserNotFoundException(userId.toString()));

        Post post = new Post(null, text, media, user, null);
        postRepository.save(post);
    }

    public void deletePost(Long postId){
        postRepository.deleteById(postId);
    }



    public void likePost(Long postId, Long userId){
        if (likeRepository.existsByPostIdAndUserId(postId, userId)){
            likeRepository.deleteByPostIdAndUserId(postId, userId);
            return;
        }

        Post post = postRepository.findById(postId).orElseThrow(()->new PostNotFoundException(postId.toString()));
        User user = userRepository.findById(userId).orElseThrow(()->new UserNotFoundException(userId.toString()));
        Like like = new Like(new LikeId(postId, userId), post, user, null);
        likeRepository.save(like); 
    }

    // public void unlikePost(Long postId, Long userId){
    //     if(!likeRepository.existsByPostIdAndUserId(postId, userId)){
    //         return;
    //     }
    //     likeRepository.deleteByPostIdAndUserId(postId, userId);
    // }

    public void createComment(Long userId, Long postId, String text){
        Post post = postRepository.findById(postId).orElseThrow(()->new PostNotFoundException(postId.toString()));
        User user = userRepository.findById(userId).orElseThrow(()->new UserNotFoundException(userId.toString()));
        Comment comment = new Comment(null, text, post, user, null);

        commentRepository.save(comment);
    }

    public void deleteComment(Long comId){
        commentRepository.deleteById(comId);
    }

}
