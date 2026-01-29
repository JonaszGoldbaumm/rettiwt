package app.rettiwtSpring.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class LoginRequest {
    @NotBlank
    private String username_or_email;
    @NotBlank
    private String password;
}
