package app.rettiwtSpring.dto;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class FeedResponseDto{
    private List<PostDto> posts;
}
