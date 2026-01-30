package app.rettiwtSpring.controllers;

import java.io.IOException;
import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.server.ResponseStatusException;

import app.rettiwtSpring.dto.CommentCreate;
import app.rettiwtSpring.dto.LikeActionDto;
import app.rettiwtSpring.dto.PostDetailsDto;
import app.rettiwtSpring.model.Comment;
import app.rettiwtSpring.model.Post;
import app.rettiwtSpring.model.User;
import app.rettiwtSpring.repository.CommentRepository;
import app.rettiwtSpring.repository.PostRepository;
import app.rettiwtSpring.service.PostDetailsService;
import app.rettiwtSpring.service.PostInteractionService;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/post")
@RequiredArgsConstructor
public class PostController {
    private final PostInteractionService interactionService;
    private final PostDetailsService postDetailsService;
    private final PostRepository postRepository;
    private final CommentRepository commentRepository;

    @PostMapping(consumes=MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<LikeActionDto> createPost(
        @RequestParam("text") String text,
        @RequestParam(value="media", required=false) MultipartFile media,
        @AuthenticationPrincipal User currUser) throws IOException{
        
            byte[] mediaBytes = null;
        if (media != null && !media.isEmpty()) {
            String contentType = media.getContentType();
            if (contentType == null || !List.of("image/jpeg", "image/png", "image/webp").contains(contentType)) {
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Invalid image type");
            }
            if(text.isEmpty()){
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Post must contain text");
            }
            mediaBytes = media.getBytes();
        }

        interactionService.createPost(currUser.getId(), text.trim(), mediaBytes);
        return ResponseEntity.status(HttpStatus.CREATED).body(new LikeActionDto(true));
    }
    @GetMapping("/{postId}")
    public ResponseEntity<PostDetailsDto> getPostDetails(
            @PathVariable Long postId, 
            @AuthenticationPrincipal User currUser) {
        
        Long userId = (currUser != null) ? currUser.getId() : null;
        
        return ResponseEntity.ok(postDetailsService.getPostDetails(postId, userId));
    }

    @GetMapping("/{postId}/media")
    public ResponseEntity<byte[]> getPostMedia(@PathVariable Long postId) {
        Post post = postRepository.findById(postId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Post not found"));
        
        if (post.getMedia() == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Media not found");
        }

        return ResponseEntity.ok()
                .contentType(MediaType.IMAGE_JPEG)
                .body(post.getMedia());
    }

    @PostMapping("/{postId}/like")
    public ResponseEntity<LikeActionDto> toggleLike(@PathVariable Long postId, @AuthenticationPrincipal User currUser) {
        interactionService.likePost(postId, currUser.getId());
        return ResponseEntity.ok(new LikeActionDto(true));
    }

    @PostMapping("/{postId}/comment")
    public ResponseEntity<LikeActionDto> addComment(
            @PathVariable Long postId, 
            @RequestBody CommentCreate data, 
            @AuthenticationPrincipal User currUser) {
        
        interactionService.createComment(currUser.getId(), postId, data.getText().trim());
        return ResponseEntity.ok(new LikeActionDto(true));
    }

    @DeleteMapping("/{postId}")
    public ResponseEntity<LikeActionDto> deletePost(@PathVariable Long postId, @AuthenticationPrincipal User currUser) {
        Post post = postRepository.findById(postId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Post not found"));

        if (!post.getUser().getId().equals(currUser.getId())) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "Not allowed");
        }

        interactionService.deletePost(postId);
        return ResponseEntity.ok(new LikeActionDto(true));
    }

    @DeleteMapping("/comments/{commentId}")
    public ResponseEntity<LikeActionDto> deleteComment(@PathVariable Long commentId, @AuthenticationPrincipal User currUser) {
        Comment comment = commentRepository.findById(commentId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Comment not found"));

        if (!comment.getUser().getId().equals(currUser.getId())) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "Not allowed");
        }

        interactionService.deleteComment(commentId);
        return ResponseEntity.ok(new LikeActionDto(true));
    }
}
