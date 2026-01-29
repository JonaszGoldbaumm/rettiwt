package app.rettiwtSpring.dto;

import java.time.Instant;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class PostDto {
    private Long id;
    private String text;
    private Instant created_at;
    private UserSummaryDto user;
    private int like_count;
    private int comment_count;
    private boolean liked_by_user;
    private boolean has_media;
}
