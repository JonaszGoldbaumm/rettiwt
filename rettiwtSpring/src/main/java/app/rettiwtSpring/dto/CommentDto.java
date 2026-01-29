package app.rettiwtSpring.dto;

import java.time.Instant;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class CommentDto {
    private Long id;
    private String text;
    private Instant created_at;
    private UserSummaryDto user;
}
