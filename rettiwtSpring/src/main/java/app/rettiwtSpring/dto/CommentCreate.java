package app.rettiwtSpring.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class CommentCreate {
    @NotBlank(message="Comments must have text")
    private String text;
}
