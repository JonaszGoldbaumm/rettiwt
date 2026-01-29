package app.rettiwtSpring.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class RegisterRequest {
    @NotBlank
    private String username;
    @Email
    @NotBlank
    private String email;
    @NotBlank
    private String password;
}
