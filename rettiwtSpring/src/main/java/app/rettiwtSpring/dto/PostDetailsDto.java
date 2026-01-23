package app.rettiwtSpring.dto;

import java.util.List;

import app.rettiwtSpring.model.Comment;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class PostDetailsDto {
    private Long postId;
    private Long likeCount;
    private boolean likedByCurrentUser;
    private List<Comment> comments;
}
