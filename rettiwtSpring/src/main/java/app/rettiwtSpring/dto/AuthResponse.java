package app.rettiwtSpring.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class AuthResponse {
    private String access_token;
    private String token_type;
    private Long user_id;
    private String username;
      
}
