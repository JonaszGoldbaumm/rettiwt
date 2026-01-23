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
    private byte[] profilePic;
    private String description;
    private long followerCount;
    private long followedCount;
    private List<UserSummaryDto> followers;
    private List<UserSummaryDto> followed;
}
