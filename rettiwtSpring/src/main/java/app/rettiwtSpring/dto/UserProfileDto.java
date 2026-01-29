package app.rettiwtSpring.dto;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class UserProfileDto {
    private Long id;
    private String username;
    private String email;
    private String description;

    private int followers_count;
    private int followed_count;

    private List<UserSummaryDto> followers;
    private List<UserSummaryDto> followed;
    
}
