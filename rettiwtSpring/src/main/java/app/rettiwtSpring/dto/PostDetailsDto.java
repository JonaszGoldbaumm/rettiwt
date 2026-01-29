package app.rettiwtSpring.dto;

import java.time.Instant;
import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter @Setter
@AllArgsConstructor
@NoArgsConstructor
public class PostDetailsDto {
    private Long id;
    private String text;
    private Instant created_at;
    private UserSummaryDto author;
    private int like_count;
    private boolean liked_by_user;
    private List<CommentDto> comments;
}